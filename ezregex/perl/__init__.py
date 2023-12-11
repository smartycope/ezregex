#!/usr/bin/env python3
""" Support for the Perl dialect of regular expressions"""

from .elements import *
from .psuedonymns import *

from ..python import __docs__, __groups__

# These should all be the prefered psuedonymn, in camel case
# __groups__['positionals'] = __groups__['positionals'] + (<positionals>, <to>, <add>)


for element in sum([elems for elems in __groups__.values()], start=tuple()):
    if element not in __docs__ and str(type(globals()[element])) == "<class 'function'>":
        __docs__[element] = globals()[element].__doc__
