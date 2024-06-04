# pyright: reportArgumentType = false
# pyright: reportUndefinedVariable = false
# pyright: reportUndefinedVariable = false
from ..base import load_base
from ..EZRegex import EZRegex
from .JavaScriptEZRegex import JavaScriptEZRegex

globals().update(load_base(JavaScriptEZRegex, lambda num_or_name, cur=...: fr'{cur}\g<{num_or_name}>'))

ctrl_char = EZRegex(lambda char, cur=...: cur + r'\c' + char)
ascii_char = EZRegex(lambda octal, cur=...: cur + r'\\' + octal)

# TODO: There's probably a way to do this by hand
del line_starts_with
del line_ends_with
# string_starts_with = EZRegex(lambda input='', cur=...: r'\A' + input + cur},
# string_ends_with = EZRegex(lambda input='', cur=...: input + r'\Z' + cur},
