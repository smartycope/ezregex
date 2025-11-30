from .PythonEZRegex import PythonEZRegex
from ..inject_parts import inject_parts

globals().update(inject_parts(PythonEZRegex))
