"""
Take a version as an argument and a list of versions on stdin.
Spits out what docker tags should be applied to the build.

Notes on semver handling.
 - buildmetadata is stripped and ignored. See  https://semver.org/spec/v2.0.0.html#spec-item-10
"""
import sys
from typing import List
import re


def semverparse(ver: str) -> (int, int, int, str, str):
    """Parse a semver string into components. Accepts:
      1) Complete semver string
      2) Partial version string (0 or 0.1)

      Returns a
    """
    # 1.2.3-snapshot-20201212.137+build11
    major, minor, patch, prerelease, buildmetadata = (None, None, None, None, None)
    # match = re.match(r'^(\d+)(?:\.(\d+))?(?:\.(\d+))?$', ver)
    # Adapted from semver.org
    match = re.match(
        r'^(?P<major>0|[1-9]\d*)(?:\.(?P<minor>0|[1-9]\d*))?(?:\.(?P<patch>0|[1-9]\d*))?(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$',
        ver)
    if match:
        major = int(match.group('major'))
        if match.group('minor') is not None:
            minor = int(match.group('minor'))
            if match.group('patch') is not None:
                patch = int(match.group('patch'))
                if match.group('prerelease'):
                    prerelease = match.group('prerelease')
                if match.group('buildmetadata'):
                    buildmetadata = match.group('buildmetadata')
    else:
        raise ValueError(f"Invalid version string '{ver}' (regex did not match)")

    return major, minor, patch, prerelease, buildmetadata


def get_new_tags(newversion, existing_verions) -> List[str]:
    """
    Taka a version (newversion) and return the relevant tags we should set on this:

    So for the following:
    0.1.0, 0.2.0, 0.3.0

    If we get 0.2.1 we should set the following:
     0.2.1, 0.2
     Not 0 as 0.3.0 should point to 0 and 0.3

    Rules for return values:
     * always return the full (1.2.3)
     * always return major.minor (1.2)
     * if we're the highest minor in the major version we're on then we return the major as well (1)
     * if the major doesn't exists return the major (1)
    """
    major, minor, patch, prerelease, buildmetadata = newversion
    if prerelease is not None:
        prerelease = '-' + newversion[3]
    else:
        prerelease = ''
    if (major, minor, patch) in existing_verions:
        raise ValueError("Version already exists")

    tags = []

    tags.append(f"{major}.{minor}.{patch}{prerelease}")
    tags.append(f"{major}.{minor}{prerelease}")

    majors = [ver[0] for ver in existing_verions]
    our_minors = [ver[1] for ver in existing_verions if ver[1] != None and ver[0] == major]
    if major not in majors:
        tags.append(f"{major}{prerelease}")
    elif max(our_minors) <= minor:
        tags.append(f"{major}{prerelease}")
    return tags

def main():

    existing_versions = []
    for line in sys.stdin:
         existing_versions.append(semverparse(line.rstrip()))
    new_ver = semverparse(sys.argv[1])
    print(" ".join(get_new_tags(new_ver, existing_versions)))

if __name__ == '__main__':
    main()