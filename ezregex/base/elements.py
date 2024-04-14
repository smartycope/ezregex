# pyright: reportOperatorIssue = false
from re import escape
from string import digits
from sys import version_info

from ezregex import EZRegex


def _match_range_func(min, max, input, greedy=True, possessive=False, cur=...):
    assert not ((not greedy) and possessive), 'Match Range can\'t be non-greedy AND possessive at the same time'
    s = cur
    if len(input):
        s += r'(?:' + input + r')'
    s += r'{' + str(min) + r',' + str(max) + r'}'
    if not greedy:
        s += r'?'
    if possessive:
        if version_info < (3, 11):
            raise Exception('Possessive qualifiers require at least Python3.11 ')
        s += r'+'
    return s

def _at_least_one_func(input, greedy=True, possessive=False, cur=...):
    assert not ((not greedy) and possessive), 'At Least One can\'t be non-greedy AND possessive at the same time'
    s = cur
    if len(input) > 1:
        s += fr'(?:{input})+'
    else:
        if len(input) == 1:
            s += fr'{input}+'
    if not greedy:
        s += '?'
    if possessive:
        if version_info < (3, 11):
            raise Exception('Possessive qualifiers require at least Python3.11 ')
        s += '+'
    return s

def _at_least_none_func(input, greedy=True, possessive=False, cur=...):
    assert not ((not greedy) and possessive), 'At Least None can\'t be non-greedy AND possessive at the same time'
    s = cur
    if len(input) > 1:
        s += fr'(?:{input})*'
    else:
        if len(input) == 1:
            s += fr'{input}*'
    if not greedy:
        s += '?'
    if possessive:
        if version_info < (3, 11):
            raise Exception('Possessive qualifiers require at least Python3.11 ')
        s += '+'
    return s

def _optional_func(input, greedy=True, possessive=False, cur=...):
    assert not ((not greedy) and possessive), 'optional can\'t be non-greedy AND possessive at the same time'
    s = cur
    if len(input) > 1:
        s += fr'(?:{input})?'
    else:
        if len(input) == 1:
            s += fr'{input}?'
    if not greedy:
        s += r'?'
    if possessive:
        if version_info < (3, 11):
            raise Exception('Possessive qualifiers require at least Python3.11 ')
        s += r'+'
    return s

def _any_of_func(*inputs, chars=None, split=None, cur=...):
    if split and len(inputs) != 1:
        assert False, "Please don't specifiy split and pass multiple inputs to anyof"
    elif split:
        inputs = list(inputs[0])
    elif len(inputs) == 1 and split is None and chars is not False:  # None means auto
        chars = True
        inputs = list(inputs[0])
    elif len(inputs) == 1 and split is None:
        inputs = list(inputs[0])
    elif len(inputs) > 1 and chars is None and all(map(lambda s: len(s) == 1, inputs)):
        chars = True

    if chars:
        cur += r'['
        for i in inputs:
            cur += i
        cur += r']'
    else:
        cur += r'(?:'
        for i in inputs:
            cur += i
            cur += '|'
        cur = cur[:-1]
        cur += r')'
    return cur

def _any_char_except_func(*inputs, cur=...):
    # If it's just a string, split it up
    if len(inputs) == 1 and len(inputs[0]) > 1:
        inputs = list(inputs[0])

    cur += r'[^'
    for i in inputs:
        cur += i
    cur += r']'
    return cur

def _each_func(*inputs, cur=...):
    inputs = list(inputs)
    last = inputs.pop()
    s = cur
    for i in inputs:
        s += fr'(?={i})'
    s += last
    return s


base = {
    # Positional
    'string_starts_with': {'definition': lambda input='', cur=...: r'\A' + input + cur},
    'string_ends_with':   {'definition': lambda input='', cur=...: input + r'\Z' + cur},
    # Always use the multiline flag, so as to distinguish between start of a line vs start of the string
    'line_starts_with':   {'definition': lambda input='', cur=...: r'^' + input + cur, 'flags':'m'},
    'line_ends_with':     {'definition': lambda input='', cur=...: cur + input + r'$', 'flags':'m'},
    'word_boundary':      {'definition': r'\b'},
    'not_word_boundary':  {'definition': r'\B'},

    # Literals
    'tab':                {'definition': r'\t'},
    'space':              {'definition': r' '},
    'space_or_tab':       {'definition': r'[ \t]'},
    'new_line':           {'definition': r'\n'},
    'carriage_return':    {'definition': r'\r'},
    'quote':              {'definition': r'(?:\'|"|`)'},
    'vertical_tab':       {'definition': r'\v'},
    'form_feed':          {'definition': r'\f'},
    'comma':              {'definition': r'\,'},
    'period':             {'definition': r'\.'},
    'underscore':         {'definition': r'_'},
    'any_between':        {'definition': lambda char, and_char, cur=...: cur + r'[' + char + r'-' + and_char + r']'},

    # Not Literals
    'not_whitespace':     {'definition': r'\S'},
    'not_digit':          {'definition': r'\D'},
    'not_word':           {'definition': r'\W'},

    # Catagories
    'whitespace':         {'definition': r'\s'},
    'whitechunk':         {'definition': r'\s+'},
    'digit':              {'definition': r'\d'},
    'number':             {'definition': r'\d+'},
    'word':               {'definition': r'\w+'},
    'word_char':          {'definition': r'\w'},
    'anything':           {'definition': r'.'},
    'chunk':              {'definition': r'.+'},
    'uppercase':          {'definition': r'[A-Z]'},
    'lowercase':          {'definition': r'[a-z]'},
    'letter':             {'definition': r'[A-Za-z]'},
    'hex_digit':          {'definition': r'[0-9a-fA-F]'},
    'oct_digit':          {'definition': r'[0-7]'},
    'punctuation':        {'definition': r'[' + escape('`~!@#$%^&*()-_=+[{]}\\|;:\'",<.>/?¢]') + r']'},
    'controller':         {'definition': r'[\x00-\x1F\x7F]'},
    'printable':          {'definition': r'[\x21-\x7E]'},
    'printable_and_space':{'definition': r'[\x20-\x7E]'},
    'alpha_num':          {'definition': r'[A-Za-z0-9_]'},
    'unicode':            {'definition': lambda name, cur=...: fr'\N{name}'},

    # Amounts
    'match_max':          {'definition': lambda input, cur=...: cur + ('' if not len(input) else r'(?:' + input + r')') + r'+'},
    'match_num':          {'definition': lambda num, input, cur=...: cur + ('' if not len(input) else r'(?:' + input + r')') + r'{' + str(num) + r'}'},
    'match_more_than':    {'definition': lambda min, input, cur=...: cur + ('' if not len(input) else r'(?:' + input + r')') + r'{' + str(int(min) + 1) + r',}'},
    'match_at_least':     {'definition': lambda min, input, cur=...: cur + ('' if not len(input) else r'(?:' + input + r')') + r'{' + str(min) + r',}'},
    'match_at_most':      {'definition': lambda max, input, cur=...: cur + ('' if not len(input) else r'(?:' + input + r')') + r'{0,' + str(max) + r'}'},
    'match_range':        {'definition': _match_range_func},
    'at_least_one':       {'definition': _at_least_one_func},
    'at_least_none':      {'definition': _at_least_none_func},

    # Choices
    'optional':           {'definition': _optional_func},
    'either':             {'definition': lambda input, or_input, cur=...: cur + rf'(?:{input}|{or_input})'},
    'any_of':             {'definition': _any_of_func},
    'any_char_except':    {'definition': _any_char_except_func},
    'any_except':         {'definition': lambda input, type='.*', cur=...: cur + f'(?!{input}){type}'},
    'each':               {'definition': _each_func},

    # Conditionals
    'if_proceded_by':     {'definition': lambda input, cur=...: fr'{cur}(?={input})'},
    'if_not_proceded_by': {'definition': lambda input, cur=...: fr'{cur}(?!{input})'},
    'if_preceded_by':     {'definition': lambda input, cur=...: fr'(?<={input}){cur}'},
    'if_not_preceded_by': {'definition': lambda input, cur=...: fr'(?<!{input}){cur}'},
    'if_enclosed_with':   {'definition': lambda open, stuff, close, cur=...: fr'((?<={open}){stuff}(?={open if close is None else close}))'},

    # Grouping
    'group':              {'definition': lambda input, name=None, cur=...: f'{cur}({input})' if name is None else f'{cur}(?P<{name}>{input})'},
    'passive_group':      {'definition': lambda input, cur=...: f'{cur}(?:{input})'},
    'earlier_group':      {'definition': lambda num_or_name, cur=...: f'{cur}\\{num_or_name}' if isinstance(num_or_name, int) or num_or_name in digits else f'{cur}(?P={num_or_name})'},
    'if_exists':          {'definition': lambda num_or_name, does, doesnt, cur=...: f'{cur}(?({num_or_name}){does}{"|" + str(doesnt) if doesnt is not None else ""})'},

    # Premade
    'literally_anything':  {'definition': r'(?:.|\n)'},
    'signed':             {'definition': r'(?:(?:\-|\+))?\d+'},
    'unsigned':           {'definition': r'\d+'},
    'plain_float':        {'definition': r'(?:(?:\-|\+))?\d+\.(?:\d+)?'},
    'full_float':         {'definition': r'(?:(?:\-|\+))?\d+\.(?:\d+)?(?:e(?:(?:\-|\+))?\d+)?'},
    'int_or_float':       {'definition': r'(?:(?:\-|\+))?\d+\.(?:\d+)?(?:e(?:(?:\-|\+))?\d+)?(?:\-)?\d+(?:\.(?:\d+)?)?'},
    'ow':                 {'definition': r'(?:\s+)?'},

    # Misc.
    'is_exactly':         {'definition': lambda input, cur=...: r"\A" + input + r'\Z'},
    'literal':            {'definition': lambda input, cur=...: cur + input},
    'raw':                {'definition': lambda regex, cur=...: str(regex), 'sanatize': False},

    # Flags
    'ASCII':              {'definition': lambda cur=...: cur, 'flags': 'a'},
    'DOTALL':             {'definition': lambda cur=...: cur, 'flags': 's'},
    'IGNORECASE':         {'definition': lambda cur=...: cur, 'flags': 'i'},
    'LOCALE':             {'definition': lambda cur=...: cur, 'flags': 'L'},
    'MULTILINE':          {'definition': lambda cur=...: cur, 'flags': 'm'},
    'UNICODE':            {'definition': lambda cur=...: cur, 'flags': 'u'},
}
