from .REZRegex import REZRegex
from ..inject_parts import inject_parts

globals().update(inject_parts(REZRegex))
