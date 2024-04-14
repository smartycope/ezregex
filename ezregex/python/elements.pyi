#!/usr/bin/env python3
# from ..EZRegex import EZRegex

"Group: Test"
type EZRegex = int

InputType = str | EZRegex | int | float


def any_between(char:str, and_char:str) -> EZRegex:
    "Match any char between `char` and `and_char`, using the ASCII table for reference"

"Group: Amounts"
def match_max(input:InputType) -> EZRegex:
    """Match as many of `input` in the string as you can. This is equivelent to using the unary + operator.
    If `input` is not provided, it works on the previous regex pattern. That's not recommended for
    clarity's sake though"""

def match_num(num: int, input: InputType) -> EZRegex:
    "Match `num` amount of `input` in the string"

def match_more_than(min: int, input: InputType) -> EZRegex:
    "Match more than `min` sequences of `input` in the string"

def match_at_least(min:int, input:InputType) -> EZRegex:
    "Match at least `min` sequences of `input` in the string"

def match_at_most(max:int, input:InputType) -> EZRegex:
    "Match at most `max` instances of `input` in the string"

def match_range(min:int, max:int, input:InputType, greedy:bool=True, possessive:bool=False) -> EZRegex:
    """ Match between `min` and `max` sequences of `input` in the string. This also accepts `greedy` and `possessive` parameters
        Max can be an empty string to indicate no maximum
        greedy means it will try to match as many repititions as possible
        non-greedy will try to match as few repititions as possible
        possessive means it won't backtrack to try to find any repitions
        see https://docs.python.org/3/library/re.html for more help
    """

def at_least_one(input:InputType, greedy:bool=True, possessive:bool=False) -> EZRegex:
    """ Match at least one of `input` in the string. This also accepts `greedy` and `possessive` parameters
        greedy means it will try to match as many repititions as possible
        non-greedy will try to match as few repititions as possible
        possessive means it won't backtrack to try to find any repitions
        see https://docs.python.org/3/library/re.html for more help
    """

def at_least_none(input:InputType, greedy:bool=True, possessive:bool=False) -> EZRegex:
    """ Match 0 or more sequences of `input`. This also accepts `greedy` and `possessive` parameters
        greedy means it will try to match as many repititions as possible
        non-greedy will try to match as few repititions as possible
        possessive means it won't backtrack to try to find any repitions
        see https://docs.python.org/3/library/re.html for more help
    """

"Group: Choices"
def optional(input:InputType, greedy:bool=True, possessive:bool=False) -> EZRegex:
    """ Match `input` if it's there. This also accepts `greedy` and `possessive` parameters
        greedy means it will try to match as many repititions as possible
        non-greedy will try to match as few repititions as possible
        possessive means it won't backtrack to try to find any repitions
        see https://docs.python.org/3/library/re.html for more help
    """

def either(input:InputType, or_input:InputType) -> EZRegex: ...

# TODO
def any_of(*inputs, chars=None, split=None) -> EZRegex:
    """ Match any of the given `inputs`. Note that `inputs` can be multiple parameters,
        or a single string. Can also accept parameters chars and split. If char is set
        to True, then `inputs` must only be a single string, it interprets `inputs`
        as characters, and splits it up to find any of the chars in the string. If
        split is set to true, it forces the ?(...) regex syntax instead of the [...]
        syntax. It should act the same way, but your output regex will look different.
        By default, it just optimizes it for you.
    """

# TODO
def any_char_except(*inputs) -> EZRegex:
    "This matches any char that is NOT in `inputs`. `inputs` can be multiple parameters, or a single string of chars to split."

# TODO
def any_except(input, type='.*') -> EZRegex:
    """ Matches anything other than `input`, which must be a single string or
    EZRegex chain, **not** a list. Also optionally accepts the `type` parameter,
    which works like this: \"Match any `type` other than `input`\". For example,
    \"match any word which is not foo\". Do note that this function is new, and
    I'm still working out the kinks."""

def each(*inputs:InputType) -> EZRegex:
    """ Matches if the next part of the string can match all of the given inputs. Like the + operator, but out of order."""

"Group: Conditionals"
def if_proceded_by(input:InputType) -> EZRegex:
    """ Matches the pattern if it has `input` coming after it. Can only be used once in a given pattern,
        as it only applies to the end """

def if_not_proceded_by(input:InputType) -> EZRegex:
    """ Matches the pattern if it does **not** have `input` coming after it. Can only be used once in
        a given pattern, as it only applies to the end """

def if_preceded_by(input:InputType) -> EZRegex:
    """ Matches the pattern if it has `input` coming before it. Can only be used once in a given pattern,
        as it only applies to the beginning """

def if_not_preceded_by(input:InputType) -> EZRegex:
    """ Matches the pattern if it does **not** have `input` coming before it. Can only be used once
        in a given pattern, as it only applies to the beginning """

def if_enclosed_with(open:str, stuff:InputType, close:str|None=None) -> EZRegex:
    """ Matches if the string has `open`, then `stuff`, then `close`, but only \"matches\"
        stuff. Just a convenience combination of ifProceededBy and ifPreceededBy.
    """

"Group: Grouping"
def group(input:InputType, name:str|None=None) -> EZRegex:
    "Causes `input` to be captured as an unnamed group. Only useful when replacing regexs"

def passive_group(input:InputType) -> EZRegex:
    "As all regexs in EZRegex capture passively, this is entirely useless. But if you really want to, here it is"

def earlier_group(num_or_name:int|str) -> EZRegex:
    """ Matches whatever the group referenced by `num_or_name` matched earlier. Must be *after* a
    group which would match `num_or_name`. """

def if_exists(num_or_name:int|str, does:InputType, doesnt:InputType|None=None) -> EZRegex:
    """ Matches `does` if the group `num_or_name` exists, otherwise it matches `doesnt` """

"Group: Replacement"
def rgroup(num_or_name:str|int) -> EZRegex:
    """ Puts in its place the group specified, either by group number (for unnamed
        groups) or group name (for named groups). Named groups are also counted by
        number, I'm pretty sure. Groups are numbered starting from 1."""



def replace(string:str, rtn_str:bool=True) -> str:
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

"Group: Misc"
def is_exactly(input:InputType) -> EZRegex:
    "This matches the string if and only if the entire string is exactly equal to `input`"

def literal(input:InputType) -> EZRegex:
    "This is a redundant function. You should always be able to use `... + 'stuff'` just as easily as `... + literal('stuff')`"

# For adding raw regex statements without sanatizing them
def raw(regex:str) -> EZRegex:
    """ If you already have some regular regex written, and you want to incorperate
        it, this will allow you to include it without sanatizing all the backslaches
        and such, which all the other EZRegexs do automatically."""



# replace_entire.__metadata__

# ## Premade
# literally_anything = either(anything, newLine)
# signed = optional(either('-', '+')) + number
# unsigned = number
# plain_float = signed + period + optional(number)
# full_float = plain_float + optional('e' + signed)
# int_or_float = optional('-') + number + optional(period + optional(number))
# ow = optional(whitechunk)
# # Source: http://stackoverflow.com/questions/201323/ddg#201378
# email = raw(r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])")
# # Source: https://semver.org/ (at the bottom)
# version = raw(r"(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?")
# version_numbered = raw(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?")


# ## Flags
# ASCII      = EZRegex(lambda cur=...: cur, flags=RegexFlag.ASCII)
# DOTALL     = EZRegex(lambda cur=...: cur, flags=RegexFlag.DOTALL)
# IGNORECASE = EZRegex(lambda cur=...: cur, flags=RegexFlag.IGNORECASE)
# LOCALE     = EZRegex(lambda cur=...: cur, flags=RegexFlag.LOCALE)
# MULTILINE  = EZRegex(lambda cur=...: cur, flags=RegexFlag.MULTILINE)
# UNICODE    = EZRegex(lambda cur=...: cur, flags=RegexFlag.UNICODE)
# print(replace_entire.__doc__)
