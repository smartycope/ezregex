#!/usr/bin/env python3
""" A readable and intuitive way to generate Regular Expressions """
__version__ = '2.2.1'

# Import this as a submodule
from . import generate
from .api import api
from .EZRegex import EZRegex
from .generate import generate_regex
from .invert import invert
# Python is the default
from .python import *
from . import R
from . import javascript
from . import perl
