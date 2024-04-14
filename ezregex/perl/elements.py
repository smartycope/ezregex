# pyright: reportArgumentType = false
import re
from json import load

from ..base import load_base
from ..EZRegex import EZRegex

globals().update(load_base('perl'))

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
    return string if rtn_str else EZRegex(string, 'perl', sanatize=False, replacement=True)

rgroup = EZRegex(lambda num_or_name, cur=...: fr'{cur}\g<{num_or_name}>', 'perl', replacement=True)
replace_entire = EZRegex(lambda cur=...: cur + r'\g<0>', 'perl', replacement=True)
