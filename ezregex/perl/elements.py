#!/usr/bin/env python3
from ..EZRegex import EZRegex
from sys import version_info
from re import RegexFlag, escape
from warnings import warn

# This also imports all the psuedonymns from the python submodule as well
from ..python import *

def earlierGroup(num_or_name):
    """ Matches whatever the group referenced by `num_or_name` matched earlier. Must be *after* a
    group which would match `num_or_name`. """
    if isinstance(num_or_name, int) or num_or_name in '0123456789':
        return EZRegex(lambda num_or_name, cur=...: rf'{cur}\\{num_or_name}')(num_or_name)
    else:
        return EZRegex(lambda num_or_name, cur=...: rf'{cur}(\g<{num_or_name}>)')(num_or_name)

# I'm not sure this will still work under Perl
del email
