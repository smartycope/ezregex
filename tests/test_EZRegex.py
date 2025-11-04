import re
from timeit import repeat

import pytest

import ezregex as er
from ezregex import *


def test_basic():
    assert literal('test') == 'test'

def test_basic_concat():
    assert str(literal('test') + digit) == r'test\d'
    assert str('test' + digit) == r'test\d'

def test_access_dialect():
    assert type(literal('thing')) is PythonEZRegex

def test_psuedonyms():
    assert er.matchMax(digit) == er.match_max(digit)
    assert matchMax(digit) == match_max(digit)


def test_immutability():
    with pytest.raises(TypeError):
        digit.flags = 'ab'
    with pytest.raises(TypeError):
        digit.compile = lambda: ...
    with pytest.raises(TypeError):
        del digit.compile
    with pytest.raises(TypeError):
        del digit.flags

def test_test_method():
    return
    # ow = optional(whitechunk)
    params = er.group(er.atLeastNone(er.ow + er.word + er.ow + er.optional(',') + er.ow))
    function = er.word + er.ow + '(' + params + ')'
    function.test('this should match func(param1, param2 ), foo(), and bar( foo,)')

    r = 'group 1' + ':' + ow + group('stuff') + ' | ' + 'group ' + number + ': ' + group('things') + ' | ' + 'named group "' + word + '": '  + named_group('foo', 'bar')
    s = 'random stuff! and then group 1: stuff | group 2: things | named group "foo": bar  \t oh and then more random stuff'
    r.test(s)

    s = 'word1 word2 word3'
    word.test(s)

    (word + whitechunk + group('func') + ':' + group(anyof('8', '7')), 'test').test()

    # This is actually accurate, if you think about it.
    # ifFollowedBy(word).test("literal(hllow) + isExactly('thing')")# fails in _matchJSON()

    ('(' + +(anything + optional(group(comma))) + ')').test()# -- empty groups print as None

    group(+group(number) + group(anyof('98'))).test('999')

def test_no_parameters_to_chains():
    # This is sort of conceptually impossible, ish
    # with pytest.raises(TypeError):
    #     digit(6)
    # with pytest.raises(TypeError):
    #     digit(input=6)
    with pytest.raises(TypeError):
        (digit + word)(6)
    with pytest.raises(TypeError):
        (digit + word)(input=6)
    # This is also conceptually impossible without a moderate refactor
    # with pytest.raises(TypeError):
    #     match_amt(6, digit)(6)
    # with pytest.raises(TypeError):
    #     match_amt(6, digit)(input=6)

    assert match_amt(6, digit)()
    assert (digit + word)()
    assert digit()

def test_re_shadow_funcs():
    s = r'\d(\w+)'
    string = 'timmy is 6years old'
    repl = replace('number {1}')

    def eq(a, b):
        if not ((a is None) == (b is None)) and a.span() == b.span() and a.groups() == b.groups():
            raise AssertionError(f'{a} != {b}')

    eq((digit + group(word)).search(string),      re.compile(s).search(string))
    eq((digit + group(word)).match(string),       re.compile(s).match(string))
    eq((digit + group(word)).fullmatch(string),   re.compile(s).fullmatch(string))
    eq((digit + group(word)).split(string),       re.compile(s).split(string))
    eq((digit + group(word)).findall(string),     re.compile(s).findall(string))
    eq((digit + group(word)).finditer(string),    re.compile(s).finditer(string))
    eq((digit + group(word)).sub(repl, string),   re.compile(s).sub(repl, string))
    eq((digit + group(word)).subn(repl, string),  re.compile(s).subn(repl, string))

def test_flag_methods():
    assert (digit + ASCII).flags == 'a'
    with pytest.raises(TypeError):
        digit.flags = 'L'
    assert digit.flags == ''
    a = digit.set_flags('asL')
    assert a.flags == 'asL'
    assert (digit + ASCII).add_flag('L').flags == 'aL'
    assert (digit + ASCII).remove_flag('a').flags == ''
    assert (digit + ASCII).remove_flag('L').flags == 'a'

def test_elemental_methods():
    input = word
    min = 1
    max = 3
    try:
        assert digit.group() == group(digit) == digit.unnamed
        assert digit.group('test') == group(digit, 'test') == digit.named('test')
        assert digit.if_not_preceded_by(input) == if_not_preceded_by(input) + digit
        assert digit.if_preceded_by(input) == if_preceded_by(input) + digit
        assert digit.if_not_proceded_by(input) == digit + if_not_proceded_by(input)
        assert digit.if_proceded_by(input) == digit + if_proceded_by(input)
        assert digit.if_enclosed_with('|') == if_enclosed_with(digit, '|')
        assert digit.if_enclosed_with('(', ')') == if_enclosed_with(digit, '(', ')')
        assert digit.at_least(min) == at_least(min, digit)
        assert digit.more_than(min) == more_than(min, digit)
        assert digit.amt(2) == match_num(2, digit)
        assert digit.at_most(max) == at_most(max, digit)
        assert digit.between(min, max) == between(min, max, digit)
        assert digit.between(min, max, greedy=False) == between(min, max, digit, greedy=False)
        assert digit.between(min, max, possessive=True) == between(min, max, digit, possessive=True)
        assert digit.at_least_one() == at_least_one(digit)
        assert digit.at_least_one(greedy=False) == at_least_one(digit, greedy=False)
        assert digit.at_least_one(possessive=True) == at_least_one(digit, possessive=True)
        assert digit.at_least_none() == at_least_none(digit)
        assert digit.at_least_none(greedy=False) == at_least_none(digit, greedy=False)
        assert digit.at_least_none(possessive=True) == at_least_none(digit, possessive=True)
        assert digit.or_(input) == either(digit, input)

        assert MULTILINE + digit.group() == group(digit) + MULTILINE
        assert MULTILINE + digit.group('test') == group(digit, 'test') + MULTILINE
        assert MULTILINE + digit.if_not_preceded_by(input) == if_not_preceded_by(input) + MULTILINE + digit
        assert MULTILINE + digit.if_preceded_by(input) == if_preceded_by(input) + MULTILINE + digit
        assert MULTILINE + digit.if_not_proceded_by(input) == digit + if_not_proceded_by(input) + MULTILINE
        assert MULTILINE + digit.if_proceded_by(input) == digit + if_proceded_by(input) + MULTILINE
        assert MULTILINE + digit.if_enclosed_with('|') == if_enclosed_with(digit, '|') + MULTILINE
        assert MULTILINE + digit.if_enclosed_with('(', ')') == if_enclosed_with(digit, '(', ')') + MULTILINE
        assert MULTILINE + digit.at_least(min) == at_least(min, digit) + MULTILINE
        assert MULTILINE + digit.more_than(min) == more_than(min, digit) + MULTILINE
        assert MULTILINE + digit.amt(2) == match_num(2, digit) + MULTILINE
        assert MULTILINE + digit.at_most(max) == at_most(max, digit) + MULTILINE
        assert MULTILINE + digit.between(min, max) == between(min, max, digit) + MULTILINE
        assert MULTILINE + digit.between(min, max, greedy=False) == between(min, max, digit, greedy=False) + MULTILINE
        assert MULTILINE + digit.between(min, max, possessive=True) == between(min, max, digit, possessive=True) + MULTILINE
        assert MULTILINE + digit.at_least_one() == at_least_one(digit) + MULTILINE
        assert MULTILINE + digit.at_least_one(greedy=False) == at_least_one(digit, greedy=False) + MULTILINE
        assert MULTILINE + digit.at_least_one(possessive=True) == at_least_one(digit, possessive=True) + MULTILINE
        assert MULTILINE + digit.at_least_none() == at_least_none(digit) + MULTILINE
        assert MULTILINE + digit.at_least_none(greedy=False) == at_least_none(digit, greedy=False) + MULTILINE
        assert MULTILINE + digit.at_least_none(possessive=True) == at_least_none(digit, possessive=True) + MULTILINE
        assert MULTILINE + digit.or_(input) == either(digit, input) + MULTILINE
    # I usually run tests in Python3.12, so I'm just gonna disable all these tests for Python3.10 (since I have automated
    # tests run in Python3.10, and 3.10 doesn't support possessive or greedy regex operators)
    except Exception as err:
        if 'require at least Python3.11' not in str(err):
            raise err

    assert digit.optional == optional(digit)
    assert digit.repeat == repeat(digit)
    assert digit.exactly == is_exactly(digit)

    assert digit.ASCII == digit + ASCII
    assert digit.IGNORECASE == digit + IGNORECASE
    assert digit.DOTALL == digit + DOTALL
    assert digit.LOCALE == digit + LOCALE
    assert digit.MULTILINE == digit + MULTILINE

    assert digit.append(input) == digit + input
    assert digit.prepend(input) == input + digit

    assert digit.append(input).ASCII == digit + ASCII + input
    assert digit.prepend(input).ASCII == input + digit + ASCII

    assert 'foo' + number + optional(whitespace) + word == number.append(whitespace.optional).prepend('foo').append(word)
    assert (
        optional(whitespace) + group(either(repeat('a'), 'b')) + if_followed_by(word) ==
        whitespace.optional.append(literal('a').repeat.or_('b').unnamed).if_followed_by(word) ==
        whitespace.optional + repeat('a').or_('b').unnamed + if_followed_by(word)
    )


def test_no_duplicate_flags():
    r = lineStart + word + '/' + '/' + lineEnd
    assert r.str() == r'(?m)^\w+//$'
