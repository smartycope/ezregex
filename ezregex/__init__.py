#!/usr/bin/env python3
__version__ = '1.5.0'
from .invert import invert
from .EZRegexMember import EZRegexMember
from .elements import *
from .psuedonymns import *
from re import RegexFlag, escape
from . import _docs

__groups__ = {
    "positionals": (
        "stringStartsWith",
        "stringEndsWith",
        "lineStartsWith",
        "lineEndsWith",
    ),
    "literals": (
        "spaceOrTab",
        "newLine",
        "carriageReturn",
        "tab",
        "space",
        "quote",
        "verticalTab",
        "formFeed",
        "comma",
        "period",
    ),
    "notLiterals": (
        "notWhitespace",
        "notDigit",
        "notWord",
    ),
    "groups": (
        "whitespace",
        "whitechunk",
        "digit",
        "letter",
        "number",
        "word",
        "wordChar",
        "anything",
        "chunk",
        "uppercase",
        "lowercase",
        "hexDigit",
        "octDigit",
        "punctuation",
        "controller",
        "printable",
        "printableAndSpace",
        "alphaNum",
        "unicode",
    ),
    "replacement": (
        "rgroup",
        "replaceEntire",
    ),
    "amounts": (
        "matchMax",
        "matchNum",
        "matchMoreThan",
        "matchAtLeast",
        "matchAtMost",
        "matchRange",
        "optional",
        "atLeastOne",
        "atLeastNone",
    ),
    "choices": (
        "either",
        "anyBetween",
        "anyOf",
        "anyCharExcept",
        "anyExcept",
    ),
    "conditionals": (
        "ifProceededBy",
        "ifNotProceededBy",
        "ifPrecededBy",
        "ifNotPreceededBy",
        "ifEnclosedWith",
    ),
    "grouping": (
        "group",
        "passiveGroup",
        "namedGroup",
    ),
    "combonations": (
        "literallyAnything",
        "signed",
        "unsigned",
        "plain_float",
        "full_float",
        "int_or_float",
        "ow",
        "email",
    ),
    "misc": (
        "literal",
        "isExactly",
        "raw",
    ),
    "flags": (
        "ASCII",
        "DOTALL",
        "IGNORECASE",
        "LOCALE",
        "MULTILINE",
        "UNICODE",
    ),
}

__all__ = sum([elems for elems in __groups__.values()], start=tuple())
