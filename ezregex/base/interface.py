#!/usr/bin/env python3
from ..EZRegex import EZRegex

# This file gets parsed to generate the documentation, and to provide descriptions and things to ezregex.org
# You should be able to treat it as any .pyi file, with the addition that strings of the form
# "Group: <name>\n<optional description>"
# designate the group for that section, and strings below variables act as the descriptions for those variables.

InputType = str | EZRegex | int | float


string_starts_with: EZRegex
string_ends_with: EZRegex
line_starts_with: EZRegex
line_ends_with: EZRegex
word_boundary: EZRegex
"Matches the boundary of a word, i.e. the empty space between a word character and not a word character, or the end of a string"
not_word_boundary: EZRegex
"The opposite of `wordBoundary`"


tab: EZRegex
space: EZRegex
space_or_tab: EZRegex
new_line: EZRegex
carriage_return: EZRegex
quote: EZRegex
"Matches ', \", and `"
vertical_tab: EZRegex
form_feed: EZRegex
comma: EZRegex
period: EZRegex
underscore: EZRegex


not_whitespace: EZRegex
not_digit: EZRegex
not_word: EZRegex


whitespace: EZRegex
whitechunk: EZRegex
"A \"chunk\" of whitespace. Just any amount of whitespace together"
digit: EZRegex
number: EZRegex
"Matches multiple digits next to each other. Does not match negatives or decimals"
word: EZRegex
word_char: EZRegex
"Matches just a single \"word character\", defined as any letter, number, or _"
anything: EZRegex
"Matches any single character, except a newline. To also match a newline, use literally_anything"
chunk: EZRegex
'A "chunk": Any clump of characters up until the next newline'
uppercase: EZRegex
lowercase: EZRegex
letter: EZRegex
"Matches just a letter -- not numbers or _ like word_char"
hex_digit: EZRegex
oct_digit: EZRegex
punctuation: EZRegex
controller: EZRegex
"Matches a metadata ASCII characters"
printable: EZRegex
"Matches printable ASCII characters"
printable_and_space: EZRegex
alpha_num: EZRegex
unicode: EZRegex
"Matches a unicode character by name"

def any_between(char:str, and_char:str) -> EZRegex:
    "Match any char between `char` and `and_char`, using the ASCII table for reference"
    ...


def match_max(input:InputType) -> EZRegex:
    """ Match as many of `input` in the string as you can. This is equivelent to using the unary + operator.
    If `input` is not provided, it works on the previous regex pattern. That's not recommended for
    clarity's sake though
    """
    ...

def match_num(num: int, input: InputType) -> EZRegex:
    "Match `num` amount of `input` in the string"
    ...

def more_than(min: int, input: InputType) -> EZRegex:
    "Match more than `min` sequences of `input` in the string"
    ...

def at_least(min:int, input:InputType) -> EZRegex:
    "Match at least `min` sequences of `input` in the string"
    ...

def at_most(max:int, input:InputType) -> EZRegex:
    "Match at most `max` instances of `input` in the string"
    ...

def between(min:int, max:int, input:InputType, greedy:bool=True, possessive:bool=False) -> EZRegex:
    """ Match between `min` and `max` sequences of `input` in the string. This also accepts `greedy` and `possessive` parameters
        Max can be an empty string to indicate no maximum
        `greedy` means it will try to match as many repititions as possible
        non-greedy will try to match as few repititions as possible
        `possessive` means it won't backtrack to try to find any repitions
        see https://docs.python.org/3/library/re.html for more help
    """
    ...

def at_least_one(input:InputType, greedy:bool=True, possessive:bool=False) -> EZRegex:
    """ Match at least one of `input` in the string. This also accepts `greedy` and `possessive` parameters
        `greedy` means it will try to match as many repititions as possible
        non-greedy will try to match as few repititions as possible
        `possessive` means it won't backtrack to try to find any repitions
        see https://docs.python.org/3/library/re.html for more help
    """
    ...

def at_least_none(input:InputType, greedy:bool=True, possessive:bool=False) -> EZRegex:
    """ Match 0 or more sequences of `input`. This also accepts `greedy` and `possessive` parameters
        `greedy` means it will try to match as many repititions as possible
        non-greedy will try to match as few repititions as possible
        `possessive` means it won't backtrack to try to find any repitions
        see https://docs.python.org/3/library/re.html for more help
    """
    ...


def optional(input:InputType, greedy:bool=True, possessive:bool=False) -> EZRegex:
    """ Match `input` if it's there. This also accepts `greedy` and `possessive` parameters
        `greedy` means it will try to match as many repititions as possible
        non-greedy will try to match as few repititions as possible
        `possessive` means it won't backtrack to try to find any repitions
        see https://docs.python.org/3/library/re.html for more help
    """
    ...

def either(input:InputType, or_input:InputType) -> EZRegex: ...

def any_of(*inputs:str, chars:bool|None=None, split:bool|None=None) -> EZRegex:
    """ Match any of the given `inputs`. Note that `inputs` can be multiple parameters,
        or a single string. Can also accept parameters chars and split. If char is set
        to True, then `inputs` must only be a single string, it interprets `inputs`
        as characters, and splits it up to find any of the chars in the string. If
        split is set to true, it forces the ?(...) regex syntax instead of the [...]
        syntax. It should act the same way, but your output regex will look different.
        By default, it just optimizes it for you.
    """
    ...

def any_char_except(*inputs:str) -> EZRegex:
    "This matches any char that is NOT in `inputs`. `inputs` can be multiple parameters, or a single string of chars to split."
    ...

def any_except(input:InputType, type:InputType='.*') -> EZRegex:
    """ Matches anything other than `input`, which must be a single string or EZRegex chain, **not** a list. Also
    optionally accepts the `type` parameter, which works like this: \"Match any `type` other than `input`\". For example,
    \"match any word which is not foo\". Do note that this function is new, and I'm still working out the kinks.
    """
    ...

def each(*inputs:InputType) -> EZRegex:
    "Matches if the next part of the string can match all of the given inputs. Like the + operator, but out of order."
    ...



def if_proceded_by(input:InputType) -> EZRegex:
    """ Matches the pattern if it has `input` coming after it. Can only be used once in a given pattern,
        as it only applies to the end
    """
    ...

def if_not_proceded_by(input:InputType) -> EZRegex:
    """ Matches the pattern if it does **not** have `input` coming after it. Can only be used once in
        a given pattern, as it only applies to the end
    """
    ...

def if_preceded_by(input:InputType) -> EZRegex:
    """ Matches the pattern if it has `input` coming before it. Can only be used once in a given pattern,
        as it only applies to the beginning
    """
    ...

def if_not_preceded_by(input:InputType) -> EZRegex:
    """ Matches the pattern if it does **not** have `input` coming before it. Can only be used once
        in a given pattern, as it only applies to the beginning
    """
    ...

def if_enclosed_with(open:str, stuff:InputType, close:str|None=None) -> EZRegex:
    """ Matches if the string has `open`, then `stuff`, then `close`, but only \"matches\"
        stuff. Just a convenience combination of ifProceededBy and ifPreceededBy.
    """
    ...


def group(input:InputType, name:str|None=None) -> EZRegex:
    "Causes `input` to be captured as an unnamed group. Only useful when replacing regexs"
    ...

def passive_group(input:InputType) -> EZRegex:
    "As all regexs in EZRegex capture passively, this is entirely useless. But if you really want to, here it is"
    ...

def earlier_group(num_or_name:int|str) -> EZRegex:
    """ Matches whatever the group referenced by `num_or_name` matched earlier. Must be *after* a
    group which would match `num_or_name`
    """
    ...

def if_exists(num_or_name:int|str, does:InputType, doesnt:InputType|None=None) -> EZRegex:
    """ Matches `does` if the group `num_or_name` exists, otherwise it matches `doesnt` """
    ...



def rgroup(num_or_name:str|int) -> EZRegex:
    """ Puts in its place the group specified, either by group number (for unnamed
        groups) or group name (for named groups). Named groups are also counted by
        number, I'm pretty sure. Groups are numbered starting from 1
    """
    ...

replace_entire: EZRegex
"Puts in its place the entire match"

def replace(string:str, rtn_str:bool=True) -> str|EZRegex:
    """ Generates a valid regex replacement string, using Python f-string like syntax.

        Example:
            ``` replace("named: {group}, numbered: {1}, entire: {0}") ```

        Like Python f-strings, use {{ and }} to specify { and }

        Set the `rtn_str` parameter to True to have it return an EZRegex type instead of a string

        Note: Remember that index 0 is the entire match

        There's a few of advantages to using this instead of just the regular regex replacement syntax:
        - It's consistent between dialects
        - It's closer to Python f-string syntax, which is cleaner and more familiar
        - It handles numbered, named, and entire replacement types the same
    """
    ...


def is_exactly(input:InputType) -> EZRegex:
    "This matches the string if and only if the entire string is exactly equal to `input`"
    ...

def literal(input:InputType) -> EZRegex:
    "This is a redundant function. You should always be able to use `... + 'stuff'` just as easily as `... + literal('stuff')`"
    ...

# For adding raw regex statements without sanatizing them
def raw(regex:str) -> EZRegex:
    """ If you already have some regular regex written, and you want to incorperate
        it, this will allow you to include it without sanatizing all the backslaches
        and such, which all the other EZRegexs do automatically
    """
    ...



literally_anything: EZRegex
"*Any* character, include newline"
signed: EZRegex
"a signed number, including 123, -123, and +123"
unsigned: EZRegex
"Same as number. Will not match +123"
plain_float: EZRegex
"Will match 123.45 and 123."
full_float: EZRegex
"Will match plain_float as well as things like 1.23e-10 and 1.23e+10"
int_or_float: EZRegex
ow: EZRegex
"\"Optional Whitechunk\""

