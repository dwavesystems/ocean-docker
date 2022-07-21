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

# build a cartesian product of these subcomponents (sub-tags)
# (`None` = use a value as defined in `CANONICAL_TAGS`, but leave out the sub-tag name)
OCEAN_VERSIONS = {None}.union(OCEAN_VERSIONS_ROUNDED)
PYTHON_VERSIONS = {None, '3.8', '3.9', '3.10'}
PLATFORM_TAGS = {None, 'bullseye', 'slim', 'slim-bullseye'}

# sub-tag alias map
# note: expanded here for clarity (vs scripted)
CANONICAL_TAGS = {
    'ocean': {
        None: OCEAN_VERSION,
        OCEAN_VERSION_MAJOR: OCEAN_VERSION,
        OCEAN_VERSION_MINOR: OCEAN_VERSION,
        OCEAN_VERSION_PATCH: OCEAN_VERSION,
    },
    'python': {
        None: '3.9'
    },
    'platform': {
        None: 'bullseye',
        'slim': 'slim-bullseye',
    }
}


def make_tag(ocean, python, platform, default_tag='latest'):
    """Form a tag name from sub-tags."""
    if python is not None:
        python = f"python{python}"

    nonempty_subtags = list(filter(None, (ocean, python, platform)))
    if nonempty_subtags:
        tag = '-'.join(nonempty_subtags)
    else:
        tag = default_tag
    return tag


def tag_info(default_tag='latest', **subtags):
    """Build a tag and canonical tag info from sub-tags.
    Return (tag, canonical tag, canonical subtags).
    """
    # `subtags` key order matters! use: (ocean, python, platform)
    tag = make_tag(**subtags)

    # derive canonical sub-tag (from, possibly, an alias)
    canonical_subtags = {k: CANONICAL_TAGS[k].get(v, v) for k, v in subtags.items()}
    canonical_tag = make_tag(**canonical_subtags)

    return namedtuple('TagInfo', 'tag canonical_tag canonical_subtags')(
        tag, canonical_tag, canonical_subtags)


def get_tags(ocean_versions, python_versions, platform_tags):
    """Produce: (1) a map of canonical tags (that we need to build) to a bag of
    alias tags; (2) canonical sub-tags for each canonical tag; and (3) a map of
    upstream canonical tags for each tag.
    """
    tag_bags = defaultdict(set)   # Dict[str, Set[str]]
    sub_tags = dict()   # Dict[str, Dict[str, str]]
    upstream = dict()   # Dict[str, str]

    for oc, py, pl in product(ocean_versions, python_versions, platform_tags):
        info = tag_info(ocean=oc, python=py, platform=pl)
        tag_bags[info.canonical_tag].add(info.tag)
        sub_tags[info.canonical_tag] = info.canonical_subtags
        upstream[info.tag] = info.canonical_tag

    return namedtuple('Tags', 'bags canonical upstream')(
        tag_bags, sub_tags, upstream)


def version_rounded(version, scale, sep='.'):
    return sep.join((version.split(sep))[:scale+1])


def get_tag_meta(build_info, tag):
    if tag in build_info.canonical:
        canonical_tag = tag
    elif tag in build_info.upstream:
        canonical_tag = build_info.upstream[tag]
    else:
        raise ValueError('Canonical tag not found')

    return {
        'canonical_tag': canonical_tag,
        'alias_tags': list(build_info.bags[canonical_tag].difference([canonical_tag])),
        'subtags': build_info.canonical[canonical_tag],
    }


@click.group()
def cli():
    """Generate tags or dockerfiles."""


@cli.command()
def tags():
    """Print tags to build for OCEAN_VERSION from environment."""

    tag_bags = get_tags(OCEAN_VERSIONS, PYTHON_VERSIONS, PLATFORM_TAGS).bags
    all_tags = set(tag_bags.keys()).union(*tag_bags.values())

    print(f"===\nmatrix\n===\n"
          f"- ocean: {', '.join(filter(None, OCEAN_VERSIONS))}\n"
          f"- python: {', '.join(filter(None, PYTHON_VERSIONS))}\n"
          f"- platform: {', '.join(filter(None, PLATFORM_TAGS))}\n")

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

    build_info = get_tags(OCEAN_VERSIONS, PYTHON_VERSIONS, PLATFORM_TAGS)
    if not tags:
        tags = build_info.canonical.keys()

    meta = [get_tag_meta(build_info, tag) for tag in tags]

    for tagmeta in meta:
        click.echo(json.dumps(tagmeta, indent=2))


@cli.command()
@click.option('--ocean-version-scale', default=1, type=int,
              help='Number of Ocean version components after major, in directory name.')
def dockerfiles(ocean_version_scale):
    """Create all Dockerfiles required to build our matrix of images."""

    build_info = get_tags(OCEAN_VERSIONS, PYTHON_VERSIONS, PLATFORM_TAGS)
    sub_tags = build_info.canonical

    # purge old dockerfiles
    base = './dockerfiles'
    shutil.rmtree(base, ignore_errors=True)

    # load template
    template_path = 'Dockerfile-linux.template'
    with open(template_path) as fp:
        template = fp.read()

    # generate Dockerfile for each canonical tag
    for c_tag, c_sub in sub_tags.items():
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
            json.dump(get_tag_meta(build_info, c_tag), fp, indent=2)


if __name__ == '__main__':
    cli()
