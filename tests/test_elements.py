# import random
# import re
# from inspect import currentframe, getframeinfo

# from rich import print as rprint
# from rich.table import Table
# from rich.text import Text
# from test_generate import *

import ezregex.python as er
# from ezregex import api
from ezregex.python import *


# # Positional
# def test_string_starts_with():
#     # """ lambda input='', cur=...: r'\A' + input + cur """
#     assert False, 'string_starts_with does not have tests'

# def test_string_ends_with():
#     # """ lambda input='', cur=...: input + r'\Z' + cur """
#     assert False, 'string_ends_with does not have tests'

# # Always use the multiline flag, so as to distinguish between start of a line vs start of the string
# def test_line_starts_with():
#     # """ lambda input='', cur=...: r'^' + input + cur, 'flags':'m' """
#     assert False, 'line_starts_with does not have tests'

# def test_line_ends_with():
#     # """ lambda input='', cur=...: cur + input + r'$', 'flags':'m' """
#     assert False, 'line_ends_with does not have tests'

# def test_word_boundary():
#     # """ r'\b' """
#     assert False, 'word_boundary does not have tests'

# def test_not_word_boundary():
#     # """ r'\B' """
#     assert False, 'not_word_boundary does not have tests'


# Literals
# def test_tab():
#     # """ r'\t' """
#     assert False, 'tab does not have tests'

# def test_space():
#     # """ r' ' """
#     assert False, 'space does not have tests'

# def test_space_or_tab():
#     # """ r'[ \t]' """
#     assert False, 'space_or_tab does not have tests'

# def test_new_line():
#     # """ r'\n' """
#     assert False, 'new_line does not have tests'

# def test_carriage_return():
#     # """ r'\r' """
#     assert False, 'carriage_return does not have tests'

# def test_quote():
#     # """ r'(?:\'|"|`)' """
#     assert False, 'quote does not have tests'

# def test_vertical_tab():
#     # """ r'\v' """
#     assert False, 'vertical_tab does not have tests'

# def test_form_feed():
#     # """ r'\f' """
#     assert False, 'form_feed does not have tests'

# def test_comma():
#     # """ r'\,' """
#     assert False, 'comma does not have tests'

# def test_period():
#     # """ r'\.' """
#     assert False, 'period does not have tests'

# def test_underscore():
#     # """ r'_' """
#     assert False, 'underscore does not have tests'

# def test_any_between():
#     # """ lambda char, and_char, cur=...: cur + r'[' + char + r'-' + and_char + r']' """
#     assert False, 'any_between does not have tests'


# # Not Literals
# def test_not_whitespace():
#     # """ r'\S' """
#     assert False, 'not_whitespace does not have tests'

# def test_not_digit():
#     # """ r'\D' """
#     assert False, 'not_digit does not have tests'

# def test_not_word():
#     # """ r'\W' """
#     assert False, 'not_word does not have tests'


# Catagories
# def test_whitespace():
#     # """ r'\s' """
#     assert False, 'whitespace does not have tests'

# def test_whitechunk():
#     # """ r'\s+' """
#     assert False, 'whitechunk does not have tests'

# def test_digit():
#     # """ r'\d' """
#     assert False, 'digit does not have tests'

# def test_number():
#     # """ r'\d+' """
#     assert False, 'number does not have tests'

# def test_word():
#     # """ r'\w+' """
#     assert False, 'word does not have tests'

# def test_word_char():
#     # """ r'\w' """
#     assert False, 'word_char does not have tests'

# def test_anything():
#     # """ r'.' """
#     assert False, 'anything does not have tests'

# def test_chunk():
#     # """ r'.+' """
#     assert False, 'chunk does not have tests'

# def test_uppercase():
#     # """ r'[A-Z]' """
#     assert False, 'uppercase does not have tests'

# def test_lowercase():
#     # """ r'[a-z]' """
#     assert False, 'lowercase does not have tests'

# def test_letter():
#     # """ r'[A-Za-z]' """
#     assert False, 'letter does not have tests'

# def test_hex_digit():
#     # """ r'[0-9a-fA-F]' """
#     assert False, 'hex_digit does not have tests'

# def test_oct_digit():
#     # """ r'[0-7]' """
#     assert False, 'oct_digit does not have tests'

# def test_punctuation():
#     # """ r'[' + escape('`~!@#$%^&*()-_=+[{]}\\|;:\'",<.>/?¢]') + r']' """
#     assert False, 'punctuation does not have tests'

# def test_controller():
#     # """ r'[\x00-\x1F\x7F]' """
#     assert False, 'controller does not have tests'

# def test_printable():
#     # """ r'[\x21-\x7E]' """
#     assert False, 'printable does not have tests'

# def test_p():
#     # """ # r'[\x20-\x7E]' """
#     assert False, 'p does not have tests'

# def test_alpha_num():
#     # """ r'[A-Za-z0-9_]' """
#     assert False, 'alpha_num does not have tests'

# def test_unicode():
#     # """ lambda name, cur=...: fr'\N{name}' """
#     assert False, 'unicode does not have tests'


# Amounts
# def test_match_max():
#     # """ lambda input, cur=...: cur + ('' if not len(input) else r'(?:' + input + r')') + r'+' """
#     assert False, 'match_max does not have tests'

# def test_match_num():
#     # """ lambda num, input, cur=...: cur + ('' if not len(input) else r'(?:' + input + r')') + r'{' + str(num) + r'}' """
#     assert False, 'match_num does not have tests'

# def test_match_more_than():
#     # """ lambda min, input, cur=...: cur + ('' if not len(input) else r'(?:' + input + r')') + r'{' + str(int(min) + 1) + r',}' """
#     assert False, 'match_more_than does not have tests'

# def test_match_at_least():
#     # """ lambda min, input, cur=...: cur + ('' if not len(input) else r'(?:' + input + r')') + r'{' + str(min) + r',}' """
#     assert False, 'match_at_least does not have tests'

# def test_match_at_most():
#     # """ lambda max, input, cur=...: cur + ('' if not len(input) else r'(?:' + input + r')') + r'{0,' + str(max) + r'}' """
#     assert False, 'match_at_most does not have tests'

# def test_match_range():
#     # """ _match_range_func """
#     assert False, 'match_range does not have tests'

# def test_at_least_one():
#     # """ _at_least_one_func """
#     assert False, 'at_least_one does not have tests'

# def test_at_least_none():
#     # """ _at_least_none_func """
#     assert False, 'at_least_none does not have tests'


# Choices
# def test_optional():
#     # """ _optional_func """
#     assert False, 'optional does not have tests'

# def test_either():
#     # """ lambda input, or_input, cur=...: cur + rf'(?:{input}|{or_input})' """
#     assert False, 'either does not have tests'

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


# def test_any_except():
#     # """ lambda input, type='.*', cur=...: cur + f'(?!{input}){type}' """
#     assert False, 'any_except does not have tests'

# def test_each():
#     # """ _each_func """
#     assert False, 'each does not have tests'


# Conditionals
# def test_if_proceded_by():
#     # """ lambda input, cur=...: fr'{cur}(?={input})' """
#     assert False, 'if_proceded_by does not have tests'

# def test_if_not_proceded_by():
#     # """ lambda input, cur=...: fr'{cur}(?!{input})' """
#     assert False, 'if_not_proceded_by does not have tests'

# def test_if_preceded_by():
#     # """ lambda input, cur=...: fr'(?<={input}){cur}' """
#     assert False, 'if_preceded_by does not have tests'

# def test_if_not_preceded_by():
#     # """ lambda input, cur=...: fr'(?<!{input}){cur}' """
#     assert False, 'if_not_preceded_by does not have tests'

# def test_if_enclosed_with():
#     # """ lambda open, stuff, close, cur=...: fr'((?<={open}){stuff}(?={open if close is None else close}))' """
#     assert False, 'if_enclosed_with does not have tests'


# # Grouping
# def test_group():
#     # """ lambda input, name=None, cur=...: f'{cur}({input})' if name is None else f'{cur}(?P<{name}>{input})' """
#     assert False, 'group does not have tests'

# def test_passive_group():
#     # """ lambda input, cur=...: f'{cur}(?:{input})' """
#     assert False, 'passive_group does not have tests'

# def test_earlier_group():
#     # """ lambda num_or_name, cur=...: f'{cur}\\{num_or_name}' if isinstance(num_or_name, int) or num_or_name in digits else f'{cur}(?P={num_or_name})' """
#     assert False, 'earlier_group does not have tests'

# def test_if_exists():
#     # """ lambda num_or_name, does, doesnt, cur=...: f'{cur}(?({num_or_name}){does}{"|" + str(doesnt) if doesnt is not None else ""})' """
#     assert False, 'if_exists does not have tests'


# # Premade
# def test_literally_anything():
#     # """ r'(?:.|\n)' """
#     assert False, 'literally_anything does not have tests'

# def test_signed():
#     # """ r'(?:(?:\-|\+))?\d+' """
#     assert False, 'signed does not have tests'

# def test_unsigned():
#     # """ r'\d+' """
#     assert False, 'unsigned does not have tests'

# def test_plain_float():
#     # """ r'(?:(?:\-|\+))?\d+\.(?:\d+)?' """
#     assert False, 'plain_float does not have tests'

# def test_full_float():
#     # """ r'(?:(?:\-|\+))?\d+\.(?:\d+)?(?:e(?:(?:\-|\+))?\d+)?' """
#     assert False, 'full_float does not have tests'

# def test_int_or_float():
#     # """ r'(?:(?:\-|\+))?\d+\.(?:\d+)?(?:e(?:(?:\-|\+))?\d+)?(?:\-)?\d+(?:\.(?:\d+)?)?' """
#     assert False, 'int_or_float does not have tests'

# def test_ow():
#     # """ r'(?:\s+)?' """
#     assert False, 'ow does not have tests'


# # Misc.
# def test_is_exactly():
#     # """ lambda input, cur=...: r"\A" + input + r'\Z' """
#     assert False, 'is_exactly does not have tests'

# def test_literal():
#     # """ lambda input, cur=...: cur + input """
#     assert False, 'literal does not have tests'

# def test_raw():
#     # """ lambda regex, cur=...: str(regex), 'sanatize': False """
#     assert False, 'raw does not have tests'


# TODO: Flags are dialect-specific, so they can't be here
# Flags
# def test_ASCII():
#     # """ lambda cur=...: cur, 'flags': 'a' """
#     assert str(word + ASCII + stuff)      == r'(?a)\w+.+', fr"{word + ASCII + stuff}      != (?a)\w+.+"

# def test_DOTALL():
#     # """ lambda cur=...: cur, 'flags': 's' """
#     assert str(word + DOTALL + stuff)     == r'(?s)\w+.+', fr"{word + DOTALL + stuff}     != (?s)\w+.+"

# def test_IGNORECASE():
#     # """ lambda cur=...: cur, 'flags': 'i' """
#     assert str(word + IGNORECASE + stuff) == r'(?i)\w+.+', fr"{word + IGNORECASE + stuff} != (?i)\w+.+"

# def test_LOCALE():
#     # """ lambda cur=...: cur, 'flags': 'L' """
#     assert str(word + LOCALE + stuff)     == r'(?L)\w+.+', fr"{word + LOCALE + stuff}     != (?L)\w+.+"

# def test_MULTILINE():
#     # """ lambda cur=...: cur, 'flags': 'm' """
#     assert str(word + MULTILINE + stuff)  == r'(?m)\w+.+', fr"{word + MULTILINE + stuff}  != (?m)\w+.+"

# def test_UNICODE():
#     # """ lambda cur=...: cur, 'flags': 'u' """
#     assert False, 'UNICODE does not have tests'



def test_misc():
    """ Just threw a bunch of stuff in here for now, I need to move it elsewhere eventually """
    a = word + ow
    # b = stuff + UNICODE
    c = IGNORECASE + '9'
    assert a + c == word + ow + IGNORECASE + '9', f"{a + b + c} != {word + ow + IGNORECASE + '9'}"

    # for cnt, r in enumerate(regexs):
    #     regex, match, dontMatch = r
    #     try:
    #         if match is not None:
    #             for m in match:
    #                 assert m in regex, f"{regex} does not match '{m}' (approx. {__file__}, line {_regexsLine+cnt})"
    #         if dontMatch is not None:
    #             for m in dontMatch:
    #                 assert m not in regex, f"{regex} DOES match '{m}' (approx. {__file__}, line {_regexsLine+cnt})"
    #     except Exception as err:
    #         print(regex)
    #         print(f'Error @ approx. {__file__}, line {_regexsLine+cnt}: \nregex = `{regex}`, match = `{match}`, dontMatch = `{dontMatch}`')
    #         raise err#.with_traceback(None)

    a = str(EZRegex(r'\s+', 'python'))
    b = str(EZRegex(raw(r'\s+'), 'python'))
    c = r'\s+'
    d = str(raw(r'\s+'))
    # e = str(whitespace + matchMax)
    assert a == b == c == d, f'\na: {a}\n b: {b}\n c: {c}\n d: {d}\n e: {e}'
    # assert (word + ow + anything + ':').test('word    d:', show=False)
    # assert not (word + ow + anything + ':').test('word', show=False)
    assert 'word    d:' in (word + ow + anything + ':')

    test = word + chunk
    test += word
    assert str(test) == str(word + chunk + word), f"{str(test)} != {str(word + chunk + word)}"
    assert test == word + chunk + word
    assert either('(' + word + ')', '.') == either(er.literal('(') + word() + er.literal(')'), '.'), f"{either('(' + word + ')', '.')} != {either(er.literal('(') + word() + er.literal(')'), '.')}"
    assert str(ifFollowedBy(word)) == r'(?=\w+)'

    #TODO: assert (word + ow + anything + ':') in 'word    d:'
    #TODO: assert (word + ow + anything + ':') not in 'word'
    assert str(word) == r'\w+', f'{word}'
