# pyright: reportArgumentType = false
# pyright: reportUndefinedVariable = false
from ..base import load_base
from ..EZRegex import EZRegex
from .REZRegex import REZRegex

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

del ASCII
del DOTALL
del IGNORECASE
del LOCALE
del MULTILINE
del UNICODE

# Matches any single character except line break characters, like the dot, but is not affected by any options that make the dot match all characters including line breaks.
not_newline = REZRegex(r'\N')
