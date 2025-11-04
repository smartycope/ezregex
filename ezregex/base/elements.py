# pyright: reportOperatorIssue = false
from re import escape
from string import digits
from sys import version_info


def input_not_empty(func, name, not_empty=0):
    def rtn(*args, **kwargs):
        if not len(str(args[not_empty])):
            raise ValueError(f'Input parameter of {name} cannot be empty')
        return func(*args, **kwargs)
    return rtn

def not_empty(param, func, param_name='input'):
    if not len(str(param)):
        raise ValueError(f'Parameter {param_name} in {func} cannot be empty')


def match_range(min, max, input, greedy=True, possessive=False, cur=...):
    if ((not greedy) and possessive):
        raise ValueError('match_range can\'t be non-greedy AND possessive at the same time')
    not_empty(input, 'match_range')

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

def at_least_one(input, greedy=True, possessive=False, cur=...):
    if ((not greedy) and possessive):
        raise ValueError('at_least_one can\'t be non-greedy AND possessive at the same time')
    not_empty(input, 'at_least_one')

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

def at_least_none(input, greedy=True, possessive=False, cur=...):
    if ((not greedy) and possessive):
        raise ValueError('at_least_none can\'t be non-greedy AND possessive at the same time')
    not_empty(input, 'at_least_none')

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

def optional(input, greedy=True, possessive=False, cur=...):
    if ((not greedy) and possessive):
        raise ValueError('optional can\'t be non-greedy AND possessive at the same time')
    not_empty(input, 'optional')

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

def _parse_any_of_params(*inputs, chars=None, split=None):
    if split and len(inputs) != 1:
        raise ValueError("Please don't specifiy split and pass multiple inputs to anyof")
    elif split:
        inputs = list(inputs[0])
    elif len(inputs) == 1 and split is None and chars is not False:  # None means auto
        chars = True
        inputs = list(inputs[0])
    elif len(inputs) == 1 and split is None:
        inputs = list(inputs[0])
    elif len(inputs) > 1 and chars is None and all(map(lambda s: len(str(s)) == 1, inputs)):
        chars = True

    return chars, inputs

def any_of(*inputs, chars=None, split=None, cur=...):
    chars, inputs = _parse_any_of_params(*inputs, chars=chars, split=split)

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

def any_char_except(*inputs, cur=...):
    # If it's just a string, split it up
    if len(inputs) == 1 and len(inputs[0]) > 1:
        inputs = list(inputs[0])

    cur += r'[^'
    for i in inputs:
        cur += i
    cur += r']'
    return cur

def each(*inputs, cur=...):
    inputs = list(inputs)
    last = inputs.pop()
    s = cur
    for i in inputs:
        s += fr'(?={i})'
    s += last
    return s

def any_between(char, and_char, cur=...):
    not_empty(char, 'any_between', 'char')
    not_empty(and_char, 'any_between', 'and_char')
    return cur + r'[' + char + r'-' + and_char + r']'

def match_max(input, cur=...):
    not_empty(input, 'match_max')
    return cur + r'(?:' + input + r')' + r'+'

def match_num(num, input, cur=...):
    not_empty(input, 'match_num')
    return cur + r'(?:' + input + r')' + r'{' + str(num) + r'}'

def match_more_than(min, input, cur=...):
    not_empty(input, 'match_more_than')
    return cur + r'(?:' + input + r')' + r'{' + str(int(min) + 1) + r',}'

def match_at_least(min, input, cur=...):
    not_empty(input, 'match_at_least')
    return cur + r'(?:' + input + r')' + r'{' + str(min) + r',}'

def match_at_most(max, input, cur=...):
    not_empty(input, 'match_at_most')
    return cur + r'(?:' + input + r')' + r'{0,' + str(max) + r'}'

def either(input, or_input, cur=...):
    not_empty(input, 'either')
    return cur + rf'(?:{input}|{or_input})'

def any_except(input, type='.*', cur=...):
    not_empty(input, 'any_except')
    return cur + f'(?!{input}){type}'

def if_proceded_by(input, cur=...):
    not_empty(input, 'if_proceded_by')
    return fr'{cur}(?={input})'

def if_not_proceded_by(input, cur=...):
    not_empty(input, 'if_not_proceded_by')
    return fr'{cur}(?!{input})'

def if_preceded_by(input, cur=...):
    not_empty(input, 'if_preceded_by')
    return fr'(?<={input}){cur}'

def if_not_preceded_by(input, cur=...):
    not_empty(input, 'if_not_preceded_by')
    return fr'(?<!{input}){cur}'

def if_enclosed_with(open, stuff, close=..., cur=...):
    not_empty(input, 'if_enclosed_with')
    if close is Ellipsis:
        close = open
    return fr'((?<={open}){stuff}(?={open if close is None else close}))'

def group(input, name=None, cur=...):
    not_empty(input, 'group')
    if name is not None:
        not_empty(name, 'group', 'name')
    return f'{cur}({input})' if name is None else f'{cur}(?P<{name}>{input})'

def passive_group(input, cur=...):
    not_empty(input, 'passive_group')
    return f'{cur}(?:{input})'

def earlier_group(num_or_name, cur=...):
    not_empty(num_or_name, 'earlier_group', num_or_name)
    return f'{cur}\\{num_or_name}' if isinstance(num_or_name, int) or num_or_name in digits else f'{cur}(?P={num_or_name})'

def if_exists(num_or_name, does, doesnt, cur=...):
    not_empty(num_or_name, 'earlier_group', num_or_name)
    return f'{cur}(?({num_or_name}){does}{"|" + str(doesnt) if doesnt is not None else ""})'


base = {
    # Positional
    # TODO: enforce these only being at the end or beginning of a chain -- maybe
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
    'any_between':        {'definition': any_between},

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
    # TODO: is there a more formal definition of this or something?
    'punctuation':        {'definition': r'[' + escape('`~!@#$%^&*()-_=+[{]}\\|;:\'",<.>/?¢]') + r']'},
    'controller':         {'definition': r'[\x00-\x1F\x7F]'},
    'printable':          {'definition': r'[\x21-\x7E]'},
    'printable_and_space':{'definition': r'[\x20-\x7E]'},
    'alpha_num':          {'definition': r'[A-Za-z0-9_]'},
    'unicode':            {'definition': lambda name, cur=...: fr'\N{name}'},

    # Amounts
    'repeat':             {'definition': match_max},
    'amt':                {'definition': match_num},
    'more_than':          {'definition': match_more_than},
    'at_least':           {'definition': match_at_least},
    'at_most':            {'definition': match_at_most},
    'between':            {'definition': match_range},
    'at_least_one':       {'definition': at_least_one},
    'at_least_none':      {'definition': at_least_none},

    # Choices
    'optional':           {'definition': optional},
    'either':             {'definition': either},
    'any_of':             {'definition': any_of},
    'any_char_except':    {'definition': any_char_except},
    'any_except':         {'definition': any_except},
    'each':               {'definition': each},

    # Conditionals
    'if_proceded_by':     {'definition': if_proceded_by},
    'if_not_proceded_by': {'definition': if_not_proceded_by},
    'if_preceded_by':     {'definition': if_preceded_by},
    'if_not_preceded_by': {'definition': if_not_preceded_by},
    'if_enclosed_with':   {'definition': if_enclosed_with},

    # Grouping
    'group':              {'definition': group},
    'passive_group':      {'definition': passive_group},
    'earlier_group':      {'definition': earlier_group},
    'if_exists':          {'definition': if_exists},

    # Premade
    # TODO: a chunk of literally anything/chunk of literally anything except ...
    'literally_anything': {'definition': r'(?:.|\n)'},
    'signed':             {'definition': r'(?:(?:\-|\+))?\d+'},
    'unsigned':           {'definition': r'\d+'},
    'plain_float':        {'definition': r'(?:(?:\-|\+))?\d+\.(?:\d+)?'},
    'full_float':         {'definition': r'(?:(?:\-|\+))?\d+\.(?:\d+)?(?:e(?:(?:\-|\+))?\d+)?'},
    'int_or_float':       {'definition': r'(?:(?:\-|\+))?\d+\.(?:\d+)?(?:e(?:(?:\-|\+))?\d+)?(?:\-)?\d+(?:\.(?:\d+)?)?'},
    'ow':                 {'definition': r'\s*'},

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


psuedonymns = {
    'repeat': ('matchMax', 'match_max'),
    'at_most': ('matchAtMost', 'atMost', 'match_at_most',),
    'amt': ('matchNum', 'matchAmt', 'match_amt', 'match_num', 'num',),
    'between': ('matchRange', 'match_range'),
    'more_than': ('matchMoreThan', 'match_greater_than', 'matchGreaterThan', 'moreThan', 'match_more_than',),
    'at_least': ('matchAtLeast', 'match_min', 'matchMin', 'atLeast', 'match_at_least',),
    'line_starts_with': ('lineStartsWith', 'line_start', 'lineStart',),
    'string_starts_with': ('stringStartsWith', 'string_start', 'stringStart',),
    'line_ends_with': ('lineEndsWith', 'line_end', 'lineEnd',),
    'string_ends_with': ('stringEndsWith', 'string_end', 'stringEnd',),
    'chunk': ('stuff',),
    'whitechunk': ('whiteChunk', 'white'),
    'anything': ('anychar', 'anyChar', 'char'),
    'letter': ('alpha',),
    'alpha_num': ('alphanum'  , 'alpha_num',),
    'any_between': ('anyBetween',),
    'word_char': ('wordChar',),
    'hex_digit': ('hexDigit', 'hex',),
    'oct_digit': ('octDigit',),
    'new_line': ('newline', 'newLine',),
    'space_or_tab': ('spaceOrTab',),
    'carriage_return': ('carriageReturn',),
    'vertical_tab': ('verticalTab',),
    'form_feed': ('formFeed',),
    'period': ('dot',),
    'int_or_float': ('intOrFloat',),
    'not_whitespace': ('notWhitespace',),
    'not_digit': ('notDigit',),
    'not_word': ('notWord',),
    'any_of': ('anyof', 'any_of', 'anyOf', 'oneOf', 'one_of',),
    'any_except': ('anyExcept',),
    'any_char_except': ('anyCharExcept',),
    'printable_and_space': ('printableAndSpace',),
    'if_proceded_by': ('ifFollowedBy', 'if_followed_by', 'ifProcededBy',),
    'if_exists': ('ifExists',),
    'if_not_proceded_by': ('ifNotFollowedBy', 'if_not_followed_by', 'ifNotProcededBy'),
    'if_preceded_by': ('ifPrecededBy',),
    'if_not_preceded_by': ('ifNotPrecededBy',),
    'if_enclosed_with': ('ifEnclosedWith', 'if_enclosed_by', 'ifEnclosedBy',),
    'passive_group': ('passiveGroup',),
    'earlier_group': ('sameAs', 'same_as', 'earlierGroup', 'sameAsGroup', 'same_as_group',),
    'is_exactly': ('exactly', 'isExactly',),
    'optional': ('oneOrNone', 'one_or_none', 'opt',),
    'at_least_one': ('oneOrMore', 'one_or_more', 'atLeastOne', 'atLeast1', 'at_least_1',),
    'at_least_none': ('noneOrMore', 'none_or_more', 'atLeastNone', 'at_least_0', 'atLeast0', 'anyAmt', 'any_amt', 'zeroOrMore', 'zero_or_more',),
    'ASCII': ('ascii', 'a',),
    'DOTALL': ('dotall', 's',),
    'IGNORECASE': ('ignorecase', 'i', 'ignoreCase', 'ignore_case',),
    'LOCALE': ('locale', 'L',),
    'MULTILINE': ('multiline', 'm',),
    'signed': ('integer',),
    'literally_anything': ('literallyAnything',),
    'word_boundary': ('wordBoundary',),
    'not_word_boundary': ('notWordBoundary',),
    'rgroup': ('replaceGroup', 'replace_group',),
    'replace_entire': ('replaceAll', 'replace_all', 'replaceEntire',),
}
