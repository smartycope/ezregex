import pytest

import ezregex as er
from ezregex import *
from ezregex import EZRegex, python


def test_no_empty_strings():
    with pytest.raises(ValueError):
        str(group('', name='i') + optional(digit))

    with pytest.raises(ValueError):
        str(match_max(group('')))

    with pytest.raises(ValueError):
        str(amt(2, ''))

    with pytest.raises(ValueError):
        str(group('abc', name=''))


def test_any_of():
    # """ _any_of_func """
    assert er.anyof('aiLmsux', split=True, chars=True)._compile(False) == "[aiLmsux]", \
        f"Was supposed to be '[aiLmsux]', was actually '{er.anyof('aiLmsux', split=True, chars=True)._compile(False)}'"
    # assert er.anyof('aiLmsux', split=False, chars=True)._compile(False) == Error, \
    #   f"Was supposed to be 'Error', was actually '{er.anyof('aiLmsux', split=False, chars=True)._compile(False)}'"
    assert er.anyof('aiLmsux', split=None, chars=True)._compile(False) == "[aiLmsux]", \
        f"Was supposed to be '[aiLmsux]', was actually '{er.anyof('aiLmsux', split=None, chars=True)._compile(False)}'"
    assert er.anyof('aiLmsux', split=True, chars=False)._compile(False) == '(?:a|i|L|m|s|u|x)', \
        f"Was supposed to be '(?:a|i|L|m|s|u|x)', was actually '{er.anyof('aiLmsux', split=True, chars=False)._compile(False)}'"
    # assert er.anyof('aiLmsux', split=False, chars=False)._compile(False) == Error, \
    #   f"Was supposed to be 'Error', was actually '{er.anyof('aiLmsux', split=False, chars=False)._compile(False)}'"
    assert er.anyof('aiLmsux', split=None, chars=False)._compile(False) == '(?:a|i|L|m|s|u|x)', \
        f"Was supposed to be '(?:a|i|L|m|s|u|x)', was actually '{er.anyof('aiLmsux', split=None, chars=False)._compile(False)}'"
    assert er.anyof('aiLmsux', split=True, chars=None)._compile(False) == '(?:a|i|L|m|s|u|x)', \
        f"Was supposed to be '(?:a|i|L|m|s|u|x)', was actually '{er.anyof('aiLmsux', split=True, chars=None)._compile(False)}'"
    # assert er.anyof('aiLmsux', split=False, chars=None)._compile(False) == Error, \
    #   f"Was supposed to be 'Error', was actually '{er.anyof('aiLmsux', split=False, chars=None)._compile(False)}'"
    assert er.anyof('aiLmsux', split=None, chars=None)._compile(False) == "[aiLmsux]", \
        f"Was supposed to be '[aiLmsux]', was actually '{er.anyof('aiLmsux', split=None, chars=None)._compile(False)}'"

    # assert er.anyof(*list('aiLmsux'), split=True, chars=True)._compile(False) == Error, \
    #   f"Was supposed to be 'Error', was actually '{er.anyof(*list('aiLmsux'), split=True, chars=True)._compile(False)}'"
    assert er.anyof(*list('aiLmsux'), split=False, chars=True)._compile(False) == "[aiLmsux]", \
        f"Was supposed to be '[aiLmsux]', was actually '{er.anyof(*list('aiLmsux'), split=False, chars=True)._compile(False)}'"
    assert er.anyof(*list('aiLmsux'), split=None, chars=True)._compile(False) == "[aiLmsux]", \
        f"Was supposed to be '[aiLmsux]', was actually '{er.anyof(*list('aiLmsux'), split=None, chars=True)._compile(False)}'"
    # assert er.anyof(*list('aiLmsux'), split=True, chars=False)._compile(False) == Error, \
    #   f"Was supposed to be 'Error', was actually '{er.anyof(*list('aiLmsux'), split=True, chars=False)._compile(False)}'"
    assert er.anyof(*list('aiLmsux'), split=False, chars=False)._compile(False) == '(?:a|i|L|m|s|u|x)', \
        f"Was supposed to be '(?:a|i|L|m|s|u|x)', was actually '{er.anyof(*list('aiLmsux'), split=False, chars=False)._compile(False)}'"
    assert er.anyof(*list('aiLmsux'), split=None, chars=False)._compile(False) == '(?:a|i|L|m|s|u|x)', \
        f"Was supposed to be '(?:a|i|L|m|s|u|x)', was actually '{er.anyof(*list('aiLmsux'), split=None, chars=False)._compile(False)}'"
    # assert er.anyof(*list('aiLmsux'), split=True, chars=None)._compile(False) == Error, \
    #   f"Was supposed to be 'Error', was actually '{er.anyof(*list('aiLmsux'), split=True, chars=None)._compile(False)}'"
    assert er.anyof(*list('aiLmsux'), split=False, chars=None)._compile(False) == "[aiLmsux]", \
        f"Was supposed to be '[aiLmsux]', was actually '{er.anyof(*list('aiLmsux'), split=False, chars=None)._compile(False)}'"
    assert er.anyof(*list('aiLmsux'), split=None, chars=None)._compile(False) == "[aiLmsux]", \
        f"Was supposed to be '[aiLmsux]', was actually '{er.anyof(*list('aiLmsux'), split=None, chars=None)._compile(False)}'"


def test_any_char_except():
    # """ _any_char_except_func """
    assert er.any_char_except('abcd')._compile(False) == '[^abcd]'
    assert er.any_char_except(*list('abcd'))._compile(False) == '[^abcd]'



def test_misc():
    """ Just threw a bunch of stuff in here for now, I need to move it elsewhere eventually """
    a = word + ow
    # b = stuff + UNICODE
    c = IGNORECASE + '9'
    assert a + c == word + ow + IGNORECASE + '9', f"{a + c} != {word + ow + IGNORECASE + '9'}"

    a = str(PythonEZRegex(r'\s+'))
    with pytest.raises(TypeError):
        b = str(PythonEZRegex(raw(r'\s+')))
    c = r'\s+'
    d = str(raw(r'\s+'))
    # e = str(whitespace + matchMax)
    assert a == c == d, f'\na: {a}\n c: {c}\n d: {d}\n e: {e}'
    # assert (word + ow + anything + ':').test('word    d:', show=False)
    # assert not (word + ow + anything + ':').test('word', show=False)
    assert 'word    d:' in (word + ow + anything + ':')

    test = word + chunk
    test += word
    assert str(test) == str(word + chunk + word), f"{str(test)} != {str(word + chunk + word)}"
    assert test == word + chunk + word
    assert either('(' + word + ')', '.') == either(er.literal('(') + word() + er.literal(')'), '.'), f"{either('(' + word + ')', '.')} != {either(er.literal('(') + word() + er.literal(')'), '.')}"
    assert str(er.ifFollowedBy(word)) == r'(?=\w+)'

    #TODO: assert (word + ow + anything + ':') in 'word    d:'
    #TODO: assert (word + ow + anything + ':') not in 'word'
    assert str(word) == r'\w+', f'{word}'
