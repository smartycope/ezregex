#!/usr/bin/env python3
__version__ = '1.0.0'

from .EZRegexMember import EZRegexMember

# Positional
# wordStartsWith = EZRegexMember(lambda cur, input: input + r'\<' + cur)
# wordEndsWith   = EZRegexMember(lambda cur, input: cur   + r'\>' + input)
startsWith     = EZRegexMember(lambda cur, input: input + r'\A' + cur)
endsWith       = EZRegexMember(lambda cur, input: cur   + r'\z' + input)
# ifAtBeginning  = EZRegexMember(lambda cur: r'^' + cur)
# ifAtEnd        = EZRegexMember(r'$')
# Matching
match     = EZRegexMember(lambda cur, input: cur + input)
isExactly = exactly = EZRegexMember(lambda cur, input: "^" + input + '$')
# Not sure how to implement these, I don't have enough experience with Regex
# \b       Matches the empty string, but only at the start or end of a word.
# \B       Matches the empty string, but not at the start or end of a word.

# Amounts
matchMax      = EZRegexMember(lambda cur,      input='':      cur + ('' if not len(input) else r'(?:' + input + r')') + r'+')
matchNum      = EZRegexMember(lambda cur, num, input='':      cur + ('' if not len(input) else r'(?:' + input + r')') + r'{' + str(num) + r'}')
matchRange    = EZRegexMember(lambda cur, min, max, input='': cur + ('' if not len(input) else r'(?:' + input + r')') + r'{' + str(min) + r',' + str(max) + r'}')
matchMoreThan = EZRegexMember(lambda cur, min, input='':      cur + ('' if not len(input) else r'(?:' + input + r')') + r'{' + str(min - 1) + r',}')
matchAtLeast  = EZRegexMember(lambda cur, min, input='':      cur + ('' if not len(input) else r'(?:' + input + r')') + r'{' + str(min) + r',}')

# Single Characters
whitespace = EZRegexMember(r'\s')
whitechunk = EZRegexMember(r'\s+')
digit      = EZRegexMember(r'\d')
number     = EZRegexMember(r'\d+')
word       = EZRegexMember(r'\w+')
wordChar   = EZRegexMember(r'\w')
hexDigit   = EZRegexMember(r'\x')
octDigit   = EZRegexMember(r'\O')
anything   = EZRegexMember(r'.')
chunk      = EZRegexMember(r'.+')
stuff      = chunk
whiteChunk = whitechunk
anychar    = anything
anyChar    = anything

# Explicit Characters
spaceOrTab     = EZRegexMember(r'[ \t]')
newLine        = EZRegexMember(r'\n')
carriageReturn = EZRegexMember(r'\r')
tab            = EZRegexMember(r'\t')
space          = EZRegexMember(r' ')
quote          = EZRegexMember(r'(?:\'|")')
verticalTab    = EZRegexMember(r'\v')
formFeed       = EZRegexMember(r'\f')
comma          = EZRegexMember(r'\,')
period = dot   = EZRegexMember(r'\.')
newline = newLine

# Not Chuncks
notWhitespace = EZRegexMember(r'\S')
notDigit      = EZRegexMember(r'\D')
notWord       = EZRegexMember(r'\W')

# Optionals
optional      = EZRegexMember(lambda cur, input='': cur + (fr'(?:{input})?' if len(input) > 1 else (fr'{input}?' if len(input) == 1 else '')))
multiOptional = EZRegexMember(lambda cur, input='': cur + (fr'(?:{input})*' if len(input) > 1 else (fr'{input}*' if len(input) == 1 else '')))
either        = EZRegexMember(lambda cur, input, or_input: cur + rf'(?:{input}|{or_input})')
anyBetween    = EZRegexMember(lambda cur, input, and_input: cur + r'[' + input + r'-' + and_input + r']')
anyAmount     = multiOptional

def _anyCharsFunc(cur, *inputs):
    cur += r'['
    for i in inputs:
        cur += i
    cur += r']'
    return cur
anyChars = EZRegexMember(_anyCharsFunc)

def _anyOfFunc(cur, *inputs):
    cur += r'(?:'
    for i in inputs:
        cur += i
        cur += '|'
    cur = cur[:-1]
    cur += r')'
    return cur
anyOf = anyof = EZRegexMember(_anyOfFunc)

def _anyCharExceptFunc(cur, *inputs):
    cur += r'[^'
    for i in inputs:
        cur += i
    cur += r']'
    return cur
anyCharExcept  = EZRegexMember(_anyCharExceptFunc)

def _anyExceptFunc(cur, *inputs):
    raise NotImplementedError('I am as yet unsure how to implement anyExcept. Maybe try using either anyCharExcept, which does work, or something like this: (?:(?!sequence).)+')
    # cur += r'(?:'
    # for i in inputs:
    #     cur += i
    #     cur += '|'
    # cur = cur[:-1]
    # cur += r')'
    return cur
anyExcept = EZRegexMember(_anyExceptFunc)


# Sets
anyUppercase       = EZRegexMember(r'[A-Z]')
anyLowercase       = EZRegexMember(r'[a-z]')
anyLetter          = EZRegexMember(r'[A-Za-z]')
anyAlphaNum        = EZRegexMember(r'[A-Za-z0-9]')
anyDigit           = EZRegexMember(r'[0-9]')
anyHexDigit        = EZRegexMember(r'[0-9a-fA-F]')
anyOctDigit        = EZRegexMember(r'[0-7]')
anyPunctuation     = EZRegexMember(r'[:punct:]')
anyBlank           = EZRegexMember(r'[ \t\r\n\v\f]')
anyControllers     = EZRegexMember(r'[\x00-\x1F\x7F]')
anyPrinted         = EZRegexMember(r'[\x21-\x7E]')
anyPrintedAndSpace = EZRegexMember(r'[\x20-\x7E]')
anyAlphaNum_       = EZRegexMember(r'[A-Za-z0-9_]')

# Numbers
octalNum = EZRegexMember(lambda cur, num: cur + r'\\' + num)
hexNum   = EZRegexMember(lambda cur, num: cur + r'\x' + num)

# Conditionals
ifProceededBy    = EZRegexMember(lambda cur, condition: fr'{cur}(?={condition})')
ifNotProceededBy = EZRegexMember(lambda cur, condition: fr'{cur}(?!{condition})')
ifPrecededBy     = EZRegexMember(lambda cur, condition: fr'(?<={condition}){cur}')
ifNotPrecededBy  = EZRegexMember(lambda cur, condition: fr'(?<!{condition}){cur}')
ifEnclosedWith   = EZRegexMember(lambda cur, open, stuff, close: fr'((?<={open}){stuff}(?={close}))')
ifFollowedBy     = ifProceededBy
ifNotFollowedBy  = ifNotProceededBy


# Groups
# I don't understand these.
# (?aiLmsux) The letters set the corresponding flags defined below.
# \number  Matches the contents of the group of the same number.
group          = EZRegexMember(lambda cur, chain: f'{cur}({chain})')
passiveGroup   = EZRegexMember(lambda cur, chain: f'{cur}(?:{chain})')
namedGroup     = EZRegexMember(lambda cur, name, chain: f'{cur}(?P<{name}>{chain})')
# referenceGroup = EZRegexMember(lambda cur, name:        f'{cur}(?P={name})')

# TODO figure this out and add it
# Replace Syntax
# Use these on the replacement end to reference groups specified in the original regex
replaceGroup          = EZRegexMember(lambda cur, num:  f'{cur}\\g<{num}>')
# replaceNamedGroup     = EZRegexMember(lambda cur, name: f'{cur}?P={name})')
replaceNamedGroup     = replaceGroup

# # I don't think this inverse is correct
# notGroup       = EZRegexMember(lambda cur, chain: f'{cur}(?:{chain})',
#                                     lambda cur, chain: cur + chain)

# namedGroup     = EZRegexMember(lambda cur, name, chain: f'{cur}(?P {name} {chain})')
# referenceGroup = EZRegexMember(lambda cur, name:        f'{cur}(?P={name})')

# For adding raw regex statements without sanatizing them
raw = EZRegexMember(lambda cur, regex: str(regex), sanatize=False)


# TODO Implement Dialects
# Global Flags -- I don't think these will work
matchGlobally     = EZRegexMember(r'//g')
caseInsensitive   = EZRegexMember(r'//i')
matchMultiLine    = EZRegexMember(r'//m')
treatAsSingleLine = EZRegexMember(r'//s')
notGreedy         = EZRegexMember(r'//U')
