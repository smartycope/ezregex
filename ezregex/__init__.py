#!/usr/bin/env python3
""" A readable and intuitive way to generate Regular Expressions """
__version__ = '2.2.0'

# Import this as a submodule
from . import generate
from .api import api
from .EZRegex import EZRegex
from .generate import generate_regex
from .invert import invert
from .python import *
