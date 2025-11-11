#!/usr/bin/env python3
""" Support for the Python dialect of regular expressions"""
__version__ = '2.1.0'

import re
import sys

from .. import EZRegex
from ..mixins import (BaseMixin, AssertionsMixin, GroupsMixin, AnchorsMixin, ReplacementsMixin)
from ..flag_docs import common_flag_docs
from sys import version_info

# TODO: make all the flag functions here also accept re.FLAG types (internally they should work the same though)

class PythonEZRegex(
    BaseMixin(allow_greedy=True, allow_possessive=version_info >= (3, 11)),
    AssertionsMixin(),
    GroupsMixin(advanced=True),
    # only 3.14+ has support for \z
    AnchorsMixin(word=False, string_end=r'\Z'),
    ReplacementsMixin(
        advanced=False,
        named_group=lambda name, cur=...: fr'{cur}\g<{name}>',
        numbered_group=lambda num, cur=...: fr'{cur}\g<{num}>'
    ),
    EZRegex,

    escape_chars=b'()[]{}?*+-|^$\\.&~# \t\n\r\v\f',
    flags={
        'ascii': 'a',
        'ignore_case': 'i',
        'single_line': 's',
        'locale': 'L',
        'multiline': 'm',
        'unicode': 'u'
    },
    flags_docs_map={**common_flag_docs, 'locale': '''Try not to use this, and rely on unicode matching instead'''},
    flags_docs_link='https://docs.python.org/3/library/re.html#flags',

    # If we try to combine it with something, invalidate the cache
    variables={
        '_compiled': (None, lambda l, r: None),
    }
):
    """
    Official docs:
    https://docs.python.org/3/library/re.html
    """

    # TODO: rewrite these using existing elements, and put them in a premade mixin, so they can be generic
    # Source: http://stackoverflow.com/questions/201323/ddg#201378
    email = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    "Matches an email"
    # Source: https://semver.org/ (at the bottom)
    version = r"(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?"
    """The *official* regex for matching version numbers from https://semver.org/. It includes 5 groups that can be
    matched/replaced: `major`, `minor`, `patch`, `prerelease`, and `buildmetadata`"""
    version_numbered = r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?"
    "Same as `version`, but it uses numbered groups for each version number instead of named groups"

    # Just for compatibility with previous python verions
    is_exactly = lambda s: fr'\A{s}\Z'

    @EZRegex.exclude
    def compile(self, add_flags=True):
        return re.compile(self._compile(add_flags))

    @property
    @EZRegex.exclude
    def compiled(self):
        if self._compiled is None:
            self.__dict__['_compiled'] = self.compile()
        return self._compiled

    # Shadowing the re functions
    @EZRegex.exclude
    def search(self, string, pos=0, endpos=sys.maxsize):
        return self.compile().search(string, pos, endpos)

    @EZRegex.exclude
    def match(self, string, pos=0, endpos=sys.maxsize):
        return self.compile().match(string, pos, endpos)

    @EZRegex.exclude
    def fullmatch(self, string, pos=0, endpos=sys.maxsize):
        return self.compile().fullmatch(string, pos, endpos)

    @EZRegex.exclude
    def split(self, string, maxsplit=0):
        return self.compile().split(string, maxsplit)

    @EZRegex.exclude
    def findall(self, string, pos=0, endpos=sys.maxsize):
        return self.compile().findall(string, pos, endpos)

    @EZRegex.exclude
    def finditer(self, string, pos=0, endpos=sys.maxsize):
        return self.compile().finditer(string, pos, endpos)

    @EZRegex.exclude
    def sub(self, repl, string, count=0):
        return self.compile().sub(repl, string, count)

    @EZRegex.exclude
    def subn(self, repl, string, count=0):
        return self.compile().subn(repl, string, count)

for i in PythonEZRegex.parts():
    globals()[i] = getattr(PythonEZRegex, i)