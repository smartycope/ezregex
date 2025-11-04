# pyright: reportArgumentType = false
# pyright: reportUndefinedVariable = false
from ..base import load_base
from ..EZRegex import EZRegex
from .PCRE2EZRegex import PCRE2EZRegex

globals().update(load_base(PCRE2EZRegex, lambda num_or_name, cur=...: fr'{cur}${{{num_or_name}}}'))

# we want *lowercase* \z, not \Z
is_exactly = isExactly = lambda s: fr'\A{s}\z'