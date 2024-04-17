from ..base.interface import *

del UNICODE

"Group: Premade"
email: EZRegex
"Matches an email"
version: EZRegex
"""The *official* regex for matching version numbers from https://semver.org/. It includes 5 groups that can be
matched/replaced: `major`, `minor`, `patch`, `prerelease`, and `buildmetadata`
"""
version_numbered: EZRegex
"Same as `version`, but it uses numbered groups for each version number instead of named groups"
