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
from itertools import product
from collections import defaultdict, namedtuple

import click
import jinja2


# ocean version under build
# TODO: get latest from github releases
OCEAN_VERSION = os.environ['OCEAN_VERSION']

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
PYTHON_VERSIONS = {None, 'python3.8', 'python3.9', 'python3.10'}
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
        None: 'python3.9'
    },
    'platform': {
        None: 'bullseye',
        'slim': 'slim-bullseye',
    }
}


def build_tag(default_tag='latest', **subtags):
    """Build a tag from sub-tags. Return (tag, canonical tag) tuple."""
    # `subtags` key order matters! use: (ocean, python, platform)
    nonempty_subtags = list(filter(None, subtags.values()))
    if nonempty_subtags:
        tag = '-'.join(nonempty_subtags)
    else:
        tag = default_tag

    # derive canonical sub-tag (from, possibly, an alias)
    canonical_subtags = (CANONICAL_TAGS[k].get(v, v) for k, v in subtags.items())
    canonical_tag = '-'.join(canonical_subtags)

    return tag, canonical_tag


def get_tags(ocean_versions, python_versions, platform_tags):
    """Produce a map of canonical tags (that we need to build) to a bag of
    alias tags.
    """
    tag_bags = defaultdict(set)   # Dict[str, Set[str]]

    for oc, py, pl in product(ocean_versions, python_versions, platform_tags):
        tag, canonical_tag = build_tag(ocean=oc, python=py, platform=pl)
        tag_bags[canonical_tag].add(tag)

    return tag_bags


@click.group()
def cli():
    """Generate tags or dockerfiles."""

@cli.command()
def tags():
    """Print tags to build for OCEAN_VERSION from environment."""
    tag_bags = get_tags(OCEAN_VERSIONS, PYTHON_VERSIONS, PLATFORM_TAGS)
    all_tags = set(tag_bags.keys()).union(*tag_bags.values())

    print(f"===\nmatrix\n===\n"
        f"- ocean: {', '.join(filter(None, OCEAN_VERSIONS))}\n"
        f"- python: {', '.join(filter(None, PYTHON_VERSIONS))}\n"
        f"- platform: {', '.join(filter(None, PLATFORM_TAGS))}\n")

    print("===\ncanonical images/tags:", len(tag_bags), '\n===')
    for canonical, aliases in tag_bags.items():
        print(f'{canonical}:\n  {", ".join(sorted(aliases.difference(canonical)))}\n')

    print(f"===\nall tags: {len(all_tags)}\n===")
    for tag in sorted(all_tags):
        print(tag)

@cli.command()
def dockerfiles():
    pass

if __name__ == '__main__':
    cli()
