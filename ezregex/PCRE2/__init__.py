""" Support for the PCRE2 dialect of regular expressions"""
__version__ = '1.1.0'

from ..EZRegex import EZRegex
from ..mixins import (BaseMixin, AssertionsMixin, GroupsMixin, AnchorsMixin, ReplacementsMixin)
from ..flag_docs import common_flag_docs

class PCRE2EZRegex(
    BaseMixin(allow_greedy=True, allow_possessive=True),
    AssertionsMixin(),
    GroupsMixin(advanced=True),
    AnchorsMixin(string=False),
    BasicGroupsMixin(),
    ReplacementsMixin(
        advanced=True,
        entire_match='$&',
    ),
    EZRegex,
    _escape_chars=b'()[]{}?*+-|^$\\.&~# \t\n\r\v\f',
    _repl_escape_chars=b'$',
    flags={
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
    flags_docs_map={
        **common_flag_docs,
        'noncapturing': '''Not recomendded. Don't capture with any groups. Instead, simply don't use any groups''',
        'extra': '''Not recomendded. Any character following a \\ that is not a valid meta sequence \
will be faulted and raise an error. \\O, for example, will cause an \
error, and it will not match.'''
    }
):
    """
    Official docs:
    https://www.pcre.org/current/doc/html/pcre2syntax.html
    https://www.pcre.org/current/doc/html/pcre2pattern.html
    """
    def _final_func(self, s:str) -> str:
        if self.replacement:
            # This is how you escape a $ in a replacement string
            return s.replace(r'\$', '$$')
        return s

