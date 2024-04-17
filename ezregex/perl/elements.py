# pyright: reportArgumentType = false
# pyright: reportUndefinedVariable = false
from ..base import load_base
from ..EZRegex import EZRegex

globals().update(load_base('perl', lambda num_or_name, cur=...: fr'{cur}\g<{num_or_name}>'))
