import re

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
