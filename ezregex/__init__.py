#!/usr/bin/env python3
""" A readable and intuitive way to generate Regular Expressions """
__version__ = '3.1.3'

# Import this as a submodule
from . import generate
from .api import api
from .EZRegex import EZRegex
from .generate import generate_regex
from .invert import invert
from .psuedonyms import psuedonyms as _psuedonyms, all_psuedonyms as _all_psuedonyms

from . import python
from . import javascript
from . import r
from . import pcre2

# Python is the default
from .python import *
