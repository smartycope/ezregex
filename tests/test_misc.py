import pytest

import ezregex as ez
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
    assert ez.anyof('aiLmsux', split=True, chars=True)._compile(False) == "[aiLmsux]", \
        f"Was supposed to be '[aiLmsux]', was actually '{ez.anyof('aiLmsux', split=True, chars=True)._compile(False)}'"
    # assert er.anyof('aiLmsux', split=False, chars=True)._compile(False) == Error, \
    #   f"Was supposed to be 'Error', was actually '{er.anyof('aiLmsux', split=False, chars=True)._compile(False)}'"
    assert ez.anyof('aiLmsux', split=None, chars=True)._compile(False) == "[aiLmsux]", \
        f"Was supposed to be '[aiLmsux]', was actually '{ez.anyof('aiLmsux', split=None, chars=True)._compile(False)}'"
    assert ez.anyof('aiLmsux', split=True, chars=False)._compile(False) == '(?:a|i|L|m|s|u|x)', \
        f"Was supposed to be '(?:a|i|L|m|s|u|x)', was actually '{ez.anyof('aiLmsux', split=True, chars=False)._compile(False)}'"
    # assert er.anyof('aiLmsux', split=False, chars=False)._compile(False) == Error, \
    #   f"Was supposed to be 'Error', was actually '{er.anyof('aiLmsux', split=False, chars=False)._compile(False)}'"
    assert ez.anyof('aiLmsux', split=None, chars=False)._compile(False) == '(?:a|i|L|m|s|u|x)', \
        f"Was supposed to be '(?:a|i|L|m|s|u|x)', was actually '{ez.anyof('aiLmsux', split=None, chars=False)._compile(False)}'"
    assert ez.anyof('aiLmsux', split=True, chars=None)._compile(False) == '(?:a|i|L|m|s|u|x)', \
        f"Was supposed to be '(?:a|i|L|m|s|u|x)', was actually '{ez.anyof('aiLmsux', split=True, chars=None)._compile(False)}'"
    # assert er.anyof('aiLmsux', split=False, chars=None)._compile(False) == Error, \
    #   f"Was supposed to be 'Error', was actually '{er.anyof('aiLmsux', split=False, chars=None)._compile(False)}'"
    assert ez.anyof('aiLmsux', split=None, chars=None)._compile(False) == "[aiLmsux]", \
        f"Was supposed to be '[aiLmsux]', was actually '{ez.anyof('aiLmsux', split=None, chars=None)._compile(False)}'"

    # assert er.anyof(*list('aiLmsux'), split=True, chars=True)._compile(False) == Error, \
    #   f"Was supposed to be 'Error', was actually '{er.anyof(*list('aiLmsux'), split=True, chars=True)._compile(False)}'"
    assert ez.anyof(*list('aiLmsux'), split=False, chars=True)._compile(False) == "[aiLmsux]", \
        f"Was supposed to be '[aiLmsux]', was actually '{ez.anyof(*list('aiLmsux'), split=False, chars=True)._compile(False)}'"
    assert ez.anyof(*list('aiLmsux'), split=None, chars=True)._compile(False) == "[aiLmsux]", \
        f"Was supposed to be '[aiLmsux]', was actually '{ez.anyof(*list('aiLmsux'), split=None, chars=True)._compile(False)}'"
    # assert er.anyof(*list('aiLmsux'), split=True, chars=False)._compile(False) == Error, \
    #   f"Was supposed to be 'Error', was actually '{er.anyof(*list('aiLmsux'), split=True, chars=False)._compile(False)}'"
    assert ez.anyof(*list('aiLmsux'), split=False, chars=False)._compile(False) == '(?:a|i|L|m|s|u|x)', \
        f"Was supposed to be '(?:a|i|L|m|s|u|x)', was actually '{ez.anyof(*list('aiLmsux'), split=False, chars=False)._compile(False)}'"
    assert ez.anyof(*list('aiLmsux'), split=None, chars=False)._compile(False) == '(?:a|i|L|m|s|u|x)', \
        f"Was supposed to be '(?:a|i|L|m|s|u|x)', was actually '{ez.anyof(*list('aiLmsux'), split=None, chars=False)._compile(False)}'"
    # assert er.anyof(*list('aiLmsux'), split=True, chars=None)._compile(False) == Error, \
    #   f"Was supposed to be 'Error', was actually '{er.anyof(*list('aiLmsux'), split=True, chars=None)._compile(False)}'"
    assert ez.anyof(*list('aiLmsux'), split=False, chars=None)._compile(False) == "[aiLmsux]", \
        f"Was supposed to be '[aiLmsux]', was actually '{ez.anyof(*list('aiLmsux'), split=False, chars=None)._compile(False)}'"
    assert ez.anyof(*list('aiLmsux'), split=None, chars=None)._compile(False) == "[aiLmsux]", \
        f"Was supposed to be '[aiLmsux]', was actually '{ez.anyof(*list('aiLmsux'), split=None, chars=None)._compile(False)}'"


def test_any_char_except():
    # """ _any_char_except_func """
    assert ez.any_char_except('abcd')._compile(False) == '[^abcd]'
    assert ez.any_char_except(*list('abcd'))._compile(False) == '[^abcd]'


def test_misc():
    """ Just threw a bunch of stuff in here for now, I need to move it elsewhere eventually """
    a = word + ow
    # b = stuff + UNICODE
    c = options('ignore_case') + '9'
    assert a + c == word + ow + options('ignore_case') + '9', f"{a + c} != {word + ow + options('ignore_case') + '9'}"

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
    assert either('(' + word + ')', '.') == either(ez.literal('(') + word() + ez.literal(')'), '.'), f"{either('(' + word + ')', '.')} != {either(ez.literal('(') + word() + ez.literal(')'), '.')}"
    assert str(ez.ifFollowedBy(word)) == r'(?=\w+)'

    #TODO: assert (word + ow + anything + ':') in 'word    d:'
    #TODO: assert (word + ow + anything + ':') not in 'word'
    assert str(word) == r'\w+', f'{word}'


def test_options():
    assert options().str() == ''
    with pytest.raises(ValueError):
        options('notaflag')
    with pytest.raises(ValueError):
        options(notaflag=True)
    with pytest.raises(ValueError):
        options(notaflag=False)
    assert str(word + options('IGNORE_CASE')) == r'(?i)\w+'
    assert str(word + options('ignore_case')) == r'(?i)\w+'
    assert str(word + options(ignore_case=True)) == r'(?i)\w+'
    assert str(word + options(IGNORE_CASE=True)) == r'(?i)\w+'
    with pytest.raises(ValueError):
        anyof('a', 'b', 'c') + options('ignore_case') + options(IGNORE_CASE=False)


def test_docstrings():
    assert options.__doc__.strip() == """
Documentation:
        https://docs.python.org/3/library/re.html#flags

Usage:
        word + options(ignore_case=True)
        word + options('ignore_case')
        word + options('ignore_case', 'multiline')
        word + options('ignore_case', multiline=True)

    Args:
        ascii:
                Make matching words, word boundaries, digits, and whitespace perform ASCII-only matching instead of full Unicode matching (which is default). This is only meaningful for Unicode (str) patterns, and is ignored for bytes patterns
        ignore_case:
                Perform case-insensitive matching, including expressions that explicitly use uppercase members. Full Unicode matching (such as Ü matching ü) also works unless the ASCII flag is used to disable non-ASCII matches. The current locale does not change the effect of this flag unless the LOCALE flag is also used
        single_line:
                Not recommended. Makes the '.' special character match any character at all, including a newline. It's recommended you simply use literally_anything instead
        locale:
                Try not to use this, and rely on unicode matching instead
        multiline:
                Not recommended. Makes the '^' and '$' special characters match the start and end of lines, instead of the start and end of the string. This is automatically inserted when using line_start and line_end, you shouldn't need to add it manually
        unicode:
                Match using the full unicode standard, instead of just ASCII. Enabled by default, and therefore redundant
    """.strip()

    # test mixin members
    assert number.__doc__ == "Matches multiple digits next to each other. Does not match negatives or decimals"
    # test mixin methods
    assert any_of.__doc__ == """ Match any of the given `inputs`. Note that `inputs` can be multiple parameters,
                or a single string. Can also accept parameters chars and split. If char is set
                to True, then `inputs` must only be a single string, it interprets `inputs`
                as characters, and splits it up to find any of the chars in the string. If
                split is set to true, it forces the ?(...) regex syntax instead of the [...]
                syntax. It should act the same way, but your output regex will look different.
                By default, it just optimizes it for you.
            """
    # test mixin lambdas
    assert unicode.__doc__ == "Matches a unicode character by name"

    # test mixin decorated methods
    assert match_range.__doc__ == """ Match between `min` and `max` sequences of `input` in the string. This also accepts `greedy` and `possessive` parameters
                Max can be an empty string to indicate no maximum
                `greedy` means it will try to match as many repititions as possible
                non-greedy will try to match as few repititions as possible
                `possessive` means it won't backtrack to try to find any repitions
                see https://docs.python.org/3/library/re.html for more help
            """

    # test psuedonyms
    assert is_exactly.__doc__ == exactly.__doc__ == "This matches the string if and only if the entire string is exactly equal to `input`"