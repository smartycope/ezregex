""" Support for the JavaScript dialect of regular expressions"""
__version__ = '1.1.0'

from .. import EZRegex
from ..mixins import (BaseMixin, AssertionsMixin, GroupsMixin, AnchorsMixin, ReplacementsMixin)
from ..flag_docs import common_flag_docs

class JavaScriptEZRegex(
    BaseMixin(allow_greedy=True, allow_possessive=True),
    AssertionsMixin(),
    GroupsMixin(
        advanced=True,
        named_group=lambda input, name, cur=...: f'{cur}(?<{name}>{input})',
        earlier_numbered_group=lambda num, cur=...: fr'{cur}\{num}',
        earlier_named_group=lambda name, cur=...: fr'{cur}\k<{name}>'
    ),
    AnchorsMixin(),
    ReplacementsMixin(
        advanced=False,
        entire_match='$&',
    ),
    EZRegex,

    escape_chars=b'()[]{}?*+-|^$\\.&~# \t\n\r\v\f/',
    flags={
        'global': 'g',
        'has_indicies': 'd',
        'multiline': 'm',
        'ignore_case': 'i',
        'single_line': 's',
        'unicode': 'u',
        'sticky': 'y'
    },
    flags_docs_map={
        **common_flag_docs,
        'has_indicies': '''Generate indices for substring matches''',
        'sticky': '''The pattern is forced to become anchored at the start of the search or at the position of the last successful match, equivalent to a \G''',
    },
    flags_docs_link='https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions#advanced_searching_with_flags',

    string_anchor_used=(True, lambda l, r: l or r),
):
    """
    Official docs:
    https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions
    """

    # We intentionally only add the // if we're adding flags
    # However, note that it will add // even if there are no flags
    def _flag_func(self, final):
        if self.string_anchor_used and 'm' in self.flags:
            raise ValueError('string_starts_with and string_ends_with don\'t work with the multiline flag')
        if self.replacement:
            return final
        return f'/{final}/{self.flags}'

    # TODO: test this to make sure I'm right to exclude cur from the output
    is_exactly = lambda input, cur=...: r"^" + input + r"$"

    del if_exists

    string_starts_with = lambda input='', cur=...: r'^' + input + cur, {'string_anchor_used': True}
    string_ends_with   = lambda input='', cur=...: cur + input + r'$', {'string_anchor_used': True}


for i in JavaScriptEZRegex.parts():
    globals()[i] = getattr(JavaScriptEZRegex, i)
