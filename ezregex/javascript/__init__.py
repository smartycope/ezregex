from .JavascriptEZRegex import JavascriptEZRegex
from ..inject_parts import inject_parts

globals().update(inject_parts(JavascriptEZRegex))
