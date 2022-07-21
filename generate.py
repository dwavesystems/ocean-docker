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
from itertools import product
from collections import defaultdict, namedtuple

import click
import chevron


# ocean version under build
# TODO: get latest from github releases
OCEAN_VERSION = os.getenv('OCEAN_VERSION')

if OCEAN_VERSION is None:
    print("Please specify Ocean version under build with OCEAN_VERSION env var.")
    exit(1)

# ocean version under build, as named tuple
ocean_version_info = namedtuple('Version', 'major minor patch')(*OCEAN_VERSION.split('.'))

def _get_version(version_info, significant_parts=None):
    if significant_parts is None:
        significant_parts = len(version_info)
    return '.'.join(version_info[:significant_parts])

OCEAN_VERSIONS_ROUNDED = [_get_version(ocean_version_info, n+1)
                          for n in range(len(ocean_version_info))]

assert len(OCEAN_VERSIONS_ROUNDED) == 3
OCEAN_VERSION_MAJOR, OCEAN_VERSION_MINOR, OCEAN_VERSION_PATCH = OCEAN_VERSIONS_ROUNDED

def version_rounded(version, scale, sep='.'):
    return sep.join((version.split(sep))[:scale+1])


class BuildConfig:
    DEFAULT_TAG = 'latest'

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

    def tag_info(self, **subtags):
        """Build a tag and canonical tag info from sub-tags.
        Return (tag, canonical tag, canonical subtags).
        """
        # `subtags` key order matters! use: (ocean, python, platform)
        tag = self.make_tag(**subtags)

        # derive canonical sub-tag (from, possibly, an alias)
        def _expand(name, value):
            # expand defaults and aliases
            if value is None:
                value = self.config['defaults'][name]
            return self.config['aliases'].get(name, {}).get(value, value)

        canonical_subtags = {k: _expand(k,v) for k, v in subtags.items()}
        canonical_tag = self.make_tag(**canonical_subtags)

        return namedtuple('TagInfo', 'tag canonical_tag canonical_subtags')(
            tag, canonical_tag, canonical_subtags)

    def get_tags(self, ocean_versions, python_versions, platform_tags):
        """Produce: (1) a map of canonical tags (that we need to build) to a bag of
        alias tags; (2) canonical sub-tags for each canonical tag; and (3) a map of
        upstream canonical tags for each tag.
        """
        tag_bags = defaultdict(set)   # Dict[str, Set[str]]
        sub_tags = dict()   # Dict[str, Dict[str, str]]
        upstream = dict()   # Dict[str, str]

        for oc, py, pl in product(ocean_versions, python_versions, platform_tags):
            info = self.tag_info(ocean=oc, python=py, platform=pl)
            tag_bags[info.canonical_tag].add(info.tag)
            sub_tags[info.canonical_tag] = info.canonical_subtags
            upstream[info.tag] = info.canonical_tag

        return namedtuple('Tags', 'bags canonical upstream')(
            tag_bags, sub_tags, upstream)

    def __init__(self, config_file, **context):
        with open(config_file) as fp:
            config = json.load(fp)

        self.config = BuildConfig.expand_template(config, **context)

        self.tags = self.get_tags(
            self.ocean_versions, self.python_versions, self.platform_tags)

    @property
    def ocean_versions(self):
        return self.config['matrix']['ocean']

    @property
    def python_versions(self):
        return self.config['matrix']['python']

    @property
    def platform_tags(self):
        return self.config['matrix']['platform']


build = BuildConfig('build.json', ocean=OCEAN_VERSION)


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
    """Print tags to build for OCEAN_VERSION from environment."""

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

    print(f"===\nall tags: {len(all_tags)}\n===")
    for tag in sorted(all_tags):
        print(tag)


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
    base = './dockerfiles'
    ocean_dirs = {version_rounded(c_sub['ocean'], ocean_version_scale)
                  for c_sub in canonical_tags.values()}
    for ocean_dir in ocean_dirs:
        shutil.rmtree(os.path.join(base, ocean_dir), ignore_errors=True)

    # load template
    template_path = 'Dockerfile-linux.template'
    with open(template_path) as fp:
        template = fp.read()

    # generate `Dockerfile` and `tags.json` for each canonical tag
    for c_tag, c_sub in canonical_tags.items():
        click.echo(f"Processing {c_tag!r} = {c_sub!r}")
        ocean_dir = version_rounded(c_sub['ocean'], ocean_version_scale)
        python_dir = f"python{c_sub['python']}"
        platform = c_sub['platform']

        dir = os.path.join(base, ocean_dir, python_dir, platform)
        target = os.path.join(dir, 'Dockerfile')
        tagsfile = os.path.join(dir, 'tags.json')
        os.makedirs(dir)

        dockerfile = chevron.render(template, data=dict(
            python_version=c_sub['python'],
            ocean_version=c_sub['ocean'],
            distribution_tag=platform,
            is_slim=('slim' in platform)))

        click.echo(f"- writing {target!r}")
        with open(target, "w") as fp:
            fp.write(dockerfile)

        click.echo(f"- writing {tagsfile!r}")
        with open(tagsfile, "w") as fp:
            json.dump(get_tag_meta(build.tags, c_tag), fp, indent=2)


if __name__ == '__main__':
    cli()
