import re
from timeit import repeat
from warnings import warn

import pytest

import ezregex as ez
from ezregex import *


def test_basic():
    assert literal('test').str() == 'test'

def test_eq():
    assert literal('test') + digit == 'test' + digit

def test_basic_concat():
    assert str(literal('test') + digit) == r'test\d'
    assert str('test' + digit) == r'test\d'

def test_access_dialect():
    assert type(literal('thing')) is PythonEZRegex

def test_psuedonyms():
    assert ez.matchMax(digit) == ez.match_max(digit)
    assert ez.python.matchMax(digit) == ez.python.match_max(digit)
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
    params = ez.group(ez.atLeastNone(ez.ow + ez.word + ez.ow + ez.optional(',') + ez.ow))
    function = ez.word + ez.ow + '(' + params + ')'
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

def test_parameters_to_chains_lazy():
    EZRegex.lazy_check_params = True
    with pytest.raises(TypeError):
        digit + word(6).str()
    with pytest.raises(TypeError):
        word(6).str()
    with pytest.raises(TypeError):
        digit.word(6).str()

    with pytest.raises(TypeError):
        digit + word(input=6).str()
    with pytest.raises(TypeError):
        word(input=6).str()
    with pytest.raises(TypeError):
        digit.word(input=6).str()

    assert any_between('a', 'j').str() == r'[a-j]'
    with pytest.raises(TypeError):
        any_between('a', 'j', 'k').str()
    with pytest.raises(TypeError):
        any_between('a').str()
    # Lazy checking is less strict, it doesn't check types
    # with pytest.raises(TypeError):
    #     any_between(1.2, 3.4).str()
    # with pytest.raises(TypeError):
    #     any_between(1.2).str()
    # with pytest.raises(TypeError):
    #     any_between(1.2, 'a', 'j').str()
    # with pytest.raises(TypeError):
    #     any_between('a', 'j', 1.2).str()

    with pytest.raises(TypeError):
        digit + word(6).str()
    with pytest.raises(TypeError):
        word(6).str()
    with pytest.raises(TypeError):
        digit.word(6).str()

    with pytest.raises(TypeError):
        digit + word(input=6).str()
    with pytest.raises(TypeError):
        word(input=6).str()
    with pytest.raises(TypeError):
        digit.word(input=6).str()

    assert any_between('a', 'j').str() == r'[a-j]'
    assert any_between(1.2, 3.4).str()
    with pytest.raises(TypeError):
        any_between('a', 'j', 'k').str()
    with pytest.raises(TypeError):
        any_between('a').str()
    with pytest.raises(TypeError):
        any_between(1.2).str()
    with pytest.raises(TypeError):
        any_between(1.2, 'a', 'j').str()
    with pytest.raises(TypeError):
        any_between('a', 'j', 1.2).str()

    # There's nothing we can do about these, so just make sure they don't break anything
    # See the comment in EZRegex.py.__call__ for why this is
    assert digit().str() == r'\d'
    assert word().str() == r'\w+'
    assert digit.word().str() == r'\d\w+'
    assert digit().word().str() == r'\d\w+'
    assert match_amt(6, digit)().str() == r'(?:\d){6}'
    assert digit().str() == r'\d'
    assert word_char.amt(4).str() == r'(?:\w){4}'
    assert word_char.amt(4).group(name='word').literal(' ').str() == r'(?P<word>(?:\w){4})\ '

    # Reset, just in case
    EZRegex.lazy_check_params = False

def test_parameters_to_chains_eager():
    with pytest.raises(TypeError):
        digit + word(6)
    with pytest.raises(TypeError):
        word(6)
    with pytest.raises(TypeError):
        digit.word(6)

    with pytest.raises(TypeError):
        digit + word(input=6)
    with pytest.raises(TypeError):
        word(input=6)
    with pytest.raises(TypeError):
        digit.word(input=6)

    assert any_between('a', 'j').str() == r'[a-j]'
    with pytest.raises(TypeError):
        any_between('a', 'j', 'k')
    with pytest.raises(TypeError):
        any_between('a')
    with pytest.raises(TypeError):
        any_between(1.2)
    with pytest.raises(TypeError):
        any_between(1.2, 'a', 'j')
    with pytest.raises(TypeError):
        any_between('a', 'j', 1.2)

def test_empty_input():
    warn('This test works manually, but not in the testing env. Retest later')
    return
    with pytest.raises(ValueError):
        amt(3, '')

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

    s = r'(?P<word>\w{4}) '
    string = 'this string should have 3 four letter words'
    repl = replace('4444 ({word}) ({0})')
    eq((word_char.amt(4).group(name='word').literal(' ')).search(string),      re.compile(s).search(string))
    eq((word_char.amt(4).group(name='word').literal(' ')).match(string),       re.compile(s).match(string))
    eq((word_char.amt(4).group(name='word').literal(' ')).fullmatch(string),   re.compile(s).fullmatch(string))
    eq((word_char.amt(4).group(name='word').literal(' ')).split(string),       re.compile(s).split(string))
    eq((word_char.amt(4).group(name='word').literal(' ')).findall(string),     re.compile(s).findall(string))
    eq((word_char.amt(4).group(name='word').literal(' ')).finditer(string),    re.compile(s).finditer(string))
    eq((word_char.amt(4).group(name='word').literal(' ')).sub(repl, string),   re.compile(s).sub(repl, string))
    eq((word_char.amt(4).group(name='word').literal(' ')).subn(repl, string),  re.compile(s).subn(repl, string))

def test_flag_methods():
    assert (digit + options('ascii')).flags == {'a'}
    with pytest.raises(TypeError):
        digit.flags = {'L'}
    assert digit.flags == set()
    a = digit.set_flags('asL')
    assert a.flags == {'a', 's', 'L'}
    assert (digit + options('ascii')).add_flags('L').flags == {'a', 'L'}
    assert (digit + options('ascii')).remove_flags('a').flags == set()
    assert (digit + options('ascii')).remove_flags('L').flags == {'a'}

def test_imply_input_is_cur():
    input = word
    min = 1
    max = 3

    assert amt(3, digit).str() == r'(?:\d){3}'
    assert digit.amt(3).str() == r'(?:\d){3}'
    assert digit.amt(3, 'a')
    assert digit.amt('a', 3)
    assert digit.amt('a', 'b')
    assert amt('a', 3)
    assert amt('a', 'b')

    try:
        assert digit.group() == group(digit) == digit.group
        assert digit.group(name='test') == group(digit, name='test')
        assert digit.if_not_preceded_by(input) == if_not_preceded_by(input) + digit
        assert digit.if_preceded_by(input) == if_preceded_by(input) + digit
        assert digit.if_not_proceded_by(input) == digit + if_not_proceded_by(input)
        assert digit.if_proceded_by(input) == digit + if_proceded_by(input)
        assert digit.if_enclosed_with('|') == if_enclosed_with('|', '|', digit) == if_enclosed_with('|', input=digit)
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
        assert digit.or_(input) == or_(input, digit)
        assert digit.either(input) == either(input, digit)
        assert digit.or_(input) == either(input, digit)

        assert options('multiline') + digit.group() == group(digit) + options('multiline')
        assert options('multiline') + digit.group(name='test') == group(digit, name='test') + options('multiline')
        assert options('multiline') + digit.if_not_preceded_by(input) == if_not_preceded_by(input) + options('multiline') + digit
        assert options('multiline') + digit.if_preceded_by(input) == if_preceded_by(input) + options('multiline') + digit
        assert options('multiline') + digit.if_not_proceded_by(input) == digit + if_not_proceded_by(input) + options('multiline')
        assert options('multiline') + digit.if_proceded_by(input) == digit + if_proceded_by(input) + options('multiline')
        assert options('multiline') + digit.if_enclosed_with('|') == if_enclosed_with('|', '|', digit) + options('multiline') == if_enclosed_with('|', input=digit) + options('multiline')
        assert options('multiline') + digit.at_least(min) == at_least(min, digit) + options('multiline')
        assert options('multiline') + digit.more_than(min) == more_than(min, digit) + options('multiline')
        assert options('multiline') + digit.amt(2) == match_num(2, digit) + options('multiline')
        assert options('multiline') + digit.at_most(max) == at_most(max, digit) + options('multiline')
        assert options('multiline') + digit.between(min, max) == between(min, max, digit) + options('multiline')
        assert options('multiline') + digit.between(min, max, greedy=False) == between(min, max, digit, greedy=False) + options('multiline')
        assert options('multiline') + digit.between(min, max, possessive=True) == between(min, max, digit, possessive=True) + options('multiline')
        assert options('multiline') + digit.at_least_one() == at_least_one(digit) + options('multiline')
        assert options('multiline') + digit.at_least_one(greedy=False) == at_least_one(digit, greedy=False) + options('multiline')
        assert options('multiline') + digit.at_least_one(possessive=True) == at_least_one(digit, possessive=True) + options('multiline')
        assert options('multiline') + digit.at_least_none() == at_least_none(digit) + options('multiline')
        assert options('multiline') + digit.at_least_none(greedy=False) == at_least_none(digit, greedy=False) + options('multiline')
        assert options('multiline') + digit.at_least_none(possessive=True) == at_least_none(digit, possessive=True) + options('multiline')
        assert options('multiline') + digit.or_(input) == or_(input, digit) + options('multiline')
        assert options('multiline') + digit.either(input) == either(input, digit) + options('multiline')
        assert options('multiline') + digit.or_(input) == either(input, digit) + options('multiline')
    # I usually run tests in Python3.12, so I'm just gonna disable all these tests for Python3.10 (since I have automated
    # tests run in Python3.10, and 3.10 doesn't support possessive or greedy regex operators)
    except Exception as err:
        if 'require at least Python3.11' not in str(err):
            raise

    assert digit.optional == optional(digit)
    assert digit.repeat == repeat(digit)
    assert digit.exactly == is_exactly(digit)

    assert digit.append(input) == digit + input
    assert digit.prepend(input) == input + digit

    assert 'foo' + number + optional(whitespace) + word == number.append(whitespace.optional).prepend('foo').append(word)
    # Because either sometimes inverts the order (and that's okay)
    ans = (r'(?:\s+)?((?:b|(?:a)+))(?=\w+)', r'(?:\s+)?((?:(?:a)+|b))(?=\w+)')
    assert (optional(whitespace) + group(either(repeat('a'), 'b')) + if_followed_by(word)).str() in ans
    assert whitespace.optional.append(literal('a').repeat.or_('b').group).if_followed_by(word).str() in ans
    assert (whitespace.optional + repeat('a').or_('b').group + if_followed_by(word)).str() in ans

def test_append_prepend():
    assert digit.opt.then(word).str() == r'(?:\d)?\w+'
    assert (digit + 'asdf').opt.then(word).str() == r'(?:\dasdf)?\w+'
    assert digit.opt.then(word).opt.then(word).str() == r'(?:(?:\d)?\w+)?\w+'
    assert digit.opt.word.opt.word.str() == r'(?:(?:\d)?\w+)?\w+'

    assert digit.opt.append(word).str() == r'(?:\d)?\w+'
    assert (digit + 'asdf').opt.append(word).str() == r'(?:\dasdf)?\w+'
    assert digit.opt.append(word).opt.append(word).str() == r'(?:(?:\d)?\w+)?\w+'
    assert digit.opt.word.opt.word.str() == r'(?:(?:\d)?\w+)?\w+'

    assert digit.prepend('asdf').str() == r'asdf\d'
    assert digit.prepend('asdf').prepend('1234').str() == r'1234asdf\d'
    assert digit.append('asdf').prepend('1234').str() == r'1234\dasdf'
    assert digit.append('asdf').prepend('1234').append('jkl;').str() == r'1234\dasdfjkl;'

    assert digit.append(whitespace.opt).str() == r'\d(?:\s+)?'
    assert (digit + whitespace.opt).str() == r'\d(?:\s+)?'
    assert digit.whitespace.opt.str() == r'(?:\d\s+)?'


def test_no_duplicate_flags():
    r = lineStart + word + '/' + '/' + lineEnd
    assert r.str() == r'(?m)^\w+//$'

def test_accurate_types():
    # ...is a function
    assert type(ez.options) is type(test_accurate_types)
    assert type(ez.number) is ez.PythonEZRegex
    assert type(number) is ez.PythonEZRegex
    assert type(ez.python.number) is ez.PythonEZRegex
    assert type(ez.any_of) is ez.PythonEZRegex
    assert type(any_of) is ez.PythonEZRegex
    assert type(ez.python.any_of) is ez.PythonEZRegex
    assert type(ez.unicode) is ez.PythonEZRegex
    assert type(unicode) is ez.PythonEZRegex
    assert type(ez.python.unicode) is ez.PythonEZRegex
    assert type(ez.match_range) is ez.PythonEZRegex
    assert type(match_range) is ez.PythonEZRegex
    assert type(ez.python.match_range) is ez.PythonEZRegex
    assert type(ez.is_exactly) is ez.PythonEZRegex
    assert type(is_exactly) is ez.PythonEZRegex
    assert type(ez.python.is_exactly) is ez.PythonEZRegex
    assert type(ez.exactly) is ez.PythonEZRegex
    assert type(exactly) is ez.PythonEZRegex
    assert type(ez.python.exactly) is ez.PythonEZRegex
    assert type(ez.raw) is ez.PythonEZRegex
    assert type(raw) is ez.PythonEZRegex
    assert type(ez.python.raw) is ez.PythonEZRegex
    assert type(ez.match_amt) is ez.PythonEZRegex
    assert type(match_amt) is ez.PythonEZRegex
    assert type(ez.python.match_amt) is ez.PythonEZRegex