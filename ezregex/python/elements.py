#!/usr/bin/env python3
from ..EZRegex import EZRegex
from sys import version_info
from re import RegexFlag, escape, sub
from warnings import warn
from string import Template


# NOTE: A bunch of these have wrapper functions around them. They're just for
# linting and type hinting in the editor. Do note that passing the parameters
# directly *doesn't* work, because when calling passed lambdas, EZRegex
# sanatizes the parameters in a particular way, depending on internal members.


## Positional
stringStartsWith = EZRegex(lambda input='', cur=...: r'\A' + input + cur)
stringEndsWith   = EZRegex(lambda input='', cur=...: input + r'\Z' + cur)
# Always use the multiline flag, so as to distinguish between start of a line vs start of the string
lineStartsWith   = EZRegex(lambda input='', cur=...: r'^' + input + cur, flags=RegexFlag.MULTILINE)
lineEndsWith     = EZRegex(lambda input='', cur=...: cur + input + r'$', flags=RegexFlag.MULTILINE)
wordBoundary     = EZRegex(r'\b')
notWordBoundary  = EZRegex(r'\B')

## Literals
tab            = EZRegex(r'\t')
space          = EZRegex(r' ')
spaceOrTab     = EZRegex(r'[ \t]')
newLine        = EZRegex(r'\n')
carriageReturn = EZRegex(r'\r')
quote          = EZRegex(r'(?:\'|"|`)')
verticalTab    = EZRegex(r'\v')
formFeed       = EZRegex(r'\f')
comma          = EZRegex(r'\,')
period         = EZRegex(r'\.')
underscore     = EZRegex(r'_')


## Not Literals
notWhitespace = EZRegex(r'\S')
notDigit      = EZRegex(r'\D')
notWord       = EZRegex(r'\W')


## Catagories
whitespace = EZRegex(r'\s')
whitechunk = EZRegex(r'\s+')
digit      = EZRegex(r'\d')
number     = EZRegex(r'\d+')
word       = EZRegex(r'\w+')
wordChar   = EZRegex(r'\w')
anything   = EZRegex(r'.')
# A "chunk": Any clump of characters up until the next newline
chunk      = EZRegex(r'.+')
uppercase       = EZRegex(r'[A-Z]')
lowercase       = EZRegex(r'[a-z]')
letter          = EZRegex(r'[A-Za-z]')
hexDigit        = EZRegex(r'[0-9a-fA-F]')
octDigit        = EZRegex(r'[0-7]')
punctuation     = EZRegex(r'[' + escape('`~!@#$%^&*()-_=+[{]}\\|;:\'",<.>/?¢]') + r']')
controller        = EZRegex(r'[\x00-\x1F\x7F]')
printable         = EZRegex(r'[\x21-\x7E]')
printableAndSpace = EZRegex(r'[\x20-\x7E]')
alphaNum          = EZRegex(r'[A-Za-z0-9_]')
unicode            = EZRegex(lambda name, cur=...: fr'\N{name}')
def anyBetween(char, and_char) -> EZRegex:
    "Match any char between `char` and `and_char`, using the ASCII table for reference"
    return EZRegex(lambda char, and_char, cur=...: cur + r'[' + char + r'-' + and_char + r']')(char, and_char)


## Amounts
def matchMax(input) -> EZRegex:
    """Match as many of `input` in the string as you can. This is equivelent to using the unary + operator.
    If `input` is not provided, it works on the previous regex pattern. That's not recommended for
    clarity's sake though"""
    return EZRegex(lambda input, cur=...: cur + ('' if not len(input) else r'(?:' + input + r')') + r'+')(input)

def matchNum(num, input) -> EZRegex:
    "Match `num` amount of `input` in the string"
    return EZRegex(lambda num, input, cur=...: cur + ('' if not len(input) else r'(?:' + input + r')') + r'{' + str(num) + r'}')(num, input)

def matchMoreThan(min, input) -> EZRegex:
    "Match more than `min` sequences of `input` in the string"
    return EZRegex(lambda min, input, cur=...: cur + ('' if not len(input) else r'(?:' + input + r')') + r'{' + str(int(min) + 1) + r',}')(min, input)

def matchAtLeast(min, input) -> EZRegex:
    "Match at least `min` sequences of `input` in the string"
    return EZRegex(lambda min, input, cur=...: cur + ('' if not len(input) else r'(?:' + input + r')') + r'{' + str(min) + r',}')(min, input)

def matchAtMost(max, input) -> EZRegex:
    "Match at most `max` instances of `input` in the string"
    return EZRegex(lambda max, input, cur=...: cur + ('' if not len(input) else r'(?:' + input + r')') + r'{0,' + str(max) + r'}')(max, input)

def matchRange(min, max, input, greedy=True, possessive=False) -> EZRegex:
    """ Match between `min` and `max` sequences of `input` in the string. This also accepts `greedy` and `possessive` parameters
        Max can be an empty string to indicate no maximum
        greedy means it will try to match as many repititions as possible
        non-greedy will try to match as few repititions as possible
        possessive means it won't backtrack to try to find any repitions
        see https://docs.python.org/3/library/re.html for more help
    """
    def _matchRangeFunc(min, max, input, greedy=True, possessive=False, cur=...):
        assert not ((not greedy) and possessive), 'Match Range can\'t be non-greedy AND possessive at the same time'
        s = cur
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
    return EZRegex(_matchRangeFunc)(min, max, input, greedy=greedy, possessive=possessive)

def atLeastOne(input, greedy=True, possessive=False) -> EZRegex:
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
    return EZRegex(_atLeastOneFunc)(input, greedy=greedy, possessive=possessive)

def atLeastNone(input, greedy=True, possessive=False) -> EZRegex:
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
    return EZRegex(_atLeastNoneFunc)(input, greedy=greedy, possessive=possessive)


## Choices
def optional(input, greedy=True, possessive=False) -> EZRegex:
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
    return EZRegex(_optionalFunc)(input, greedy=greedy, possessive=possessive)

def either(input, or_input) -> EZRegex:
    return EZRegex(lambda input, or_input, cur=...: cur + rf'(?:{input}|{or_input})')(input, or_input)

def anyOf(*inputs, chars=None, split=None) -> EZRegex:
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
    return EZRegex(_anyOfFunc)(*inputs, chars=chars, split=split)

def anyCharExcept(*inputs) -> EZRegex:
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
    return EZRegex(_anyCharExceptFunc)(*inputs)

def anyExcept(input, type='.*') -> EZRegex:
    """ Matches anything other than `input`, which must be a single string or
    EZRegex chain, **not** a list. Also optionally accepts the `type` parameter,
    which works like this: \"Match any `type` other than `input`\". For example,
    \"match any word which is not foo\". Do note that this function is new, and
    I'm still working out the kinks."""
    warn('This is likely to fail')
    return EZRegex(lambda input, type='.*', cur=...: cur + f'(?!{input}){type}')(input, type=type)

def each(*inputs) -> EZRegex:
    """ Matches if the next part of the string can match all of the given inputs. Like the +
        operator, but out of order."""
    def _each(*inputs, cur=...):
        inputs = list(inputs)
        last = inputs.pop()
        s = cur
        for i in inputs:
            s += fr'(?={i})'
        s += last
        return s
    return EZRegex(_each)(*inputs)


## Conditionals
def ifProcededBy(input) -> EZRegex:
    """ Matches the pattern if it has `input` coming after it. Can only be used once in a given pattern,
        as it only applies to the end """
    return EZRegex(lambda input, cur=...: fr'{cur}(?={input})')(input)

def ifNotProcededBy(input) -> EZRegex:
    """ Matches the pattern if it does **not** have `input` coming after it. Can only be used once in
        a given pattern, as it only applies to the end """
    return EZRegex(lambda input, cur=...: fr'{cur}(?!{input})')(input)

def ifPrecededBy(input) -> EZRegex:
    """ Matches the pattern if it has `input` coming before it. Can only be used once in a given pattern,
        as it only applies to the beginning """
    return EZRegex(lambda input, cur=...: fr'(?<={input}){cur}')(input)

def ifNotPrecededBy(input) -> EZRegex:
    """ Matches the pattern if it does **not** have `input` coming before it. Can only be used once
        in a given pattern, as it only applies to the beginning """
    return EZRegex(lambda input, cur=...: fr'(?<!{input}){cur}')(input)

def ifEnclosedWith(open, stuff, close=None) -> EZRegex:
    """ Matches if the string has `open`, then `stuff`, then `close`, but only \"matches\"
        stuff. Just a convenience combination of ifProceededBy and ifPreceededBy.
    """
    if close is None:
        close = open
    return EZRegex(lambda open, stuff, close, cur=...: fr'((?<={open}){stuff}(?={close}))')(open, stuff, close)


# Grouping
def group(input, name:str=None) -> EZRegex:
    "Causes `input` to be captured as an unnamed group. Only useful when replacing regexs"
    if name is None:
        return EZRegex(lambda input, cur=...: f'{cur}({input})')(input)
    else:
        return EZRegex(lambda name, input, cur=...: f'{cur}(?P<{name}>{input})')(name, input)

def passiveGroup(input) -> EZRegex:
    "As all regexs in EZRegex capture passively, this is entirely useless. But if you really want to, here it is"
    return EZRegex(lambda input, cur=...: f'{cur}(?:{input})')(input)

def earlierGroup(num_or_name) -> EZRegex:
    """ Matches whatever the group referenced by `num_or_name` matched earlier. Must be *after* a
    group which would match `num_or_name`. """
    if isinstance(num_or_name, int) or num_or_name in '0123456789':
        return EZRegex(lambda num_or_name, cur=...: f'{cur}\\{num_or_name}')(num_or_name)
    else:
        return EZRegex(lambda num_or_name, cur=...: f'{cur}(?P={num_or_name})')(num_or_name)

def ifExists(num_or_name, does, doesnt=None) -> EZRegex:
    """ Matches `does` if the group `num_or_name` exists, otherwise it matches `doesnt` """
    return EZRegex(lambda num_or_name, does, doesnt, cur=...: f'{cur}(?({num_or_name}){does}{"|" + str(doesnt) if doesnt is not None else ""})')(num_or_name, does, doesnt)

def namedGroup(name, input) -> EZRegex:
    "Causes `input` to be captured as a named group, with the name `name`. Only useful when replacing regexs"
    warn('This function is now depricated. Please use the group member with the `name` arguement instead.')
    # return EZRegex(lambda name, input, cur=...: f'{cur}(?P<{name}>{input})')(name, input)
    return group(input, name=name)


## Replacement
def rgroup(num_or_name:str|int) -> EZRegex:
    """ Puts in its place the group specified, either by group number (for unnamed
        groups) or group name (for named groups). Named groups are also counted by
        number, I'm pretty sure. Groups are numbered starting from 1."""
    return EZRegex(lambda num_or_name, cur=...: fr'{cur}\g<{num_or_name}>', replacement=True)(num_or_name)
replaceEntire = EZRegex(lambda cur=...: cur + r'\g<0>', replacement=True)

def replace(string:str, rtn_str:bool=True) -> str:
    """ Generates a valid regex replacement string, using Python f-string like syntax.

        Example:
            ``` replace("named: {group}, numbered: {1}, entire: {0}") ```

        Like Python f-strings, use {{ and }} to specify { and }

        Set the `rtn_str` parameter to True to have it return an EZRegex type instead of a string

        Note: Remember that index 0 is the entire match

        There's a couple of advantages to using this instead of just the regular regex replacement syntax:
        - It's consistent between dialects
        - It's closer to Python f-string syntax, which is cleaner and more familiar
        - It handles numbered, named, and entire replacement types the same
    """
    # Made with ezregex.org
    # Previous method
    # '{' + optional(anyCharExcept('{'), greedy=False) + group(+alphaNum) + '}' + optional(anyCharExcept('}'), greedy=False)
    # Current method
    # '{' + group(+alphaNum) + '}'
    r = r'\{((?:[A-Za-z0-9_])+)\}'
    # Convert them to something unique, then back, so we won't pick up things like {{this}}
    # {{this}} -> \0(this\0) -> {this}
    # instead of
    # {{this}} -> {this} -> \g<this>
    string = sub('{{', '\0\0(', string)
    string = sub('}}', '\0\0)', string)
    string = sub(r, r'\\g<\g<1>>', string)
    string = sub(r'\0\0\(', '{', string)
    string = sub(r'\0\0\)', '}', string)
    return EZRegex(string, sanatize=False, replacement=True)

## Misc.
def isExactly(input) -> EZRegex:
    "This matches the string if and only if the entire string is exactly equal to `input`"
    return EZRegex(lambda input, cur=...: r"\A" + input + r'\Z')(input)

def literal(input) -> EZRegex:
    "This is a redundant function. You should always be able to use `... + 'stuff'` just as easily as `... + literal('stuff')`"
    return EZRegex(lambda input, cur=...: cur + input)(input)
# For adding raw regex statements without sanatizing them
def raw(regex) -> EZRegex:
    """ If you already have some regular regex written, and you want to incorperate
        it, this will allow you to include it without sanatizing all the backslaches
        and such, which all the other EZRegexs do automatically."""
    return EZRegex(lambda regex, cur=...: str(regex), sanatize=False)(regex)


## Premade
literallyAnything = either(anything, newLine)
signed = optional(either('-', '+')) + number
unsigned = number
plain_float = signed + period + optional(number)
full_float = plain_float + optional('e' + signed)
int_or_float = optional('-') + number + optional(period + optional(number))
ow = optional(whitechunk)
# Source: http://stackoverflow.com/questions/201323/ddg#201378
email = raw(r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])")
# Source: https://semver.org/ (at the bottom)
version = raw(r"(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?")
version_numbered = raw(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?")


## Flags
ASCII      = EZRegex(lambda cur=...: cur, flags=RegexFlag.ASCII)
DOTALL     = EZRegex(lambda cur=...: cur, flags=RegexFlag.DOTALL)
IGNORECASE = EZRegex(lambda cur=...: cur, flags=RegexFlag.IGNORECASE)
LOCALE     = EZRegex(lambda cur=...: cur, flags=RegexFlag.LOCALE)
MULTILINE  = EZRegex(lambda cur=...: cur, flags=RegexFlag.MULTILINE)
UNICODE    = EZRegex(lambda cur=...: cur, flags=RegexFlag.UNICODE)
