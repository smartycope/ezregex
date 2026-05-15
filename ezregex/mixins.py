# pyright: reportOperatorIssue = false
from re import escape, search
from string import digits
from sys import version_info
from typing import Callable
from inspect import signature, Parameter

from .psuedonyms import psuedonyms
from .EZRegex import EZRegex, EZRegexFunc
from functools import partial
from string import Formatter


from .types import EZRegexFunc, EZRegexType, EZRegexDefinition, EZRegexOther, EZRegexParam
# TODO: add typing to all of these

# NOTE: the docstrings are added manually, which I hate. They SHOULD be below the variable
# and auto-parsed, but that's difficult for a number of reasons, one of which being my
# weird, non-standard structure. Adding manually works for now.

# NOTE: when writing mixins, keep in mind that parameters which are None or bools will be passed as-is,
# ints will be cast to strings, and strings will be escaped based on the dialect's _escape_chars. Any
# other types will be auto-cast to strings, special characters will not be escaped, and a warning thrown
# See EZRegex._sanitize_param for more info

def _pretty_up_error_msg(func, param_name):
    try:
        func_names = psuedonyms[func]
    except KeyError:
        func_names = False
    return f'Parameter {param_name} in {func} {"(aka " + ", ".join(func_names) + ")" if func_names else ""}'

def raise_if_empty(param, func, param_name='pattern'):
    if not len(str(param)):
        raise ValueError(f'{_pretty_up_error_msg(func, param_name)} cannot be empty')

def validate_group_name(name, func, param_name):
    raise_if_empty(name, func, param_name)
    if name is None:
        raise ValueError(f'{_pretty_up_error_msg(func, param_name)} cannot be None')
    if search(r'\W', name):
        raise ValueError(f'{_pretty_up_error_msg(func, param_name)} cannot contain special characters')

def imply_pattern_is_cur(func):
    """ If `pattern` is Ellipsis, it will use `cur` instead, and `cur` will be set to an empty string.
        This is useful for functions that want to allow both inline and operator style chaining
        i.e. digit.amt(2) and amt(2, digit)

        NOTE: `pattern` must be a keyword parameter, and it must be the last parameter able to be
        provided as a positional argument. Don't use *args.

        NOTE: must come *after* add_greedy_possessive, not before. Don't ask me why.
    """
    def rtn(*args, pattern=..., cur=..., **kwargs):
        # First, check how many positional only params there are
        # parameters is an ordered mapping
        for num_params, param in enumerate(signature(func).parameters.values()):
            if param.name == 'pattern': break

        # If pattern is provided as a positional arg, make it into a keyword arg
        if len(args) > num_params:
            pattern = args[-1]
            args = args[:-1]

        if pattern is Ellipsis:
            return func(*args, pattern=cur, cur='', **kwargs)

        raise_if_empty(pattern, func.__name__)
        return func(*args, pattern=pattern, cur=cur, **kwargs)
    return rtn

def _parse_any_of_params(*patterns, chars=None, split=None):
    if split and len(patterns) != 1:
        raise ValueError("Please don't specifiy split and pass multiple patterns to anyof")
    elif split:
        patterns = list(patterns[0])
    elif len(patterns) == 1 and split is None and chars is not False:  # None means auto
        chars = True
        patterns = list(patterns[0])
    elif len(patterns) == 1 and split is None:
        patterns = list(patterns[0])
    elif len(patterns) > 1 and chars is None and all(map(lambda s: len(str(s)) == 1, patterns)):
        chars = True

    return chars, patterns

def BaseMixin(*, allow_greedy=False, allow_possessive=False):
    """ The basics of regex syntax. Almost all dialects have these. You almost certainly
        want to inherit from this class, even if you need to overload a few of it's members.
    """

    def add_greedy_possessive(func):
        def rtn(*args, greedy=True, possessive=False, cur=..., **kwargs):
            if not greedy and not allow_greedy:
                raise ValueError('Greedy qualifiers are not allowed in this dialect')
            if possessive and not allow_possessive:
                raise ValueError('Possessive qualifiers are not allowed in this dialect')
            if (not greedy) and possessive:
                raise ValueError('You can\'t be both non-greedy and possessive at the same time')
            return func(*args, cur=cur, **kwargs)
        return rtn

    class _BaseMixin:
        # replacement = None means it can work with both replacement and non-replacement EZRegex chains
        literal = lambda pattern, cur=...: cur + pattern, {'replacement': None, 'docstring':
        """This is a redundant function. You should always be able to use `... + 'stuff'` just as easily as `... + literal('stuff')`

            Args:
                pattern: the pattern to add
        """}

        # Not technically a variable, but it's accepted by EZRegex.__init__(), so it works
        raw = lambda regex, cur=...: cur + regex, {'_is_raw': True, 'replacement': None, 'docstring':
        """ If you already have some regular regex written and you want to incorperate
            it, this will allow you to include it without sanitizing all the backslashes
            and such, which all the other EZRegexs do automatically

            Args:
                regex: the regex to add directly
        """}

        # Positional
        word_boundary      = r'\b'
        not_word_boundary  = r'\B'

        # Literals
        tab                = r'\t'
        space              = r' '
        space_or_tab       = r'[ \t]'
        new_line           = r'\n'
        carriage_return    = r'\r'
        quote              = r'(?:\'|"|`)', {'docstring':
        "Matches ', \", and `"}
        vertical_tab       = r'\v'
        form_feed          = r'\f'
        comma              = r'\,'
        period             = r'\.'
        underscore         = r'_'

        # Not Literals
        not_whitespace     = r'\S'
        not_digit          = r'\D'
        not_word           = r'\W'

        # Catagories
        white_char         = r'\s'
        whitechunk         = r'\s+', {'docstring':
        "A \"chunk\" of whitespace. Just any amount of whitespace together"}
        digit              = r'\d'
        number             = r'\d+', {'docstring':
        "Matches multiple digits next to each other. Does not match negatives or decimals"}
        word               = r'\w+'
        word_char          = r'\w', {'docstring':
        "Matches just a single \"word character\", defined as any letter, number, or _"}
        anything           = r'.', {'docstring':
        "Matches any single character, except a newline. To also match a newline, use literally_anything"}
        chunk              = r'.+', {'docstring':
        "A \"chunk\": Any clump of characters up until the next newline"}
        uppercase          = r'[A-Z]'
        lowercase          = r'[a-z]'
        letter             = r'[A-Za-z]', {'docstring':
        "Matches just a letter -- not numbers or _ like word_char"}
        hex_digit          = r'[0-9a-fA-F]'
        oct_digit          = r'[0-7]'
        # TODO: is there a more formal definition of this or something?
        # NOTE: this could cause problems, as this is the *python* regex escape function, not the
        # current class's.
        # However, getting access to the current class here is sorta impossible, so I'm ignoring it until
        # it starts to cause problems
        punctuation         = r'[' + escape(']`~!@#$%^&*()-_=+[{}\\|;:\'",<.>/?¢]') + r']'
        controller          = r'[\x00-\x1F\x7F]', {'docstring':
        "Matches a metadata ASCII characters"}
        printable           = r'[\x21-\x7E]', {'docstring':
        "Matches printable ASCII characters"}
        printable_and_space = r'[\x20-\x7E]'
        letter_num          = r'[A-Za-z0-9_]'
        unicode             = lambda name, cur=...: fr'\N{name}', {'docstring':
        """ Matches a unicode character by name

            Args:
                name: the name of the unicode character
        """}

        # Premade
        # TODO: a chunk of literally anything/chunk of literally anything except ...
        literally_anything = r'(?:.|\n)', {'docstring':
        "*Any* character, include newline"}
        signed             = r'(?:(?:\-|\+))?\d+', {'docstring':
        "a signed number, including 123, -123, and +123"}
        unsigned           = r'\d+', {'docstring':
        "Same as number. Will not match +123"}
        plain_float        = r'(?:(?:\-|\+))?\d+\.(?:\d+)?', {'docstring':
        "Will match 123.45 and 123."}
        full_float         = r'(?:(?:\-|\+))?\d+\.(?:\d+)?(?:e(?:(?:\-|\+))?\d+)?', {'docstring':
        "Will match plain_float as well as things like 1.23e-10 and 1.23e+10"}
        int_or_float       = r'(?:(?:\-|\+))?\d+\.(?:\d+)?(?:e(?:(?:\-|\+))?\d+)?(?:\-)?\d+(?:\.(?:\d+)?)?', {'docstring':
        "Will match a full float, as well as a signed (and unsigned) integer"}
        ow                 = r'\s*', {'docstring':
        "\"Optional Whitechunk\""}

        @add_greedy_possessive
        @imply_pattern_is_cur
        def match_range(min, max, pattern=..., *, greedy=True, possessive=False, cur=...):
            """ Match between `min` and `max` sequences of `pattern` in the string. This also accepts `greedy` and `possessive` parameters
                Max can be an empty string to indicate no maximum
                `greedy` means it will try to match as many repititions as possible
                non-greedy will try to match as few repititions as possible
                `possessive` means it won't backtrack to try to find any repitions
                see your specific dialect docs for more help

                Args:
                    min (int): minimum number of instances of the pattern to match
                    max (int): maximum number of instances of the pattern to match
                    pattern: the pattern to match
                    greedy (bool): whether to match greedily (default: True)
                    possessive (bool): whether to match possessively (default: False)
            """
            raise_if_empty(pattern, 'match_range')

            s = cur
            if len(pattern):
                s += r'(?:' + pattern + r')'
            s += r'{' + str(min) + r',' + str(max) + r'}'
            if not greedy:
                s += r'?'
            if possessive:
                s += r'+'
            return s

        # Choices
        @add_greedy_possessive
        @imply_pattern_is_cur
        def optional(pattern=..., *, greedy=True, possessive=False, cur=...):
            """ Match `pattern` if it's there. This also accepts `greedy` and `possessive` parameters
                `greedy` means it will try to match as many repititions as possible
                non-greedy will try to match as few repititions as possible
                `possessive` means it won't backtrack to try to find any repitions
                see your specific dialect docs for more help

                Args:
                    pattern: the pattern to match
                    greedy (bool): whether to match greedily (default: True)
                    possessive (bool): whether to match possessively (default: False)
            """
            s = cur
            if len(pattern) > 1:
                s += fr'(?:{pattern})?'
            else:
                if len(pattern) == 1:
                    s += fr'{pattern}?'
            if not greedy:
                s += r'?'
            if possessive:
                s += r'+'
            return s

        def any_of(*patterns, chars=None, split=None, cur=...):
            """ Match any of the given `patterns`. Note that `patterns` can be multiple parameters,
                or a single string. Can also accept parameters chars and split. If char is set
                to True, then `patterns` must only be a single string, it interprets `patterns`
                as characters, and splits it up to find any of the chars in the string. If
                split is set to true, it forces the ?(...) regex syntax instead of the [...]
                syntax. It should act the same way, but your output regex will look different.
                By default, it just optimizes it for you.

                Args:
                    patterns: any of the patterns to match
                    chars (bool): whether to interpret patterns as characters (default: auto)
                    split (bool): whether to split patterns into characters (default: auto)
            """
            chars, patterns = _parse_any_of_params(*patterns, chars=chars, split=split)

            if chars:
                cur += r'['
                for i in patterns:
                    cur += i
                cur += r']'
            else:
                cur += r'(?:'
                for i in patterns:
                    cur += i
                    cur += '|'
                cur = cur[:-1]
                cur += r')'
            return cur

        def any_char_except(*chars, cur=...):
            """ This matches any char that is NOT in `chars`. `chars` can be multiple parameters,
                or a single string of chars to split.

                Args:
                    chars (str): any of the characters to match
            """

            # If it's just a string, split it up
            if len(chars) == 1 and len(chars[0]) > 1:
                chars = list(chars[0])

            cur += r'[^'
            for i in chars:
                cur += i
            cur += r']'
            return cur

        def any_between(char:str, and_char:str, cur=...):
            """ Match any char between `char` and `and_char`, using the ASCII table for reference

                Args:
                    char (str): the first character
                    and_char (str): the second character
            """
            raise_if_empty(char, 'any_between', 'char')
            raise_if_empty(and_char, 'any_between', 'and_char')
            return cur + r'[' + char + r'-' + and_char + r']'

        # TODO: the order of these parameters actually does matter, as sometime it needs
        # to match the first thing before it tries the 2nd.
        # @imply_pattern_is_cur
        def either(pattern, or_pattern=..., cur=...):
            """ Match either `pattern` or `or_pattern`. To choose between more than 2 things,
                you can either chain multiple `either` calls, or use `any_of`. Note that
                the order here matters: it first tries `pattern`, and if that doesn't
                match, then it tries `or_pattern`.

                Args:
                    pattern: a pattern to match
                    or_pattern: a pattern to match if the first one fails
            """
            # Manually handle implicit chains, instead of using imply_pattern_is_cur,
            # just because the order actually does matter
            if or_pattern is Ellipsis:
                return rf'(?:{cur}|{pattern})'
            return cur + rf'(?:{pattern}|{or_pattern})'

        # Amounts
        @imply_pattern_is_cur
        def match_max(pattern=..., *, cur=...):
            """ Match as many of `pattern` in the string as you can. This is equivelent to using the unary + operator.
            If `pattern` is not provided, it works on the previous regex pattern. That's not recommended for
            clarity's sake though

            Args:
                pattern: the pattern to match
            """
            return cur + r'(?:' + pattern + r')' + r'+'

        @imply_pattern_is_cur
        def match_num(num:int, pattern=..., *, cur=...):
            """ Match `num` amount of `pattern` in the string

            Args:
                num (int): the number of times to match the pattern
                pattern: the pattern to match
            """
            return cur + r'(?:' + pattern + r')' + r'{' + str(num) + r'}'

        @imply_pattern_is_cur
        def match_more_than(min:int, pattern=..., *, cur=...):
            """ Match more than `min` sequences of `pattern` in the string

            Args:
                min (int): the minimum number of times to match the pattern
                pattern: the pattern to match
            """
            return cur + r'(?:' + pattern + r')' + r'{' + str(int(min) + 1) + r',}'

        @imply_pattern_is_cur
        def match_at_least(min:int, pattern=..., *, cur=...):
            """ Match at least `min` sequences of `pattern` in the string

            Args:
                min (int): the minimum number of times to match the pattern
                pattern: the pattern to match
            """
            return cur + r'(?:' + pattern + r')' + r'{' + str(min) + r',}'

        @imply_pattern_is_cur
        def match_at_most(max:int, pattern=..., *, cur=...):
            """ Match at most `max` sequences of `pattern` in the string

            Args:
                max (int): the maximum number of times to match the pattern
                pattern: the pattern to match
            """
            return cur + r'(?:' + pattern + r')' + r'{0,' + str(max) + r'}'

        @add_greedy_possessive
        @imply_pattern_is_cur
        def at_least_one(pattern=..., *, greedy=True, possessive=False, cur=...):
            """ Match at least one of `pattern` in the string. This also accepts `greedy` and `possessive` parameters
                `greedy` means it will try to match as many repititions as possible
                non-greedy will try to match as few repititions as possible
                `possessive` means it won't backtrack to try to find any repitions
                see your specific dialect docs for more help

                Args:
                    pattern: the pattern to match
                    greedy (bool): whether to match greedily (default: True)
                    possessive (bool): whether to match possessively (default: False)
            """
            raise_if_empty(pattern, 'at_least_one')

            s = cur
            if len(pattern) > 1:
                s += fr'(?:{pattern})+'
            else:
                if len(pattern) == 1:
                    s += fr'{pattern}+'
            if not greedy:
                s += '?'
            if possessive:
                s += '+'
            return s

        @add_greedy_possessive
        @imply_pattern_is_cur
        def at_least_none(pattern=..., *, greedy=True, possessive=False, cur=...):
            """ Match 0 or more sequences of `pattern`. This also accepts `greedy` and `possessive` parameters
                `greedy` means it will try to match as many repititions as possible
                non-greedy will try to match as few repititions as possible
                `possessive` means it won't backtrack to try to find any repitions
                see your specific dialect docs for more help

                Args:
                    pattern: the pattern to match
                    greedy (bool): whether to match greedily (default: True)
                    possessive (bool): whether to match possessively (default: False)
            """
            raise_if_empty(pattern, 'at_least_none')

            s = cur
            if len(pattern) > 1:
                s += fr'(?:{pattern})*'
            else:
                if len(pattern) == 1:
                    s += fr'{pattern}*'
            if not greedy:
                s += '?'
            if possessive:
                s += '+'
            return s

    return _BaseMixin

# TODO: if group is called with 2 positional params, it raises an error. That error should be more helpful.
def GroupsMixin(*,
    named_group=lambda pattern, name, cur=...: f'{cur}(?P<{name}>{pattern})',
):
    """ A function which returns a class with the group and passive_group methods. Optionally
        specify how to handle named groups.
    """
    class _GroupsMixin:
        @imply_pattern_is_cur
        def group(pattern, *, name=None, cur=...):
            """ Causes `pattern` to be captured as a group. Specify `name` only as a keyword argument.
                Only useful when replacing regexs

                Args:
                    pattern: the pattern to match
                    name (str): the name of the group. Specifying this turns it into a named group,
                        instead of an unnamed group
            """
            raise_if_empty(pattern, 'group')
            if name is not None:
                if named_group is None:
                    raise ValueError('Named groups are not implemented in this dialect')
                validate_group_name(name, 'group', 'name')
            return f'{cur}({pattern})' if name is None else named_group(pattern, name, cur=cur)

        @imply_pattern_is_cur
        def passive_group(pattern, *, cur=...):
            """ As all regexs in EZRegex capture passively, this is entirely useless. But if you really want to, here it is

                Args:
                    pattern: the pattern to match
            """
            raise_if_empty(pattern, 'passive_group')
            return f'{cur}(?:{pattern})'

    return _GroupsMixin

def AdvancedGroupsMixin(*,
        earlier_numbered_group=lambda num, cur=...: f'{cur}\\{num}',
        earlier_named_group=lambda name, cur=...: f'{cur}(?P={name})'
    ):
    class _AdvancedGroupsMixin:
        def earlier_group(num_or_name, cur=...):
            """ Matches whatever the group referenced by `num_or_name` matched earlier. Must be *after* a
                group which would match `num_or_name`

                Args:
                    num_or_name (int | str): either the number or name of the previous group
            """
            validate_group_name(num_or_name, 'earlier_group', num_or_name)
            return earlier_numbered_group(num_or_name, cur=cur) \
                if isinstance(num_or_name, int) or num_or_name in digits \
                else earlier_named_group(num_or_name, cur=cur)

        def if_exists(num_or_name, does_pattern, doesnt_pattern=None, cur=...):
            """ Matches `does` if the group `num_or_name` exists, otherwise it matches `doesnt`

                Args:
                    num_or_name (int | str): either the number or name of the previous group
                    does_pattern: the pattern to match if the group exists
                    doesnt_pattern: the pattern to match if the group doesn't exist
            """
            validate_group_name(num_or_name, 'if_exists', num_or_name)
            return f'{cur}(?({num_or_name}){does_pattern}{("|" + str(doesnt_pattern)) if doesnt_pattern is not None else ""})'

    return _AdvancedGroupsMixin

def AssertionsMixin():
    """ Also called "lookahead"/"lookbehind". Adds associated singleton members which use them """

    # TODO: enforce these only being at the end or beginning of a chain -- maybe
    class _AssertionsMixin:
        # TODO: this needs more tests
        def any_except(pattern, type='.*', cur=...):
            """ Matches anything other than `pattern`, which must be a single string
            or EZRegex chain. Optionally accepts the `type` parameter,
            which works like this: "Match any `type` other than `pattern`". For example,
            "match any word which is not foo".

            Args:
                pattern: the pattern to match
                type: the type of pattern to match
            """
            raise_if_empty(pattern, 'any_except')
            return cur + f'(?!{pattern}){type}'

        @imply_pattern_is_cur
        def if_proceded_by(pattern, *, cur=...):
            """ Matches the pattern if it has `pattern` coming after it. Can only be used once in a given pattern,
                as it only applies to the end

                Args:
                    pattern: the pattern to match
            """
            return fr'{cur}(?={pattern})'

        # TODO: this needs more tests
        def each(*patterns, cur=...):
            """ Matches if the next part of the string can match all of the given patterns.
                Like the + operator, but out of order.

                Args:
                    patterns: the patterns to match
            """
            patterns = list(patterns)
            last = patterns.pop()
            s = cur
            for i in patterns:
                s += fr'(?={i})'
            s += last
            return s

        # TODO: is this description correct?
        @imply_pattern_is_cur
        def if_not_proceded_by(pattern, *, cur=...):
            """ Matches the pattern if it does **not** have `pattern` coming after it. Can only be used once in
                a given pattern, as it only applies to the end

                Args:
                    pattern: the pattern to match
            """
            return fr'{cur}(?!{pattern})'

        @imply_pattern_is_cur
        def if_preceded_by(pattern, *, cur=...):
            """ Matches the pattern if it has `pattern` coming before it. Can only be used once in a given pattern,
                as it only applies to the beginning

                Args:
                    pattern: the pattern to match
            """
            return fr'(?<={pattern}){cur}'

        @imply_pattern_is_cur
        def if_not_preceded_by(pattern, *, cur=...):
            """ Matches the pattern if it does **not** have `pattern` coming before it. Can only be used once
                in a given pattern, as it only applies to the beginning

                Args:
                    pattern: the pattern to match
            """
            return fr'(?<!{pattern}){cur}'

        @imply_pattern_is_cur
        def if_enclosed_with(open, close=..., pattern=..., *, cur=...):
            """ Matches if the string has `open`, then `pattern`, then `close`, but only \"matches\"
                `pattern`. Just a convenience combination of if_proceded_by and if_preceded_by.

                Args:
                    open: the pattern to match before the stuff
                    close: the pattern to match after the stuff. If unspecified, assumes it's the same as `open`
                    pattern: the pattern to match
            """
            if close is Ellipsis:
                close = open
            return fr'((?<={open}){pattern}(?={close}))'

    return _AssertionsMixin

def AnchorsMixin(*, string=True, line=True, word_boundaries=True, word=True, string_end=r'\z'):
    """ String anchors, where string/line/word starts/ends. You can disable specific ones via parameters"""
    class _AnchorsMixin:
        if string:
            string_starts_with = lambda pattern='', cur=...: r'\A' + pattern + cur, {'docstring':
            """ Matches the string if it starts with `pattern`

                Args:
                    pattern: the pattern to match
            """}

            string_ends_with = lambda pattern='', cur=...: pattern + string_end + cur, {'docstring':
            """ Matches the string if it ends with `pattern`

                Args:
                    pattern: the pattern to match
            """}
            is_exactly = imply_pattern_is_cur(lambda pattern=..., cur=...: r"\A" + pattern + string_end), {'docstring':
            """ This matches the string if and only if the entire string is exactly equal to `pattern`

                Args:
                    pattern: the pattern to match
            """}

        if line:
            # Always use the multiline flag, so as to distinguish between start of a line vs start of the string
            line_starts_with = lambda pattern='', cur=...: r'^' + pattern + cur, {'flags':'m', 'docstring':
            """ Matches at a line if it starts with `pattern`

                Args:
                    pattern: the pattern to match
            """}
            line_ends_with = lambda pattern='', cur=...: cur + pattern + r'$', {'flags':'m', 'docstring':
            """ Matches at a line if it ends with `pattern`

                Args:
                    pattern: the pattern to match
            """}

        if word_boundaries:
            word_boundary = r'\b', {'docstring':
            """ Matches at a word boundary, i.e. the empty space between a word
                character and not a word character, or the end of a string
            """}
            not_word_boundary = r'\B', {'docstring':
            """ Matches at anything other than a word boundary, i.e. the empty
                space between a word character and not a word character, or the
                end of a string
            """}

        if word:
            word_starts_with = lambda pattern='', cur=...: r'\<' + pattern + cur, {'docstring':
            """ Matchs a word if it starts with `pattern`

                Args:
                    pattern: the pattern to match
            """}
            word_ends_with = lambda pattern='', cur=...: pattern + r'\>' + cur, {'docstring':
            """ Matchs a word if it ends with `pattern`

                Args:
                    pattern: the pattern to match
            """}

    return _AnchorsMixin

def ReplacementsMixin(*,
    named_group:None|Callable[[str,str],str]=lambda name, cur=...: f"{cur}${{{name}}}",
    numbered_group:None|Callable[[int,str],str]=lambda num, cur=...: f"{cur}${{{num}}}",
    entire_match:None|EZRegexFunc=None,
):
    # if entire_match isn't specified, most of the time the 0th number group is the same thing
    if entire_match is None:
        entire_match = partial(numbered_group, 0)

    def _rgroup(num_or_name, cur=...):
        """ Puts in its place the group specified, either by group number (for unnamed
            groups) or group name (for named groups). Named groups are typically also counted by
            number, check your specific dialect docs for details.
            Group 0 is handled specially by this function, so it calls for the entire match,
            even if 0 doesn't mean the entire match in your dialect.

            Args:
                num_or_name (int | str): the number or name of the group you want to insert here
        """
        raise_if_empty(num_or_name, 'rgroup', num_or_name)
        is_num = isinstance(num_or_name, int) or num_or_name in digits

        if not is_num and named_group is None:
            raise ValueError('named groups are not supported by this dialect')

        if is_num and numbered_group is None:
            raise ValueError('numbered groups are not supported by this dialect')

        if is_num and num_or_name in (0, '0'):
            return entire_match(cur=cur)

        return numbered_group(num_or_name, cur=cur) \
            if is_num \
            else named_group(num_or_name, cur=cur)

    class CustomFormatter(Formatter):
        def get_value(self, key, args, kwargs):
            return _rgroup(key, '')
    formatter = CustomFormatter()

    class _ReplacementsMixin:
        rliteral = lambda pattern, cur=...: cur + pattern, {'replacement': True, 'docstring':
        """ Exactly like literal, but for replacement regexs """}

        @EZRegex.exclude
        @classmethod
        def replace(cls, string, compile=True):
            """ Generates a valid regex replacement string, using Python f-string like syntax.

                Args:
                    string (str): the templated replacement string
                    compile (bool): whether to compile the string into an EZRegex subclass instance (default: True)

                Example:
                    ``` replace("named: {group}, numbered: {1}, entire: {0}") ```

                Like Python f-strings, use {{ and }} to specify { and }

                Set the `compile` parameter to False to have it return an EZRegex subclass instance instead of a string

                Note: 0 is handled specially by this function, so it calls for the entire match,
                    even if 0 doesn't mean the entire match in your dialect.

                There's a few of advantages to using this instead of just the regular regex replacement syntax:
                - It's consistent between dialects
                - It's closer to Python f-string syntax, which is cleaner and more familiar
                - It handles numbered, named, and entire replacement types the same
            """
            string = formatter.format(string)
            return string if compile else cls([lambda cur=...: cur + string], replacement=True)

        rgroup = _rgroup, {'replacement': True}
        replace_entire = entire_match, {'replacement': True, 'docstring':
        "Puts in its place the entire match"}

    return _ReplacementsMixin

def AdvancedReplacementsMixin():
    class _AdvancedReplacementsMixin:
        entire_string = '$_', {'replacement': True}
        string_before_match = '$`', {'replacement': True}
        string_after_match = "$'", {'replacement': True}

    return _AdvancedReplacementsMixin
