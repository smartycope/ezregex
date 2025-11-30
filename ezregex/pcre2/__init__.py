from .PCRE2EZRegex import PCRE2EZRegex
from ..inject_parts import inject_parts

globals().update(inject_parts(PCRE2EZRegex))
