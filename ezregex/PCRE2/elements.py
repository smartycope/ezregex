# pyright: reportArgumentType = false
# pyright: reportUndefinedVariable = false
from ..base import load_base, _generate_options_from_flags
from ..EZRegex import EZRegex
from .PCRE2EZRegex import PCRE2EZRegex

# I think this the the official docs:
# https://www.pcre.org/current/doc/html/pcre2pattern.html

globals().update(load_base(PCRE2EZRegex, lambda num_or_name, cur=...: fr'{cur}${{{num_or_name}}}'))

# we want *lowercase* \z, not \Z
is_exactly = isExactly = lambda s: fr'\A{s}\z'

options = _generate_options_from_flags(
    PCRE2EZRegex,
    {
        'global': 'g',
        'multiline': 'm',
        'ignore_case': 'i',
        'verbose': 'x',
        'single_line': 's',
        #  'unicode': 'u',
        #  'extra': 'X',
        'lazy': 'U',
        #  'anchor': 'A',
        'duplicate_groups': 'J',
        'noncapturing': 'n'
    },
    docs_map={
        'noncapturing': '''Not recomendded. Don't capture with any groups. Instead, simply don't use any groups''',
        'extra': '''Not recomendded. Any character following a \\ that is not a valid meta sequence \
will be faulted and raise an error. \\O, for example, will cause an \
error, and it will not match.'''
    }
)
