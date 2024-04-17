strictness=20
dontIncludePassed=True
invertBackend='re_parser'
invert_tries=1
import random
import re

import pytest
from ezregex import *
import jstyleson
import ezregex as er
offset = 2


def test_invert():
    import ezregex as er
    regex = (er.digit + er.word)
    assert re.search(regex.str(), ~regex)

def test_not():
    # Not sure why this doesn't work?...
    with pytest.raises(NotImplementedError):
        not anything

# TODO: Finish this
# assert digit * ... == matchMax(digit)

# TODO: Debug this
# assert digit | word == anyof(digit, word), f"{digit | word} != {anyof(digit, word)}"
# assert 7 | digit == anyof(7, digit), f"{7 | digit} != {anyof(digit, 7)}"
# assert re.search(str(digit | word | '1'), '1') == re.search(anyof(digit, word, 1).str(), '1')

def test_unary_plus():
    assert +digit == matchMax(digit)

def test_concat_operators():
    assert anything + word == anything << word
    assert anything + word == anything >> word

def test_square_brackets():
    assert digit[2, 3] == match_range(2, 3, digit)
    assert digit[2, ...] == digit[2,] == digit[2, None] == digit[2] == match_at_least(2, digit)
    assert digit[..., 2] == digit[0, 2] == digit[None, 2] == match_at_most(2, digit)
    assert digit[...] == digit[0, ...] == digit[None] == at_least_0(digit)
    assert digit[1, ...] == digit[1] == digit[1,] == digit[1, None] == at_least_1(digit)
    # expr[...:end_expr] is equivalent to ZeroOrMore(expr, stop_on=end_expr)
    # assert digit[...:'foo'] == digit[None:'foo'] == digit[,'foo'] ==

def test_iadd():
    test = digit
    test += 6
    assert test == digit + 6, f"{test} != {digit + 6}"

def test_imul():
    test = digit
    test *= 3
    assert test == digit * 3

def test_mul():
    assert 2 * digit == digit * 2

def test_mod():
    assert digit % 'sldkj' is None, f'{digit % "sldkj"} != None'
    assert digit % '77sdsf88' == re.search('77sdsf88', digit.str())

# Test f-strings
# As of right now, these may work, but won't necissarily work
# assert f'|{word}|' == '|' + word + '|'
# assert f'|{word}|{number}|' == '|' + word + '|' + number + '|'
# assert f"|{word}{number + ifFollowedBy(word)}|" == '|' + word + number + ifFollowedBy(word) + '|'
# assert f'|{rgroup("g")}|{replace_group}|' == '|' + rgroup('g') + '|' + replace_entire + '|'

# Replacement strings are, in fact, a thing
# print(version_info)

# no idea why this doesnt work.
# assert (anything + word) * 3 == '.\w+' * 3, f"'{(anything + word) * 3}' != '{'.\w+'*3}'"




# From 1-100, 1 is easy, 100 is hard
# difficulty = 1
# runTests(
# # These should remain on, for the GitHub automated tests
# singletons=True,
# _invert=False,
# replacement=True,
# operators=True,
# _generate=True,
# # These display for you to check that they look correct
# testMethod=False,
# _api=False,
# # Settings
# strictness=difficulty,
# invert_tries=101-difficulty,
# dontIncludePassed=True,
# invertBackend='re_parser',
# )
