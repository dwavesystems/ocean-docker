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

from itertools import product
from collections import defaultdict, namedtuple


# ocean version under build
# TODO: get latest from github releases
OCEAN_VERSION = '5.3.0'

# ocean version under build, as named tuple
ocean_version_info = namedtuple('Version', 'major minor patch')(*OCEAN_VERSION.split('.'))

def get_version(version_info, significant_parts=None):
    if significant_parts is None:
        significant_parts = len(version_info)
    return '.'.join(version_info[:significant_parts])

# build a cartesian product of these subcomponents (subtags)
# (`None` = use a default value as defined in `DEFAULTS`)
OCEAN_VERSIONS = {
    None}.union(get_version(ocean_version_info, n+1) for n in range(len(ocean_version_info)))
PYTHON_VERSIONS = {
    None, 'python3.8', 'python3.9', 'python3.10'}
PLATFORM_NAMES = {
    None, 'bullseye', 'slim'}

DEFAULTS = dict(
    platform='bullseye', ocean=OCEAN_VERSION, python='python3.9')


def get_canonical_subtag(name, value):
    """Return canonical tag value for component `name`."""

    if value is None:
        return DEFAULTS[name]

    if name == 'ocean':
        if OCEAN_VERSION.startswith(value):
            return OCEAN_VERSION
        # TODO: to resolve any ocean version to canonical (full spec), we need all versions released
        raise ValueError("Unable to resolve Ocean version other than one under build.")

    return value


def get_tag(default_tag='latest', **subtags):
    # `subtags` key order matters! use: (ocean, python, platform)
    nonempty_subtags = list(filter(None, subtags.values()))
    if nonempty_subtags:
        tag = '-'.join(nonempty_subtags)
    else:
        tag = default_tag

    # derive canonical tag (`tag` can be an alias)
    canonical_subtags = (get_canonical_subtag(k, v) for k, v in subtags.items())
    canonical_tag = '-'.join(canonical_subtags)

    return tag, canonical_tag


tagbag = defaultdict(set)   # Dict[str, Set[str]]

for oc,py,pl in product(OCEAN_VERSIONS, PYTHON_VERSIONS, PLATFORM_NAMES):
    tag, canonical = get_tag(ocean=oc, python=py, platform=pl)
    tagbag[canonical].add(tag)

all_tags = set(tagbag.keys()).union(*tagbag.values())

print(f"===\nmatrix\n===\n"
      f"- ocean: {', '.join(filter(None, OCEAN_VERSIONS))}\n"
      f"- python: {', '.join(filter(None, PYTHON_VERSIONS))}\n"
      f"- platform: {', '.join(filter(None, PLATFORM_NAMES))}\n")

print("===\ncanonical images/tags:", len(tagbag), '\n===')
for canonical, aliases in tagbag.items():
    print(f'{canonical}:\n  {", ".join(sorted(aliases.difference(canonical)))}\n')

print(f"===\nall tags: {len(all_tags)}\n===")
for tag in sorted(all_tags):
    print(tag)
