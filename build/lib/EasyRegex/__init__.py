#!/usr/bin/env python3
""" EasyRegex
An readable and intuitive way to generate Regular Expressions
"""
__version__ = '2.4.2'
__author__ = 'Copeland Carter'
__email__ = 'smartycope@gmail.com'
__license__ = 'GPL 3.0'
__copyright__ = '(c) 2021, Copeland Carter'


from .EasyRegexSingleton import EasyRegexSingleton
from .invert import invertRegex, testInvertRegex
# from .tests import *

# print('EasyRegex Loaded')

#* All the singletons
# Positional
# wordStartsWith = EasyRegexSingleton(lambda cur, input: input + r'\<' + cur)
# wordEndsWith   = EasyRegexSingleton(lambda cur, input: cur   + r'\>' + input)
startsWith     = EasyRegexSingleton(lambda cur, input: input + r'\A' + cur)
endsWith       = EasyRegexSingleton(lambda cur, input: cur   + r'\z' + input)
# ifAtBeginning  = EasyRegexSingleton(lambda cur: r'^' + cur)
# ifAtEnd        = EasyRegexSingleton(r'$')
# Matching
match     = EasyRegexSingleton(lambda cur, input: cur + input)
isExactly = exactly = EasyRegexSingleton(lambda cur, input: "^" + input + '$')
# Not sure how to implement these, I don't have enough experience with Regex
# \b       Matches the empty string, but only at the start or end of a word.
# \B       Matches the empty string, but not at the start or end of a word.

# Amounts
matchMax      = EasyRegexSingleton(lambda cur,      input='':      cur + ('' if not len(input) else r'(?:' + input + r')') + r'+')
matchNum      = EasyRegexSingleton(lambda cur, num, input='':      cur + ('' if not len(input) else r'(?:' + input + r')') + r'{' + str(num) + r'}')
matchRange    = EasyRegexSingleton(lambda cur, min, max, input='': cur + ('' if not len(input) else r'(?:' + input + r')') + r'{' + str(min) + r',' + str(max) + r'}')
matchMoreThan = EasyRegexSingleton(lambda cur, min, input='':      cur + ('' if not len(input) else r'(?:' + input + r')') + r'{' + str(min - 1) + r',}')
matchAtLeast  = EasyRegexSingleton(lambda cur, min, input='':      cur + ('' if not len(input) else r'(?:' + input + r')') + r'{' + str(min) + r',}')

# Single Characters
whitespace = EasyRegexSingleton(r'\s')
whitechunk = EasyRegexSingleton(r'\s+')
digit      = EasyRegexSingleton(r'\d')
number     = EasyRegexSingleton(r'\d+')
word       = EasyRegexSingleton(r'\w+')
wordChar   = EasyRegexSingleton(r'\w')
hexDigit   = EasyRegexSingleton(r'\x')
octDigit   = EasyRegexSingleton(r'\O')
anything   = EasyRegexSingleton(r'.')
chunk      = EasyRegexSingleton(r'.+')
stuff      = chunk
whiteChunk = whitechunk
anychar    = anything
anyChar    = anything

# Explicit Characters
spaceOrTab     = EasyRegexSingleton(r'[ \t]')
newLine        = EasyRegexSingleton(r'\n')
carriageReturn = EasyRegexSingleton(r'\r')
tab            = EasyRegexSingleton(r'\t')
space          = EasyRegexSingleton(r' ')
quote          = EasyRegexSingleton(r'(?:\'|")')
verticalTab    = EasyRegexSingleton(r'\v')
formFeed       = EasyRegexSingleton(r'\f')
comma          = EasyRegexSingleton(r'\,')
period = dot   = EasyRegexSingleton(r'\.')
newline = newLine

# Not Chuncks
notWhitespace = EasyRegexSingleton(r'\S')
notDigit      = EasyRegexSingleton(r'\D')
notWord       = EasyRegexSingleton(r'\W')

# Optionals
optional      = EasyRegexSingleton(lambda cur, input='': cur + (fr'(?:{input})?' if len(input) > 1 else (fr'{input}?' if len(input) == 1 else '')))
multiOptional = EasyRegexSingleton(lambda cur, input='': cur + (fr'(?:{input})*' if len(input) > 1 else (fr'{input}*' if len(input) == 1 else '')))
either        = EasyRegexSingleton(lambda cur, input, or_input: cur + rf'(?:{input}|{or_input})')
anyBetween    = EasyRegexSingleton(lambda cur, input, and_input: cur + r'[' + input + r'-' + and_input + r']')
anyAmount     = multiOptional

def _anyCharsFunc(cur, *inputs):
    cur += r'['
    for i in inputs:
        cur += i
    cur += r']'
    return cur
anyChars = EasyRegexSingleton(_anyCharsFunc)

def _anyOfFunc(cur, *inputs):
    cur += r'(?:'
    for i in inputs:
        cur += i
        cur += '|'
    cur = cur[:-1]
    cur += r')'
    return cur
anyOf = anyof = EasyRegexSingleton(_anyOfFunc)

def _anyCharExceptFunc(cur, *inputs):
    cur += r'[^'
    for i in inputs:
        cur += i
    cur += r']'
    return cur
anyCharExcept  = EasyRegexSingleton(_anyCharExceptFunc)

def _anyExceptFunc(cur, *inputs):
    raise NotImplementedError('I am as yet unsure how to implement anyExcept. Maybe try using either anyCharExcept, which does work, or something like this: (?:(?!sequence).)+')
    # cur += r'(?:'
    # for i in inputs:
    #     cur += i
    #     cur += '|'
    # cur = cur[:-1]
    # cur += r')'
    return cur
anyExcept = EasyRegexSingleton(_anyExceptFunc)


# Sets
anyUppercase       = EasyRegexSingleton(r'[A-Z]')
anyLowercase       = EasyRegexSingleton(r'[a-z]')
anyLetter          = EasyRegexSingleton(r'[A-Za-z]')
anyAlphaNum        = EasyRegexSingleton(r'[A-Za-z0-9]')
anyDigit           = EasyRegexSingleton(r'[0-9]')
anyHexDigit        = EasyRegexSingleton(r'[0-9a-fA-F]')
anyOctDigit        = EasyRegexSingleton(r'[0-7]')
anyPunctuation     = EasyRegexSingleton(r'[:punct:]')
anyBlank           = EasyRegexSingleton(r'[ \t\r\n\v\f]')
anyControllers     = EasyRegexSingleton(r'[\x00-\x1F\x7F]')
anyPrinted         = EasyRegexSingleton(r'[\x21-\x7E]')
anyPrintedAndSpace = EasyRegexSingleton(r'[\x20-\x7E]')
anyAlphaNum_       = EasyRegexSingleton(r'[A-Za-z0-9_]')

# Numbers
octalNum = EasyRegexSingleton(lambda cur, num: cur + r'\\' + num)
hexNum   = EasyRegexSingleton(lambda cur, num: cur + r'\x' + num)

# Conditionals
ifProceededBy    = EasyRegexSingleton(lambda cur, condition: fr'{cur}(?={condition})')
ifNotProceededBy = EasyRegexSingleton(lambda cur, condition: fr'{cur}(?!{condition})')
ifPrecededBy     = EasyRegexSingleton(lambda cur, condition: fr'(?<={condition}){cur}')
ifNotPrecededBy  = EasyRegexSingleton(lambda cur, condition: fr'(?<!{condition}){cur}')
ifEnclosedWith   = EasyRegexSingleton(lambda cur, open, stuff, close: fr'((?<={open}){stuff}(?={close}))')
ifFollowedBy     = ifProceededBy
ifNotFollowedBy  = ifNotProceededBy


# Groups
# I don't understand these.
# (?aiLmsux) The letters set the corresponding flags defined below.
# \number  Matches the contents of the group of the same number.
group          = EasyRegexSingleton(lambda cur, chain: f'{cur}({chain})')
passiveGroup   = EasyRegexSingleton(lambda cur, chain: f'{cur}(?:{chain})')
namedGroup     = EasyRegexSingleton(lambda cur, name, chain: f'{cur}(?P<{name}>{chain})')
# referenceGroup = EasyRegexSingleton(lambda cur, name:        f'{cur}(?P={name})')

# TODO figure this out and add it
# Replace Syntax
# Use these on the replacement end to reference groups specified in the original regex
replaceGroup          = EasyRegexSingleton(lambda cur, num:  f'{cur}\\g<{num}>')
# replaceNamedGroup     = EasyRegexSingleton(lambda cur, name: f'{cur}?P={name})')
replaceNamedGroup     = replaceGroup

# # I don't think this inverse is correct
# notGroup       = EasyRegexSingleton(lambda cur, chain: f'{cur}(?:{chain})',
#                                     lambda cur, chain: cur + chain)

# namedGroup     = EasyRegexSingleton(lambda cur, name, chain: f'{cur}(?P {name} {chain})')
# referenceGroup = EasyRegexSingleton(lambda cur, name:        f'{cur}(?P={name})')

# For adding raw regex statements without sanatizing them
raw = EasyRegexSingleton(lambda cur, regex: str(regex), sanatize=False)


# TODO Implement Dialects
# Global Flags -- I don't think these will work
matchGlobally     = EasyRegexSingleton(r'//g')
caseInsensitive   = EasyRegexSingleton(r'//i')
matchMultiLine    = EasyRegexSingleton(r'//m')
treatAsSingleLine = EasyRegexSingleton(r'//s')
notGreedy         = EasyRegexSingleton(r'//U')
