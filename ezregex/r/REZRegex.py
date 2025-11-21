""" Support for the R dialect of regular expressions"""
__version__ = '1.1.0'

import re
from .. import EZRegex
from ..mixins import (BaseMixin, AssertionsMixin, GroupsMixin, AnchorsMixin, ReplacementsMixin, _parse_any_of_params)
from ..flag_docs import common_flag_docs
from ..inject_parts import inject_parts

class REZRegex(
    BaseMixin(allow_greedy=False, allow_possessive=False),
    GroupsMixin(
        advanced=False,
        named_group=None,
    ),
    AnchorsMixin(string=False),
    ReplacementsMixin(
        advanced=False,
        numbered_group=lambda num, cur=...: fr'{cur}\{num}',
        named_group=None,
    ),
    EZRegex,

    escape_chars=b'|()[{^$*+?.-',
    flags={},
    flags_docs_map={},
):
    """
    Official docs:
    https://www.rdocumentation.org/packages/base/versions/3.6.2/topics/regex
    """

    def _final_func(self, s:str) -> str:
        # Double escape all backslashes
        s = s.replace('\\', '\\\\')
        # Things which are control characters should *not* be double escaped
        s = re.sub(r'\\\\([abtnvfrxuU])', r'\\\g<1>', s)
        return s

    punctuation = r'[]`~!@#\$%^&\*\(\)\-_=\+[\{}\\\|;:\'",<\.>/\?]'

    def any_of(*inputs, chars=None, split=None, cur=...):
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

    # For some reason \N doesn't seem to work? It doesn't matter that much
    chunk = r'[^\n]+'

    # Matches any single character except line break characters, like the dot, but is not affected by any options that make the dot match all characters including line breaks.
    not_newline = r'\N'

    # def options(*args, **kwargs):
    #     raise ValueError('Flags are not supported in R dialect')

globals().update(inject_parts(REZRegex))
