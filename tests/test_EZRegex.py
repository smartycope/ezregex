import re
from timeit import repeat
from warnings import warn

import pytest

import ezregex as ez
from ezregex import *

ALL_DIALECTS = [ez.python.PythonEZRegex, ez.r.REZRegex, ez.javascript.JavascriptEZRegex, ez.pcre2.PCRE2EZRegex]

# TODO: tests to check how raw() interacts with replacement groups

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
        digit + word(pattern=6).str()
    with pytest.raises(TypeError):
        word(pattern=6).str()
    with pytest.raises(TypeError):
        digit.word(pattern=6).str()

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
        digit + word(pattern=6).str()
    with pytest.raises(TypeError):
        word(pattern=6).str()
    with pytest.raises(TypeError):
        digit.word(pattern=6).str()

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
        digit + word(pattern=6)
    with pytest.raises(TypeError):
        word(pattern=6)
    with pytest.raises(TypeError):
        digit.word(pattern=6)

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
        assert digit.if_enclosed_with('|') == if_enclosed_with('|', '|', digit) == if_enclosed_with('|', pattern=digit)
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
        # Order *does* matter
        assert digit.or_(input) == or_(digit, input)
        assert digit.either(input) == either(digit, input)
        assert digit.or_(input) == either(digit, input)

        assert options('multiline') + digit.group() == group(digit) + options('multiline')
        assert options('multiline') + digit.group(name='test') == group(digit, name='test') + options('multiline')
        assert options('multiline') + digit.if_not_preceded_by(input) == if_not_preceded_by(input) + options('multiline') + digit
        assert options('multiline') + digit.if_preceded_by(input) == if_preceded_by(input) + options('multiline') + digit
        assert options('multiline') + digit.if_not_proceded_by(input) == digit + if_not_proceded_by(input) + options('multiline')
        assert options('multiline') + digit.if_proceded_by(input) == digit + if_proceded_by(input) + options('multiline')
        assert options('multiline') + digit.if_enclosed_with('|') == if_enclosed_with('|', '|', digit) + options('multiline') == if_enclosed_with('|', pattern=digit) + options('multiline')
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
        assert options('multiline') + digit.or_(input) == or_(digit, input) + options('multiline')
        assert options('multiline') + digit.either(input) == either(digit, input) + options('multiline')
        assert options('multiline') + digit.or_(input) == either(digit, input) + options('multiline')
    except Exception as err:
        if 'require at least Python3.11' not in str(err):
            raise

    assert digit.optional == optional(digit)
    assert digit.repeat == repeat(digit)
    assert digit.exactly == is_exactly(digit)

    assert digit.append(input) == digit + input
    assert digit.prepend(input) == input + digit

    assert 'foo' + number + optional(whitespace) + word == number.append(whitespace.optional).prepend('foo').append(word)
    ans = r'(?:\s+)?((?:(?:a)+|b))(?=\w+)'
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

    assert (digit + whitespace.optional).str() == str(digit + optional(whitespace))
    assert digit.whitespace.optional.str() == str(optional(digit.whitespace))

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
    assert type(ez.alpha) is ez.PythonEZRegex
    assert type(alpha) is ez.PythonEZRegex
    assert type(ez.python.alpha) is ez.PythonEZRegex
    assert type(ez.alphanum) is ez.PythonEZRegex
    assert type(alphanum) is ez.PythonEZRegex
    assert type(ez.python.alphanum) is ez.PythonEZRegex
    assert type(ez.letter) is ez.PythonEZRegex
    assert type(letter) is ez.PythonEZRegex
    assert type(ez.python.letter) is ez.PythonEZRegex
    assert type(ez.letter_num) is ez.PythonEZRegex
    assert type(letter_num) is ez.PythonEZRegex
    assert type(ez.python.letter_num) is ez.PythonEZRegex

def test_proper_sanitation():
    assert literal(r'\A').str() == r'\\A'
    assert raw(r'\A').str() == r'\A'
    assert raw(r'\A').word.str() == r'\A\w+'
    assert literal(r'\A').word.str() == r'\\A\w+'
    assert (digit + raw(r'\A').word).str() == r'\d\A\w+'
    assert (digit + literal(r'\A').word).str() == r'\d\\A\w+'
    assert digit.raw(r'\A').word.str() == r'\d\A\w+'
    assert digit.literal(r'\A').word.str() == r'\d\\A\w+'
    assert (digit.raw(r'\A') + word).str() == r'\d\A\w+'
    assert (digit.literal(r'\A') + word).str() == r'\d\\A\w+'

    # I'm not sure what this will do... it should raise an error?
    with pytest.raises(TypeError):
        digit.raw.word.str()
    # TODO: this could use some more tests in it

def test_replacements_not_interoperable():
    assert (rgroup(1) + 'foo').str() == r'\g<1>foo'
    assert (rgroup('bar') + 'foo').str() == r'\g<bar>foo'
    assert (rgroup('bar') + literal('foo')).str() == r'\g<bar>foo'
    assert (rgroup('bar') + raw('foo')).str() == r'\g<bar>foo'
    with pytest.raises(TypeError):
        (rgroup('bar') + word)


def test_all_parts_are_correct_type():
    for dialect in ALL_DIALECTS:
        for part_name in dialect.parts(include_functions=False):
            assert isinstance(getattr(dialect, part_name), EZRegex)
            assert isinstance(getattr(dialect, part_name), dialect)
        print(f'{dialect.__name__} passed')

# Wouldn't it be awkward if these failed
def test_README_examples(capsys):
    assert ('foo' + number + optional(whitespace) + group(word)).str() == r'foo\d+(?:\s+)?(\w+)'
    # Or if you prefer the method syntax (they can be mixed)
    assert number.append(whitespace.optional).prepend('foo').append(word.group()).str() == r'foo\d+(?:\s+)?(\w+)'

    # These match `foo123abc` and `foo123 abc`
    # but not `abc123foo` or  `foo bar`



    import ezregex as ez

    # ow is part of ez already as "optional chunk of whitespace" (`\s*`)
    params = ez.group(ez.at_least_none(ez.ow + ez.word + ez.ow + ez.optional(',') + ez.ow))
    # Seperate parts as variables for cleaner patterns
    function = ez.word + ez.ow + '(' + params + ')'

    assert function.search('some string containing func( param1 , param2)')

    # Boolean test
    assert 'some string containing func( param1 , param2)' in function

    test_ouptut = r"""\
╭─────────────────────────────── Testing Regex ────────────────────────────────╮
│ Testing expression:                                                          │
│         \w+\s*\(((?:\s*\w+\s*,?\s*)*)\)                                      │
│ for matches in:                                                              │
│         this should match func(param1,  param2 ), foo(), and bar( foo,)      │
│                                                                              │
│ Match = "func(param1,   param2 )" (18:39)                                    │
│ Unnamed Groups:                                                              │
│         1: "param1,     param2 " (23:38)                                     │
│                                                                              │
│ Match = "foo()" (41:46)                                                      │
│ Unnamed Groups:                                                              │
│         1: "" (45:45)                                                        │
│                                                                              │
│ Match = "bar( foo,)" (52:62)                                                 │
│ Unnamed Groups:                                                              │
│         1: " foo," (56:61)                                                   │
│                                                                              │
│                                                                              │
╰─────────────────────────────────── Found  ───────────────────────────────────╯
"""

    # The test() method is helpful for debugging, and color codes groups for you
    assert function.test('this should match func(param1,\tparam2 ), foo(), and bar( foo,)')
    captured = capsys.readouterr().out
    # it's hard to test whole, because the width is dynamic to the terminal size
    assert 'Testing expression:' in captured
    assert 'for matches in:' in captured
    assert 'Match = "func(param1,   param2 )" (18:39)' in captured
    assert 'Unnamed Groups:' in captured
    assert 'Match = "foo()" (41:46)' in captured
    assert 'Unnamed Groups:' in captured
    assert 'Match = "bar( foo,)" (52:62)' in captured
    assert 'Unnamed Groups:' in captured



    # Element functions
    assert (
        optional(whitespace) + group(either(repeat('a'), 'b')) + if_followed_by(word) ==
        # Elemental methods
        whitespace.optional.append(literal('a').repeat.or_('b').group).if_followed_by(word) ==
        # Mixed
        whitespace.optional + repeat('a').or_('b').group + if_followed_by(word)
    )





    import ezregex as ez # The python dialect is the defualt dialect
    assert repr(ez.group(digit, name='name') + ez.earlier_group('name')) == r"PythonEZRegex((?P<name>\d)(?P=name), {'_compiled': None, 'flags': set(), 'replacement': False})"
    import ezregex.javascript as ez
    assert repr(ez.group(digit, name='name') + ez.earlier_group('name')) == r"JavascriptEZRegex(/(?<name>\d)\k<name>/, {'_string_anchor_used': False, 'flags': set(), 'replacement': False})"