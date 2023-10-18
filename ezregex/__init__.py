#!/usr/bin/env python3
__version__ = '1.4.0'
from .EZRegexMember import EZRegexMember
from sys import version_info
from .invert import invertRegex as invert
from re import RegexFlag, escape

# Positional
# wordStartsWith = EZRegexMember(lambda input, cur=...: input + r'\<' + cur)
# wordEndsWith   = EZRegexMember(lambda input, cur=...: cur   + r'\>' + input)
stringStartsWith = EZRegexMember(lambda input, cur=...: r'\A' + input + cur)
stringEndsWith   = EZRegexMember(lambda input, cur=...: input + r'\Z' + cur)
# Always use the multiline flag, so as to distinguish between start of a line vs start of the string
lineStartsWith   = EZRegexMember(lambda input, cur=...: r'^' + input + cur, flags=RegexFlag.MULTILINE)
lineEndsWith     = EZRegexMember(lambda input, cur=...: cur + input + r'$', flags=RegexFlag.MULTILINE)

# ifAtBeginning  = EZRegexMember(lambda cur=...: r'^' + cur)
# ifAtEnd        = EZRegexMember(r'$')

# Matching
match     = EZRegexMember(lambda input, cur=...: cur + input)
isExactly = EZRegexMember(lambda input, cur=...: "^" + input + '$')
# Not sure how to implement these, I don't have enough experience with Regex
# \b       Matches the empty string, but only at the start or end of a word.
# \B       Matches the empty string, but not at the start or end of a word.

# Amounts
matchMax      = EZRegexMember(lambda      input='', cur=...: cur + ('' if not len(input) else r'(?:' + input + r')') + r'+')
matchNum      = EZRegexMember(lambda num, input='', cur=...: cur + ('' if not len(input) else r'(?:' + input + r')') + r'{' + str(num) + r'}')
matchMoreThan = EZRegexMember(lambda min, input='', cur=...: cur + ('' if not len(input) else r'(?:' + input + r')') + r'{' + str(int(min) + 1) + r',}')
matchAtLeast  = EZRegexMember(lambda min, input='', cur=...: cur + ('' if not len(input) else r'(?:' + input + r')') + r'{' + str(min) + r',}')

def _matchRangeFunc(min, max, input='', greedy=True, possessive=False, cur=..., ):
    """ Max can be an empty string to indicate no maximum
        greedy means it will try to match as many repititions as possible
        non-greedy will try to match as few repititions as possible
        possessive means it won't backtrack to try to find any repitions
        see https://docs.python.org/3/library/re.html for more help
    """
    # return cur + ('' if not len(input) else r'(?:' + input + r')') + r'{' + str(min) + r',' + str(max) + r'}'
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
matchRange = EZRegexMember(_matchRangeFunc)

# Optionals
# multiOptional = EZRegexMember(lambda cur, input='': cur + (fr'(?:{input})*' if len(input) > 1 else (fr'{input}*' if len(input) == 1 else '')))
def _optionalFunc(input='', greedy=True, possessive=False, cur=...):
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
optional = EZRegexMember(_optionalFunc)

def _atLeastOneFunc(input='', greedy=True, possessive=False, cur=...):
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
atLeastOne = EZRegexMember(_atLeastOneFunc)

def _atLeastNoneFunc(input='', greedy=True, possessive=False, cur=...):
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
atLeastNone = EZRegexMember(_atLeastNoneFunc)

either     = EZRegexMember(lambda input, or_input, cur=...: cur + rf'(?:{input}|{or_input})')
anyBetween = EZRegexMember(lambda char, and_char, cur=...: cur + r'[' + char + r'-' + and_char + r']')

# def _anyCharsFunc(cur, *inputs, split=False):
#     cur += r'['
#     for i in inputs:
#         cur += i
#     cur += r']'
#     return cur
# anyChars = EZRegexMember(_anyCharsFunc)

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
anyOf = EZRegexMember(_anyOfFunc)

def _anyCharExceptFunc(*inputs, cur=...):
    # If it's just a string, split it up
    if len(inputs) == 1 and len(inputs[0]) > 1:
        inputs = list(inputs[0])

    cur += r'[^'
    for i in inputs:
        cur += i
    cur += r']'
    return cur
anyCharExcept  = EZRegexMember(_anyCharExceptFunc)

def _anyExceptFunc(*inputs, cur=...):
    raise NotImplementedError('I am as yet unsure how to implement anyExcept. Maybe try using either anyCharExcept, which does work, or something like this: (?:(?!sequence).)+')
    # cur += r'(?:'
    # for i in inputs:
    #     cur += i
    #     cur += '|'
    # cur = cur[:-1]
    # cur += r')'
    return cur
anyExcept = EZRegexMember(_anyExceptFunc)

# Single Characters
whitespace = EZRegexMember(r'\s')
whitechunk = EZRegexMember(r'\s+')
digit      = EZRegexMember(r'\d')
number     = EZRegexMember(r'\d+')
word       = EZRegexMember(r'\w+')
wordChar   = EZRegexMember(r'\w')
# hexDigit   = EZRegexMember(r'\X')
# octDigit   = EZRegexMember(r'\O')
anything   = EZRegexMember(r'.')
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
# punctuation     = EZRegexMember(r'[:punct:]')
# punctuation     = EZRegexMember(escape('[`~!@#$%^&*()-_=+[{]}\\|;:\'",<.>/?¢]]'))
# anyBlank           = EZRegexMember(r'[ \t\r\n\v\f]')
controller     = EZRegexMember(r'[\x00-\x1F\x7F]')
printable         = EZRegexMember(r'[\x21-\x7E]')
printableAndSpace = EZRegexMember(r'[\x20-\x7E]')
# anyAlphaNum_       = EZRegexMember(r'[A-Za-z0-9_]')
unicode            = EZRegexMember(lambda name, cur=...: fr'\N{name}')

# Conditionals
ifProceededBy    = EZRegexMember(lambda condition, cur=...: fr'{cur}(?={condition})')
ifNotProceededBy = EZRegexMember(lambda condition, cur=...: fr'{cur}(?!{condition})')
ifPrecededBy     = EZRegexMember(lambda condition, cur=...: fr'(?<={condition}){cur}')
ifNotPreceededBy = EZRegexMember(lambda condition, cur=...: fr'(?<!{condition}){cur}')
ifEnclosedWith   = EZRegexMember(lambda open, stuff, close, cur=...: fr'((?<={open}){stuff}(?={close}))')

# Groups
# referenceGroup = EZRegexMember(lambda cur, name:        f'{cur}(?P={name})')
group          = EZRegexMember(lambda chain, cur=...: f'{cur}({chain})')
passiveGroup   = EZRegexMember(lambda chain, cur=...: f'{cur}(?:{chain})')
namedGroup     = EZRegexMember(lambda name, chain, cur=...: f'{cur}(?P<{name}>{chain})')

# Flags
ASCII      = EZRegexMember(lambda cur=...: cur, flags=RegexFlag.ASCII)
DOTALL     = EZRegexMember(lambda cur=...: cur, flags=RegexFlag.DOTALL)
IGNORECASE = EZRegexMember(lambda cur=...: cur, flags=RegexFlag.IGNORECASE)
LOCALE     = EZRegexMember(lambda cur=...: cur, flags=RegexFlag.LOCALE)
MULTILINE  = EZRegexMember(lambda cur=...: cur, flags=RegexFlag.MULTILINE)
UNICODE    = EZRegexMember(lambda cur=...: cur, flags=RegexFlag.UNICODE)

# For adding raw regex statements without sanatizing them
raw = EZRegexMember(lambda regex, cur=...: str(regex), sanatize=False)

# Replace syntax
replace_group  = EZRegexMember(lambda num_or_name, cur=...: fr'\g<{num_or_name}>', replacement=True)
replace_entire = EZRegexMember(lambda cur=...: r'\g<0>', replacement=True)

# Useful Combonations
literallyAnything = either(anything, newLine)
signed = optional('-') + number
unsigned = number
float = signed + period + optional(number)
int_or_float = optional('-') + number + optional(period + optional(number))
ow = optional(whitechunk)

# Psuedonyms
match_max = matchMax
match_num = matchAmt = match_amt = matchNum
match_range = matchRange
match_more_than = match_greater_than = matchGreaterThan = matchMoreThan
match_at_least = match_min = matchMin = matchAtLeast
line_starts_with = lineStartsWith
string_starts_with = stringStartsWith
line_ends_with = lineEndsWith
string_ends_with = stringEndsWith
stuff      = chunk
whiteChunk = whitechunk
anychar    = anything
anyChar    = anything
char       = anything
# anyAmt = any_amt = multi_optional = multiOpt = multi_opt = multiOptional
anyAmt = any_amt = atLeastNone
any_between = anyBetween
word_char = wordChar
hex_digit = hex
oct_digit = octDigit
newline = newLine
space_or_tab = spaceOrTab
carriage_return = carriageReturn
vertical_tab = verticalTab
form_feed = formFeed
dot = period
intOrFloat = int_or_float
not_whitespace = notWhitespace
not_digit = notDigit
not_word = notWord
# any_chars = anyChars
anyof = any_of = anyOf
any_except = anyExcept
any_char_except = anyCharExcept
printable_and_space = printableAndSpace
ifFollowedBy     = ifProceededBy
ifNotFollowedBy  = ifNotProceededBy
if_proceeded_by = ifProceededBy
if_notProceeded_by = ifNotProceededBy
if_preceded_by = ifPrecededBy
if_notPreceded_by = ifNotPreceededBy
if_enclosed_with = ifEnclosedWith
if_proceeded_by = ifProceededBy
if_notProceeded_by = ifNotProceededBy
passive_group = passiveGroup
named_group = namedGroup
replace_all = replace_entire
exactly = isExactly
oneOrNone = one_or_none = optional
oneOrMore = one_or_more = at_least_one = atLeast1 = at_least_1 = atLeastOne
noneOrMore = none_or_more = at_least_none = at_least_0 = atLeast0 = atLeastNone
ascii = a = ASCII
dotall = s = DOTALL
ignorecase = i = ignoreCase = ignore_case = IGNORECASE
locale = L = LOCALE
multiline = m = MULTILINE
unicode = u = UNICODE


# TODO:
"""

(?>...)
Attempts to match ... as if it was a separate regular expression, and if successful, continues to match the rest of the pattern following it. If the subsequent pattern fails to match, the stack can only be unwound to a point before the (?>...) because once exited, the expression, known as an atomic group, has thrown away all stack points within itself. Thus, (?>.*). would never match anything because first the .* would match all characters possible, then, having nothing left to match, the final . would fail to match. Since there are no stack points saved in the Atomic Group, and there is no stack point before it, the entire expression would thus fail to match.

(?P=name)
A backreference to a named group; it matches whatever text was matched by the earlier group named name.

\b
Matches the empty string, but only at the beginning or end of a word. A word is defined as a sequence of word characters. Note that formally, \b is defined as the boundary between a \w and a \W character (or vice versa), or between \w and the beginning/end of the string. This means that r'\bfoo\b' matches 'foo', 'foo.', '(foo)', 'bar foo baz' but not 'foobar' or 'foo3'.

\B
Matches the empty string, but only when it is not at the beginning or end of a word. This means that r'py\B' matches 'python', 'py3', 'py2', but not 'py', 'py.', or 'py!'. \B is just the opposite of \b, so word characters in Unicode patterns are Unicode alphanumerics or the underscore, although this can be changed by using the ASCII flag. Word boundaries are determined by the current locale if the LOCALE flag is used.

(?(id/name)yes-pattern|no-pattern)
Will try to match with yes-pattern if the group with given id or name exists, and with no-pattern if it doesn’t. no-pattern is optional and can be omitted. For example, (<)?(\w+@\w+(?:\.\w+)+)(?(1)>|$) is a poor email matching pattern, which will match with '<user@host.com>' as well as 'user@host.com', but not with '<user@host.com' nor 'user@host.com>'.

\number
Matches the contents of the group of the same number. Groups are numbered starting from 1. For example, (.+) \1 matches 'the the' or '55 55', but not 'thethe' (note the space after the group). This special sequence can only be used to match one of the first 99 groups. If the first digit of number is 0, or number is 3 octal digits long, it will not be interpreted as a group match, but as the character with octal value number. Inside the '[' and ']' of a character class, all numeric escapes are treated as characters.

 """
