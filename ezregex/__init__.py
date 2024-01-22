#!/usr/bin/env python3
""" A readable and intuitive way to generate Regular Expressions """
__version__ = '1.6.3'

from .invert import invert
from .EZRegex import EZRegex
from .python import *
# We have to import these manually cause they start with __
from .python import __docs__, __groups__
from re import RegexFlag, escape
