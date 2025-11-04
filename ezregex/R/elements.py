# pyright: reportArgumentType = false
# pyright: reportUndefinedVariable = false
from ..base import load_base, _parse_any_of_params, not_empty
from ..EZRegex import EZRegex
from .REZRegex import REZRegex
from string import Formatter

# As far as I can tell, this is the docs for this syntax:
# https://www.rdocumentation.org/packages/base/versions/3.6.2/topics/regex

globals().update(load_base(REZRegex, lambda num_or_name, cur=...: fr'{cur}\g{{{num_or_name}}}'))

# I can't figure out how flags work in R, so I'm just ignoring them
del line_starts_with
del lineStartsWith
del line_start
del lineStart
del line_ends_with
del lineEndsWith
del line_end
del lineEnd

del if_proceded_by
del ifProcededBy
del if_not_proceded_by
del ifNotProcededBy
del if_preceded_by
del ifPrecededBy
del if_not_preceded_by
del ifNotPrecededBy
del if_enclosed_with
del ifEnclosedWith

del exactly
del is_exactly
del isExactly

del earlier_group
del earlierGroup

punctuation = REZRegex(r'[' + REZRegex.escape(']`~!@#$%^&*()-_=+[{}\\|;:\'",<.>/?') + r']')

def _any_of(*inputs, chars=None, split=None, cur=...):
    chars, inputs = _parse_any_of_params(*inputs, chars=chars, split=split)

    if chars:
        if ']' in inputs:
            # You can't escape ] in an R character class, it has to be first
            inputs.remove(']')
            inputs.insert(0, ']')
        cur += r'['
        for i in inputs:
            cur += i
        cur += r']'
    else:
        cur += r'(?:'
        for i in inputs:
            cur += i
            cur += '|'
        cur = cur[:-1]
        cur += r')'
    return cur
any_of = anyOf = REZRegex(_any_of)

chunk = REZRegex(r'[^\n]+')

# Matches any single character except line break characters, like the dot, but is not affected by any options that make the dot match all characters including line breaks.
not_newline = REZRegex(r'\N')

def _group(input, name=None, cur=...):
    not_empty(input, 'group')
    if name is not None:
        raise ValueError('Named groups are not supported in R')
    return f'{cur}({input})'
group = REZRegex(_group)


def _rgroup(num, cur=...):
    return f'{cur}\\{num}'

# TODO: this probably doesn't all need to be here
def replace(string, rtn_str=True):
    class CustomFormatter(Formatter):
        def get_value(self, key, args, kwargs):
            return _rgroup(key, '')

    string = CustomFormatter().format(string)

    return string if rtn_str else REZRegex(string, sanatize=False, replacement=True)

rgroup = replace_group = REZRegex(_rgroup, replacement=True)
replace_entire = REZRegex('\\0', replacement=True)

def options(*args, **kwargs):
    raise ValueError('Flags are not supported in R dialect')