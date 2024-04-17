import pytest
from ezregex import *


def test_access_dialect():
    assert literal('thing').dialect == 'python'

def test_no_change_dialect():
    with pytest.raises(TypeError):
        digit.dialect = 'asdf'


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
