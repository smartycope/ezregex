#!/usr/bin/env python3
__version__ = '1.5.1'
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
        "tab",
        "space",
        "spaceOrTab",
        "newline",
        "carriageReturn",
        "quote",
        "verticalTab",
        "formFeed",
        "comma",
        "period",
    ),
    "not literals": (
        "notWhitespace",
        "notDigit",
        "notWord",
    ),
    "catagories": (
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
        "anyBetween",
    ),
    "amounts": (
        "matchMax",
        "amt",
        "moreThan",
        "matchRange",
        "atLeast",
        "atMost",
        "atLeastOne",
        "atLeastNone",
    ),
    "choices": (
        "optional",
        "either",
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
    "replacement": (
        "rgroup",
        "replaceEntire",
    ),
    "premade": (
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

# We *dont* want to do this, actually, cause then it won't import all our psuedonymns
# __all__ = sum([elems for elems in __groups__.values()], start=tuple())
