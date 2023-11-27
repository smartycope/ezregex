#!/usr/bin/env python3
__version__ = '1.4.4'
# from .EZRegexMember import EZRegexMember
from ezregex import EZRegexMember
from sys import version_info
from re import RegexFlag, escape
from warnings import warn

# NOTE: A bunch of these have wrapper functions around them. They're just for
# linting and type hinting in the editor. Do note that passing the parameters
# directly *doesn't* work, because when calling passed lambdas, EZRegexMember
# sanatizes the parameters in a particular way, depending on internal members.

# Positional
# wordStartsWith = EZRegexMember(lambda input, cur=...: input + r'\<' + cur)
# wordEndsWith   = EZRegexMember(lambda input, cur=...: cur   + r'\>' + input)
# \b       Matches the empty string, but only at the start or end of a word.
# \B       Matches the empty string, but not at the start or end of a word.
stringStartsWith = EZRegexMember(lambda input='', cur=...: r'\A' + input + cur)
stringEndsWith   = EZRegexMember(lambda input='', cur=...: input + r'\Z' + cur)
# Always use the multiline flag, so as to distinguish between start of a line vs start of the string
lineStartsWith   = EZRegexMember(lambda input='', cur=...: r'^' + input + cur, flags=RegexFlag.MULTILINE)
lineEndsWith     = EZRegexMember(lambda input='', cur=...: cur + input + r'$', flags=RegexFlag.MULTILINE)

# Matching
def isExactly(input) -> EZRegexMember:
    "This matches the string if and only if the entire string is exactly equal to `input`"
    return EZRegexMember(lambda input, cur=...: r"\A" + input + r'\Z')(input)

def literal(input) -> EZRegexMember:
    "This is a redundant function. You should always be able to use `... + 'stuff'` just as easily as `... + literal('stuff')`"
    return EZRegexMember(lambda input, cur=...: cur + input)(input)


# Amounts and Optionals
def matchMax(input) -> EZRegexMember:
    """Match as many of `input` in the string as you can. This is equivelent to using the unary + operator.
    If `input` is not provided, it works on the previous regex pattern. That's not recommended for
    clarity's sake though"""
    return EZRegexMember(lambda input, cur=...: cur + ('' if not len(input) else r'(?:' + input + r')') + r'+')(input)

def matchNum(num, input) -> EZRegexMember:
    "Match `num` amount of `input` in the string"
    return EZRegexMember(lambda num, input, cur=...: cur + ('' if not len(input) else r'(?:' + input + r')') + r'{' + str(num) + r'}')(num, input)

def matchMoreThan(min, input) -> EZRegexMember:
    "Match more than `min` sequences of `input` in the string"
    return EZRegexMember(lambda min, input, cur=...: cur + ('' if not len(input) else r'(?:' + input + r')') + r'{' + str(int(min) + 1) + r',}')(min, input)

def matchAtLeast(min, input) -> EZRegexMember:
    "Match at least `min` sequences of `input` in the string"
    return EZRegexMember(lambda min, input, cur=...: cur + ('' if not len(input) else r'(?:' + input + r')') + r'{' + str(min) + r',}')(min, input)

def matchAtMost(max, input) -> EZRegexMember:
    "Match at most `max` instances of `input` in the string"
    return EZRegexMember(lambda max, input, cur=...: cur + ('' if not len(input) else r'(?:' + input + r')') + r'{0,' + str(max) + r'}')(max, input)

def matchRange(min, max, input, greedy=True, possessive=False) -> EZRegexMember:
    """ Match between `min` and `max` sequences of `input` in the string. This also accepts `greedy` and `possessive` parameters
        Max can be an empty string to indicate no maximum
        greedy means it will try to match as many repititions as possible
        non-greedy will try to match as few repititions as possible
        possessive means it won't backtrack to try to find any repitions
        see https://docs.python.org/3/library/re.html for more help
    """
    def _matchRangeFunc(min, max, input, greedy=True, possessive=False, cur=..., ):
        assert not ((not greedy) and possessive), 'Match Range can\'t be non-greedy AND possessive at the same time'
        s = ''
        if len(input):
            s += r'(?:' + input + r')'
        s += r'{' + str(min) + r',' + str(max) + r'}'
        if not greedy:
            s += r'?'
        if possessive:
            if version_info < (3, 11):
                raise Exception('Possessive qualifiers require at least Python3.11 ')
            s += r'+'
        return s
    return EZRegexMember(_matchRangeFunc)(min, max, input, greedy=greedy, possessive=possessive)

def optional(input, greedy=True, possessive=False) -> EZRegexMember:
    """ Match `input` if it's there. This also accepts `greedy` and `possessive` parameters
        greedy means it will try to match as many repititions as possible
        non-greedy will try to match as few repititions as possible
        possessive means it won't backtrack to try to find any repitions
        see https://docs.python.org/3/library/re.html for more help
    """
    def _optionalFunc(input, greedy=True, possessive=False, cur=...):
        assert not ((not greedy) and possessive), 'optional can\'t be non-greedy AND possessive at the same time'
        s = cur
        if len(input) > 1:
            s += fr'(?:{input})?'
        else:
            if len(input) == 1:
                s += fr'{input}?'
        if not greedy:
            s += r'?'
        if possessive:
            if version_info < (3, 11):
                raise Exception('Possessive qualifiers require at least Python3.11 ')
            s += r'+'
        return s
    return EZRegexMember(_optionalFunc)(input, greedy=greedy, possessive=possessive)

def atLeastOne(input, greedy=True, possessive=False) -> EZRegexMember:
    """ Match at least one of `input` in the string. This also accepts `greedy` and `possessive` parameters
        greedy means it will try to match as many repititions as possible
        non-greedy will try to match as few repititions as possible
        possessive means it won't backtrack to try to find any repitions
        see https://docs.python.org/3/library/re.html for more help
    """
    def _atLeastOneFunc(input, greedy=True, possessive=False, cur=...):
        assert not ((not greedy) and possessive), 'At Least One can\'t be non-greedy AND possessive at the same time'
        s = cur
        if len(input) > 1:
            s += fr'(?:{input})+'
        else:
            if len(input) == 1:
                s += fr'{input}+'
        if not greedy:
            s += '?'
        if possessive:
            if version_info < (3, 11):
                raise Exception('Possessive qualifiers require at least Python3.11 ')
            s += '+'
        return s
    return EZRegexMember(_atLeastOneFunc)(input, greedy=greedy, possessive=possessive)

def atLeastNone(input, greedy=True, possessive=False) -> EZRegexMember:
    """ Match 0 or more sequences of `input`. This also accepts `greedy` and `possessive` parameters
        greedy means it will try to match as many repititions as possible
        non-greedy will try to match as few repititions as possible
        possessive means it won't backtrack to try to find any repitions
        see https://docs.python.org/3/library/re.html for more help
    """
    def _atLeastNoneFunc(input, greedy=True, possessive=False, cur=...):
        assert not ((not greedy) and possessive), 'At Least None can\'t be non-greedy AND possessive at the same time'
        s = cur
        if len(input) > 1:
            s += fr'(?:{input})*'
        else:
            if len(input) == 1:
                s += fr'{input}*'
        if not greedy:
            s += '?'
        if possessive:
            if version_info < (3, 11):
                raise Exception('Possessive qualifiers require at least Python3.11 ')
            s += '+'
        return s
    return EZRegexMember(_atLeastNoneFunc)(input, greedy=greedy, possessive=possessive)

def either(input, or_input) -> EZRegexMember:
    return EZRegexMember(lambda input, or_input, cur=...: cur + rf'(?:{input}|{or_input})')(input, or_input)

def anyBetween(char, and_char) -> EZRegexMember:
    "Match any char between `char` and `and_char`, using the ASCII table for reference"
    return EZRegexMember(lambda char, and_char, cur=...: cur + r'[' + char + r'-' + and_char + r']')(char, and_char)

# def _anyCharsFunc(cur, *inputs, split=False):
#     cur += r'['
#     for i in inputs:
#         cur += i
#     cur += r']'
#     return cur
# anyChars = EZRegexMember(_anyCharsFunc)
def anyOf(*inputs, chars=None, split=None) -> EZRegexMember:
    """ Match any of the given `inputs`. Note that `inputs` can be multiple parameters,
        or a single string. Can also accept parameters chars and split. If char is set
        to True, then `inputs` must only be a single string, it interprets `inputs`
        as characters, and splits it up to find any of the chars in the string. If
        split is set to true, it forces the ?(...) regex syntax instead of the [...]
        syntax. It should act the same way, but your output regex will look different.
        By default, it just optimizes it for you.
    """
    def _anyOfFunc(*inputs, chars=None, split=None, cur=...):
        if split and len(inputs) != 1:
            assert False, "Please don't specifiy split and pass multiple inputs to anyof"
        elif split:
            inputs = list(inputs[0])
        elif len(inputs) == 1 and split is None and chars is not False:  # None means auto
            chars = True
            inputs = list(inputs[0])
        elif len(inputs) == 1 and split is None:
            inputs = list(inputs[0])
        elif len(inputs) > 1 and chars is None and all(map(lambda s: len(s) == 1, inputs)):
            chars = True

        if chars:
            cur += r'['
            for i in inputs:
                cur += i
            cur += r']'
        else:
            cur += r'(?:'
            for i in inputs:
                cur += i
                cur += '|'
            cur = cur[:-1]
            cur += r')'
        return cur
    return EZRegexMember(_anyOfFunc)(*inputs, chars=chars, split=split)

def anyCharExcept(*inputs) -> EZRegexMember:
    "This matches any char that is NOT in `inputs`. `inputs` can be multiple parameters, or a single string of chars to split."
    def _anyCharExceptFunc(*inputs, cur=...):
        # If it's just a string, split it up
        if len(inputs) == 1 and len(inputs[0]) > 1:
            inputs = list(inputs[0])

        cur += r'[^'
        for i in inputs:
            cur += i
        cur += r']'
        return cur
    return EZRegexMember(_anyCharExceptFunc)(*inputs)

def anyExcept(input, type='.*') -> EZRegexMember:
    """ Matches anything other than `input`, which must be a single string or
    EZRegex chain, **not** a list. Also optionally accepts the `type` parameter,
    which works like this: \"Match any `type` other than `input`\". For example,
    \"match any word which is not foo\". Do note that this function is new, and
    I'm still working out the kinks."""
    warn('This is likely to fail')
    return EZRegexMember(lambda input, type='.*', cur=...: cur + f'(?!{input}){type}')(input, type=type)

# Single Characters
whitespace = EZRegexMember(r'\s')
whitechunk = EZRegexMember(r'\s+')
digit      = EZRegexMember(r'\d')
number     = EZRegexMember(r'\d+')
word       = EZRegexMember(r'\w+')
wordChar   = EZRegexMember(r'\w')
anything   = EZRegexMember(r'.')
# A "chunk": Any clump of characters up until the next newline
chunk      = EZRegexMember(r'.+')

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
period         = EZRegexMember(r'\.')

# Not Chuncks
notWhitespace = EZRegexMember(r'\S')
notDigit      = EZRegexMember(r'\D')
notWord       = EZRegexMember(r'\W')

# Sets
uppercase       = EZRegexMember(r'[A-Z]')
lowercase       = EZRegexMember(r'[a-z]')
letter          = EZRegexMember(r'[A-Za-z]')
# anyAlphaNum        = EZRegexMember(r'[A-Za-z0-9]')
# anyDigit           = EZRegexMember(r'[0-9]')
hexDigit        = EZRegexMember(r'[0-9a-fA-F]')
octDigit        = EZRegexMember(r'[0-7]')
# hexDigit   = EZRegexMember(r'\X')
# octDigit   = EZRegexMember(r'\O')
# punctuation     = EZRegexMember(r'[:punct:]')
punctuation     = EZRegexMember(r'[' + escape('`~!@#$%^&*()-_=+[{]}\\|;:\'",<.>/?¢]') + r']')
# anyBlank           = EZRegexMember(r'[ \t\r\n\v\f]')
controller        = EZRegexMember(r'[\x00-\x1F\x7F]')
printable         = EZRegexMember(r'[\x21-\x7E]')
printableAndSpace = EZRegexMember(r'[\x20-\x7E]')
alphaNum          = EZRegexMember(r'[A-Za-z0-9_]')
unicode            = EZRegexMember(lambda name, cur=...: fr'\N{name}')

# Conditionals
def ifProceededBy(condition) -> EZRegexMember:
    "Matches the prior pattern if it has `condition` coming after it"
    return EZRegexMember(lambda condition, cur=...: fr'{cur}(?={condition})')(condition)

def ifNotProceededBy(condition) -> EZRegexMember:
    "Matches the prior pattern if it does **not** have `condition` coming after it"
    return EZRegexMember(lambda condition, cur=...: fr'{cur}(?!{condition})')(condition)

def ifPrecededBy(condition) -> EZRegexMember:
    "Matches the prior pattern if it has `condition` coming before it"
    return EZRegexMember(lambda condition, cur=...: fr'(?<={condition}){cur}')(condition)

def ifNotPreceededBy(condition) -> EZRegexMember:
    "Matches the prior pattern if it does **not** have `condition` coming before it"
    return EZRegexMember(lambda condition, cur=...: fr'(?<!{condition}){cur}')(condition)

def ifEnclosedWith(open, stuff, close=None) -> EZRegexMember:
    """ Matches if the string has `open`, then `stuff`, then `close`, but only \"matches\"
        stuff. Just a convenience combination of ifProceededBy and ifPreceededBy.
    """
    if close is None:
        close = open
    return EZRegexMember(lambda open, stuff, close, cur=...: fr'((?<={open}){stuff}(?={close}))')(cur, open, close)


# Groups
# referenceGroup = EZRegexMember(lambda cur, name:        f'{cur}(?P={name})')
def group(input, name:str=None) -> EZRegexMember:
    "Causes `input` to be captured as an unnamed group. Only useful when replacing regexs"
    if name is None:
        return EZRegexMember(lambda input, cur=...: f'{cur}({input})')(input)
    else:
        return EZRegexMember(lambda name, input, cur=...: f'{cur}(?P<{name}>{input})')(name, input)

def passiveGroup(input) -> EZRegexMember:
    "As all regexs in EZRegex capture passively, this is entirely useless. But if you really want to, here it is"
    return EZRegexMember(lambda input, cur=...: f'{cur}(?:{input})')(input)

def namedGroup(name, input) -> EZRegexMember:
    "Causes `input` to be captured as a named group, with the name `name`. Only useful when replacing regexs"
    warn(f'This function is now depricated. Please use the group member with the `name` arguement instead.')
    return EZRegexMember(lambda name, input, cur=...: f'{cur}(?P<{name}>{input})')(name, input)


# Flags
ASCII      = EZRegexMember(lambda cur=...: cur, flags=RegexFlag.ASCII)
DOTALL     = EZRegexMember(lambda cur=...: cur, flags=RegexFlag.DOTALL)
IGNORECASE = EZRegexMember(lambda cur=...: cur, flags=RegexFlag.IGNORECASE)
LOCALE     = EZRegexMember(lambda cur=...: cur, flags=RegexFlag.LOCALE)
MULTILINE  = EZRegexMember(lambda cur=...: cur, flags=RegexFlag.MULTILINE)
UNICODE    = EZRegexMember(lambda cur=...: cur, flags=RegexFlag.UNICODE)

# TODO
# keyword = EZRegexMember(lambda input, cur=...: cur + input + fr'{cur}(?={condition})'+ input)
# Keyword - similar to Literal, but must be immediately followed by whitespace, punctuation, or other non-keyword characters; prevents accidental matching of a non-keyword that happens to begin with a defined keyword
# keyword = lambda input: literal() + ifProceededBy(anyof(whitespace, pun))

# For adding raw regex statements without sanatizing them
def raw(regex) -> EZRegexMember:
    """ If you already have some regular regex written, and you want to incorperate
        it, this will allow you to include it without sanatizing all the backslaches
        and such, which all the other EZRegexMembers do automatically."""
    return EZRegexMember(lambda regex, cur=...: str(regex), sanatize=False)(regex)

# Replace syntax
def rgroup(num_or_name) -> EZRegexMember:
    """ Puts in its place the group specified, either by group number (for unnamed
        groups) or group name (for named groups). Named groups are also counted by
        number, I'm pretty sure. Groups are numbered starting from 1."""
    return EZRegexMember(lambda num_or_name, cur=...: fr'\g<{num_or_name}>', replacement=True)(num_or_name)

replaceEntire = EZRegexMember(lambda cur=...: r'\g<0>', replacement=True)

# Useful Combonations
literallyAnything = either(anything, newLine)
signed = optional(either('-', '+')) + number
unsigned = number
plain_float = signed + period + optional(number)
full_float = plain_float + optional('e' + signed)
int_or_float = optional('-') + number + optional(period + optional(number))
ow = optional(whitechunk)
# Source: http://stackoverflow.com/questions/201323/ddg#201378
email = raw(r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])")
