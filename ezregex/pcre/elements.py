# pyright: reportArgumentType = false
# pyright: reportUndefinedVariable = false
from ..base import load_base
from ..EZRegex import EZRegex
from .PCREZRegex import PCREZRegex

globals().update(load_base(PCREZRegex, lambda num_or_name, cur=...: fr'{cur}\g<{num_or_name}>'))
