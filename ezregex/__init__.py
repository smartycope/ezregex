#!/usr/bin/env python3
""" A readable and intuitive way to generate Regular Expressions """

__version__ = '1.5.1'
from .invert import invert
from .EZRegexMember import EZRegexMember
from .elements import *
from .psuedonymns import *
from re import RegexFlag, escape

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

# We actually *dont* want to do this, actually, cause then it won't import all our psuedonymns
# __all__ = sum([elems for elems in __groups__.values()], start=tuple())

# This is not a typo. It's for connecting dynamically to ezregex.org
__docs__ = {
    "literallyAnything": "*Any* character, include newline",
    "signed":            "a signed number, including 123, -123, and +123",
    "unsigned":          "Same as number. Will not match +123",
    "plain_float":       "Will match 123.45 and 123.",
    "full_float":        "Will match plain_float as well as things like 1.23e-10 and 1.23e+10",
    "ow":                "\"Optional Whitechunk\"",
    "email":             "Matches an email",
    "whitechunk":        "A \"chunk\" of whitespace. Just any amount of whitespace together",
    "number":            "Matches multiple digits next to each other. Does not match negatives or decimals",
    "wordChar":          "Matches just a single \"word character\", defined as any letter, number, or _",
    "anything":          "Matches any single character, except a newline. To also match a newline, use literallyAnything",
    "chunk":             "A \"chunk\": Any clump of characters up until the next newline",
    "letter":            "Matches just a letter -- not numbers or _ like wordChar.",
    "controller":        "Matches a metadata ASCII characters",
    "printable":         "Matches printable ASCII characters",
    "unicode":           "Matches a unicode character by name",
    "replaceEntire":     "Puts in its place the entire match",
    "groups_docs": {
        'positionals': "These differentiate the *string* starting with a sequence, and a *line* starting with a sequence. Do note that the start of the string is also the start of a line. These can also be called without parameters to denote the start/end of a string/line without something specific having to be next to it.",
        'replacement': "In the intrest of \"I don't want to think about any syntax at all\", I have included replace members. Do note that they are not interoperable with the other EZRegexMembers, and can only be used with other strings and each other.",
        'misc':        "These shadow python regex flags, and can just as easily be specified directly to the re library instead. They're provided here for compatibility with other regex dialects. See https://docs.python.org/3/library/re.html#flags for details",
        'premade':     "These are some useful combinations that may be commonly used. They are not as stable, and may be changed and added to in later versions to make them more accurate"
    },
    "operator_docs": {
        "- `+`, `<<`, `>>`": "These all do the same thing: combine expressions",
        "`*`": "Multiplies an expression a number of times. `expr * 3` is equivelent to `expr + expr + expr`",
        "`+`": "A unary + operator acts exactly as a match_max() does, or, if you're familiar with regex syntax, the + operator",
        "`[]`": "expr[2, 3] is equivalent to `match_range(2, 3, expr)`\n\t- expr[2, ...] or expr[2,] is equivalent to `at_least(2, expr)`\n\t- expr[... , 2] is equivalent to `at_most(2, expr)`\n\t- expr[...] or expr[0, ...] is equivelent to `at_least_0(expr)`\n\t- expr[1, ...] is equivalent to `at_least_1(expr)`",
        "`&`": "Coming soon! This will work like the + operator, but they can be out of order. Like an and operation.",
        "`|`": "Coming soon! This will work like an or operation, which will work just like anyOf()",
    }
}

for element in sum([elems for elems in __groups__.values()], start=tuple()):
    if element not in __docs__ and str(type(globals()[element])) == "<class 'function'>":
        __docs__[element] = globals()[element].__doc__
