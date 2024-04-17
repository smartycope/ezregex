# pyright: reportArgumentType = false
import re
from json import load

from ..base import load_base
from ..EZRegex import EZRegex

globals().update(load_base('python'))

del UNICODE # type: ignore

# TODO: Use https://docs.python.org/3/library/string.html#string.Formatter instead
def replace(string, rtn_str=True):
    # Made with ezregex.org
    # Previous method
    # '{' + optional(anyCharExcept('{'), greedy=False) + group(+alphaNum) + '}' + optional(anyCharExcept('}'), greedy=False)
    # Current method
    # '{' + group(+alphaNum) + '}'
    r = r'\{((?:[A-Za-z0-9_])+)\}'
    # Convert them to something unique, then back, so we won't pick up things like {{this}}
    # {{this}} -> \0(this\0) -> {this}
    # instead of
    # {{this}} -> {this} -> \g<this>
    string = re.sub('{{', '\0\0(', string)
    string = re.sub('}}', '\0\0)', string)
    string = re.sub(r, r'\\g<\g<1>>', string)
    string = re.sub(r'\0\0\(', '{', string)
    string = re.sub(r'\0\0\)', '}', string)
    return string if rtn_str else EZRegex(string, 'python', sanatize=False, replacement=True)

rgroup = EZRegex(lambda num_or_name, cur=...: fr'{cur}\g<{num_or_name}>', 'python', replacement=True)
replace_entire = EZRegex(lambda cur=...: cur + r'\g<0>', 'python', replacement=True)

# Source: http://stackoverflow.com/questions/201323/ddg#201378
email = raw(r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])")
# Source: https://semver.org/ (at the bottom)
version = raw(r"(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?")
version_numbered = raw(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?")
