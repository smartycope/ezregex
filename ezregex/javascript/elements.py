# pyright: reportArgumentType = false
# pyright: reportUndefinedVariable = false
import re
from json import load

from ..base import load_base
from ..EZRegex import EZRegex

globals().update(load_base('javascript'))

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
    return string if rtn_str else EZRegex(string, 'javascript', sanatize=False, replacement=True)

rgroup = EZRegex(lambda num_or_name, cur=...: fr'{cur}\g<{num_or_name}>', 'javascript', replacement=True)
replace_entire = EZRegex(lambda cur=...: cur + r'\g<0>', 'javascript', replacement=True)

ctrl_char = EZRegex(lambda char, cur=...: cur + r'\c' + char)
ascii_char = EZRegex(lambda octal, cur=...: cur + r'\\' + octal)

# TODO: There's probably a way to do this by hand
del line_starts_with
del line_ends_with
# string_starts_with = EZRegex(lambda input='', cur=...: r'\A' + input + cur},
# string_ends_with = EZRegex(lambda input='', cur=...: input + r'\Z' + cur},
