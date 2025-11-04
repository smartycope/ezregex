# pyright: reportArgumentType = false
# pyright: reportUndefinedVariable = false
from ..base import load_base, not_empty, _generate_options_from_flags
from ..EZRegex import EZRegex
from .JavaScriptEZRegex import JavaScriptEZRegex
from string import digits, Formatter

globals().update(load_base(JavaScriptEZRegex, lambda num_or_name, cur=...: fr'{cur}\k<{num_or_name}>'))

exactly = is_exactly = isExactly = JavaScriptEZRegex(lambda input, cur=...: r"^" + input + r"$")

def _group(input, name=None, cur=...):
    not_empty(input, 'group')
    if name is not None:
        not_empty(name, 'group', 'name')
    return f'{cur}({input})' if name is None else f'{cur}(?<{name}>{input})'

group = JavaScriptEZRegex(_group)

def _earlier_group(num_or_name, cur=...):
    not_empty(num_or_name, 'earlier_group', num_or_name)
    return fr'{cur}\{num_or_name}' if isinstance(num_or_name, int) or num_or_name in digits else fr'{cur}\k<{num_or_name}>'

earlier_group = earlierGroup = JavaScriptEZRegex(_earlier_group)

string_starts_with = string_start = stringStart = stringStartsWith = JavaScriptEZRegex(lambda input='', cur=...: r'^' + input + cur, string_anchor_used=True)
string_ends_with = string_end = stringEnd = stringEndsWith = JavaScriptEZRegex(lambda input='', cur=...: cur + input + r'$', string_anchor_used=True)

del ifExists
del if_exists

def _rgroup(num_or_name, cur=...):
    return fr'{cur}${num_or_name}' if isinstance(num_or_name, int) or num_or_name in digits else fr'{cur}$<{num_or_name}>'

# TODO: this probably doesn't all need to be here
def replace(string, rtn_str=True):
    class CustomFormatter(Formatter):
        def get_value(self, key, args, kwargs):
            return _rgroup(key, '')

    string = CustomFormatter().format(string)

    return string if rtn_str else JavaScriptEZRegex(string, sanatize=False, replacement=True)

rgroup = replace_group = JavaScriptEZRegex(_rgroup, replacement=True)
replace_entire = JavaScriptEZRegex('$&', replacement=True)

options = _generate_options_from_flags(
    JavaScriptEZRegex,
    {'global': 'g', 'has_indicies': 'd', 'multiline': 'm', 'ignore_case': 'i',
     'single_line': 's', 'unicode': 'u', 'sticky': 'y'},
    docs_map={
        'has_indicies': '''Generate indices for substring matches''',
        'sticky': '''The pattern is forced to become anchored at the start of the search or at the position of the last successful match, equivalent to a \G''',
    },
    docs_link='https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions#advanced_searching_with_flags'
)
