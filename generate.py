# Copyright 2022 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Generate/preview all tags a build matrix should generate, together with each
tag mapped to a canonical tag.
"""

import os
import re
import json
import shutil
from itertools import product, groupby
from collections import defaultdict, namedtuple

import click
import chevron
import requests


REPO_URL = 'https://github.com/dwavesystems/ocean-docker'


def get_latest_ocean_version():
    url = 'https://api.github.com/repos/dwavesystems/dwave-ocean-sdk/releases'
    releases = requests.get(url, params=dict(per_page=50, page=1)).json()
    tags = [release['tag_name'] for release in releases]
    return max(tags, key=lambda tag: tag.split('.'))

def version_rounded(version, scale, sep='.'):
    return sep.join((version.split(sep))[:scale+1])

def subtags_subset_of(subtags: dict, item: dict):
    return set(subtags.items()).issubset(item.items())

def get_repo_path_url(path, repo_url=REPO_URL):
    # TODO: perhaps use permalink/tag/commit instead of latest master
    return f"{repo_url}/blob/master/{path}"


class BuildConfig:
    DEFAULT_TAG = 'latest'
    DOCKERFILES_PATH = 'dockerfiles'
    DEFAULT_VERSION_SCALE = 0

    @staticmethod
    def expand_template(obj, **context):
        """Recursively expand string templates in build config object."""
        subs = {
            'ocean.major': version_rounded(context['ocean'], 0),
            'ocean.minor': version_rounded(context['ocean'], 1),
            'ocean.patch': version_rounded(context['ocean'], 2),
        }
        if isinstance(obj, str):
            return re.sub(r"\{(?P<var>[\w.:-]+)\}", lambda m: subs[m['var']], obj)
        elif isinstance(obj, dict):
            return {BuildConfig.expand_template(k, **context):
                    BuildConfig.expand_template(v, **context)
                    for k, v in obj.items()}
        elif isinstance(obj, list):
            return [BuildConfig.expand_template(v, **context) for v in obj]
        return obj

    @classmethod
    def make_tag(cls, ocean, python, platform):
        """Form a tag name from sub-tags."""
        if python is not None:
            python = f"python{python}"

        nonempty_subtags = list(filter(None, (ocean, python, platform)))
        if nonempty_subtags:
            tag = '-'.join(nonempty_subtags)
        else:
            tag = cls.DEFAULT_TAG
        return tag

    def tag_info(self, *, defaults, **subtags):
        """Build a tag and canonical tag info from sub-tags. Substitute null
        subtag values according to defaults map (category -> value).
        Return (tag, canonical tag, canonical subtags).
        """
        # `subtags` key order matters! use: (ocean, python, platform)
        tag = self.make_tag(**subtags)

        # derive canonical sub-tag (from, possibly, an alias)
        def _expand(name, value):
            # expand defaults and aliases
            if value is None:
                value = defaults[name]
            return self.config['aliases'].get(name, {}).get(value, value)

        canonical_subtags = {k: _expand(k,v) for k, v in subtags.items()}
        canonical_tag = self.make_tag(**canonical_subtags)

        return namedtuple('TagInfo', 'tag canonical_tag canonical_subtags')(
            tag, canonical_tag, canonical_subtags)

    def get_tags(self, ocean_versions, python_versions, platform_tags, defaults=None):
        """Produce: (1) a map of canonical tags (that we need to build) to a bag of
        alias tags; (2) canonical sub-tags for each canonical tag; and (3) a map of
        upstream canonical tags for each tag.
        """
        if defaults is None:
            defaults = self.config['defaults']

        tag_bags = defaultdict(set)   # Dict[str, Set[str]]
        sub_tags = dict()   # Dict[str, Dict[str, str]]
        upstream = dict()   # Dict[str, str]

        def is_excluded(tag, rules):
            for rule in rules:
                if subtags_subset_of(rule, tag.canonical_subtags):
                    return True
            return False

        for oc, py, pl in product(ocean_versions, python_versions, platform_tags):
            info = self.tag_info(ocean=oc, python=py, platform=pl, defaults=defaults)
            if is_excluded(info, self.config['exclude']):
                continue
            tag_bags[info.canonical_tag].add(info.tag)
            sub_tags[info.canonical_tag] = info.canonical_subtags
            upstream[info.tag] = info.canonical_tag

        return namedtuple('Tags', 'bags canonical upstream')(
            tag_bags, sub_tags, upstream)

    def get_shared_tags(self, config):
        """Produce a map of shared tag to a set of canonical tags.
        """
        shared_tags = defaultdict(set)      # Dict[str, Set[str]]

        for contracted in config['shared']['contracted']:
            defaults = config['defaults'].copy()
            defaults.update(contracted)
            tags = self.get_tags(
                ocean_versions=config['shared']['matrix']['ocean'],
                python_versions=config['shared']['matrix']['python'],
                platform_tags=config['shared']['matrix']['platform'],
                defaults=defaults)

            # non-canonical shared
            for canonical in tags.canonical:
                tags.upstream.pop(canonical, None)
            for shared_tag, canonical_tag in tags.upstream.items():
                shared_tags[shared_tag].add(canonical_tag)

        return shared_tags

    def get_template_path(self, **subtags):
        """Filter `config.template` and return the first that matches `subtags`."""

        templates = self.config['template']
        for path, filters in templates.items():
            for requirements in filters:
                if subtags_subset_of(requirements, subtags):
                    return path

    def get_dockerfile_path(self, tag, ocean_version_scale=None):
        """Return Dockerfile repo path, for a tag (canonical or alias)."""

        c_tag = self.tags.upstream[tag]
        c_sub = self.tags.canonical[c_tag]

        if ocean_version_scale is None:
            ocean_version_scale = self.DEFAULT_VERSION_SCALE

        ocean_dir = version_rounded(c_sub['ocean'], ocean_version_scale)
        python_dir = f"python{c_sub['python']}"
        platform = c_sub['platform']

        return os.path.join(
            self.DOCKERFILES_PATH, ocean_dir, python_dir, platform, 'Dockerfile')

    def __init__(self, config_file, ocean_version):
        with open(config_file) as fp:
            config = json.load(fp)

        self.ocean_version = ocean_version
        ctx = dict(ocean=self.ocean_version)
        self.config = BuildConfig.expand_template(config, **ctx)

        self.tags = self.get_tags(
            self.ocean_versions, self.python_versions, self.platform_tags)

        self.shared_tags = self.get_shared_tags(self.config)

    @property
    def ocean_versions(self):
        return self.config['matrix']['ocean']

    @property
    def python_versions(self):
        return self.config['matrix']['python']

    @property
    def platform_tags(self):
        return self.config['matrix']['platform']


# ocean version under build
OCEAN_VERSION = os.getenv('OCEAN_VERSION', get_latest_ocean_version())

# TODO: move under cli command(s), build file as option
build = BuildConfig(config_file='build.json', ocean_version=OCEAN_VERSION)


def get_tag_meta(build_info, tag):
    if tag in build_info.canonical:
        canonical_tag = tag
    elif tag in build_info.upstream:
        canonical_tag = build_info.upstream[tag]
    else:
        raise ValueError('Canonical tag not found')

    return {
        'canonical_tag': canonical_tag,
        'alias_tags': sorted(build_info.bags[canonical_tag].difference([canonical_tag])),
        'subtags': build_info.canonical[canonical_tag],
    }


@click.group()
def cli():
    """Generate tags or dockerfiles."""


@cli.command()
def tags():
    """Print tags to build for Ocean version under build."""

    tag_bags = build.tags.bags
    all_tags = set(tag_bags.keys()).union(*tag_bags.values())

    _alias = lambda cat, tag: build.config['aliases'].get(cat, {}).get(tag)
    _append = lambda cat, tag: f"{tag} (=={_alias(cat, tag)})" if _alias(cat, tag) else tag
    print(f"===\nmatrix\n===\n"
          f"- ocean: {', '.join(_append('ocean', v) for v in build.ocean_versions if v)}\n"
          f"- python: {', '.join(_append('python', v) for v in build.python_versions if v)}\n"
          f"- platform: {', '.join(_append('platform', v) for v in build.platform_tags if v)}\n")

    print("===\ncanonical images/tags:", len(tag_bags), '\n===')
    for canonical, aliases in tag_bags.items():
        print(f'{canonical}:\n  {", ".join(sorted(aliases.difference([canonical])))}\n')

    print(f"===\nsingle-platform tags: {len(all_tags)}\n===")
    for tag in sorted(all_tags):
        print(tag)

    shared_tags = build.shared_tags
    print(f"\n===\nshared tags: {len(shared_tags)}\n===")
    for tag, canonical in shared_tags.items():
        print(f'{tag}:\n  {", ".join(sorted(canonical))}\n')


@cli.command()
def version():
    """Print Ocean version used."""
    click.echo(build.ocean_version)


@cli.command()
@click.option('--template', default='README.md.template', type=click.File('r'),
              help='README.md template file path. Set to "-" for stdin.')
@click.option('--output', default='README.md', type=click.File('w'),
              help='README.md file path. Set to "-" for stdout.')
def readme(template, output):
    """Create README.md from a template."""

    simple = build.tags
    shared = build.shared_tags

    simple_tags = [{"tags": sorted(a_tags),
                    "dockerfile": get_repo_path_url(build.get_dockerfile_path(c_tag)),
                    "subtags": simple.canonical[c_tag]}
                   for c_tag, a_tags in simple.bags.items()]

    _key = lambda tag: ','.join(sorted(shared[tag]))
    grouped = groupby(sorted(shared, key=_key), key=_key)
    shared_tags = []
    for _, g in grouped:
        tags = sorted(g)
        shared_tags.append({
            "tags": tags,
            "canonical": [{"tag": c_tag,
                           "dockerfile": get_repo_path_url(build.get_dockerfile_path(c_tag))}
                          for c_tag in sorted(shared[tags[0]])]
        })

    def f_strip(text, render):
        return render(text).strip(' ,')

    readme = chevron.render(template.read(), data=dict(
        ocean_version=build.ocean_version,
        simple_tags=simple_tags,
        shared_tags=shared_tags,
        strip=f_strip))

    output.write(readme)
    click.echo(f"Generated {output.name!r} for Ocean {build.ocean_version}.")


@cli.command()
@click.argument('tags', nargs=-1)
def meta(tags):
    """Output image meta data for TAGS given."""

    build_info = build.tags
    if not tags:
        tags = build_info.canonical.keys()

    meta = [get_tag_meta(build_info, tag) for tag in tags]

    for tagmeta in meta:
        click.echo(json.dumps(tagmeta, indent=2))


@cli.command()
@click.option('--ocean-version-scale', default=0, type=int,
              help='Number of Ocean version components after major, in directory name.')
def dockerfiles(ocean_version_scale):
    """Create all Dockerfiles required to build our matrix of images."""

    canonical_tags = build.tags.canonical

    # purge old dockerfiles for ocean version under update
    base_dir = build.DOCKERFILES_PATH
    ocean_dirs = {version_rounded(c_sub['ocean'], ocean_version_scale)
                  for c_sub in canonical_tags.values()}
    for ocean_dir in ocean_dirs:
        shutil.rmtree(os.path.join(base_dir, ocean_dir), ignore_errors=True)

    # generate `Dockerfile` and `tags.json` for each canonical tag
    for c_tag, c_sub in canonical_tags.items():
        click.echo(f"Processing {c_tag!r} = {c_sub!r}")

        dockerfile_path = build.get_dockerfile_path(c_tag, ocean_version_scale=ocean_version_scale)
        dir = os.path.dirname(dockerfile_path)
        tagsfile_path = os.path.join(dir, 'tags.json')
        os.makedirs(dir)

        # load template
        template_path = build.get_template_path(**c_sub)
        with open(template_path) as fp:
            template = fp.read()

        # render dockerfile
        dockerfile = chevron.render(template, data=dict(
            python_version=c_sub['python'],
            ocean_version=c_sub['ocean'],
            distribution_tag=c_sub['platform'],
            is_slim=('slim' in c_sub['platform'])))

        click.echo(f"- writing {dockerfile_path!r}")
        with open(dockerfile_path, "w") as fp:
            fp.write(dockerfile)

        click.echo(f"- writing {tagsfile_path!r}")
        with open(tagsfile_path, "w") as fp:
            json.dump(get_tag_meta(build.tags, c_tag), fp, indent=2)

    # generate shared-tags.json
    ocean_dir = version_rounded(build.ocean_version, ocean_version_scale)
    sharedtags_path = os.path.join(base_dir, ocean_dir, 'shared-tags.json')
    sharedtags = {tag: sorted(canonical) for tag, canonical in build.shared_tags.items()}

    click.echo(f"Writing {sharedtags_path!r}")
    with open(sharedtags_path, "w") as fp:
        json.dump(sharedtags, fp, indent=2)


if __name__ == '__main__':
    cli()
