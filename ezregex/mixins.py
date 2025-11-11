# pyright: reportOperatorIssue = false
from re import escape
from string import digits
from sys import version_info
from typing import Callable
from .EZRegex import EZRegex, EZRegexFunc
from functools import partial
from string import Formatter

from .types import EZRegexFunc, EZRegexType, EZRegexDefinition, EZRegexOther, EZRegexParam
# TODO: add typing to all of these

def raise_if_empty(param, func, param_name='input'):
    if not len(str(param)):
        raise ValueError(f'Parameter {param_name} in {func} cannot be empty')


def BaseMixin(*, allow_greedy=False, allow_possessive=False):
    """ The basics of regex syntax. Almost all dialects have these. You almost certainly
        want to inherit from this class, even if you need to overload a few of it's members.
    """

    def add_greedy_possessive(func):
        def rtn(*args, greedy=True, possessive=False, cur=..., **kwargs):
            if not allow_greedy:
                raise ValueError('Greedy qualifiers are not allowed in this dialect')
            if not allow_possessive:
                raise ValueError('Possessive qualifiers are not allowed in this dialect')
            if (not greedy) and possessive:
                raise ValueError('You can\'t be both non-greedy and possessive at the same time')
            return func(*args, **kwargs)
        return rtn


    class _BaseMixin:
        literal = lambda input, cur=...: cur + input
        "This is a redundant function. You should always be able to use `... + 'stuff'` just as easily as `... + literal('stuff')`"

        raw = lambda regex, cur=...: str(regex), {'sanatize': False}
        """ If you already have some regular regex written, and you want to incorperate
        it, this will allow you to include it without sanatizing all the backslaches
        and such, which all the other EZRegexs do automatically
    """

        # Positional
        word_boundary      = r'\b'
        not_word_boundary  = r'\B'

        # Literals
        tab                = r'\t'
        space              = r' '
        space_or_tab       = r'[ \t]'
        new_line           = r'\n'
        carriage_return    = r'\r'
        quote              = r'(?:\'|"|`)'
        "Matches ', \", and `"
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
        whitespace         = r'\s'
        whitechunk         = r'\s+'
        "A \"chunk\" of whitespace. Just any amount of whitespace together"
        digit              = r'\d'
        number             = r'\d+'
        "Matches multiple digits next to each other. Does not match negatives or decimals"
        word               = r'\w+'
        word_char          = r'\w'
        "Matches just a single \"word character\", defined as any letter, number, or _"
        anything           = r'.'
        "Matches any single character, except a newline. To also match a newline, use literally_anything"
        chunk              = r'.+'
        "A \"chunk\": Any clump of characters up until the next newline"
        uppercase          = r'[A-Z]'
        lowercase          = r'[a-z]'
        letter             = r'[A-Za-z]'
        "Matches just a letter -- not numbers or _ like word_char"
        hex_digit          = r'[0-9a-fA-F]'
        oct_digit          = r'[0-7]'
        # TODO: is there a more formal definition of this or something?
        # NOTE: this could cause problems, as this is the *python* regex escape function, not the
        # current class's.
        # However, getting access to the current class here is sorta impossible, so I'm ignoring it until
        # it starts to cause problems
        punctuation        = r'[' + escape(']`~!@#$%^&*()-_=+[{}\\|;:\'",<.>/?¢]') + r']'
        controller         = r'[\x00-\x1F\x7F]'
        "Matches a metadata ASCII characters"
        printable          = r'[\x21-\x7E]'
        "Matches printable ASCII characters"
        printable_and_space= r'[\x20-\x7E]'
        alpha_num          = r'[A-Za-z0-9_]'
        unicode            = lambda name, cur=...: fr'\N{name}'
        "Matches a unicode character by name"

        # Premade
        # TODO: a chunk of literally anything/chunk of literally anything except ...
        literally_anything = r'(?:.|\n)'
        "*Any* character, include newline"
        signed             = r'(?:(?:\-|\+))?\d+'
        "a signed number, including 123, -123, and +123"
        unsigned           = r'\d+'
        "Same as number. Will not match +123"
        plain_float        = r'(?:(?:\-|\+))?\d+\.(?:\d+)?'
        "Will match 123.45 and 123."
        full_float         = r'(?:(?:\-|\+))?\d+\.(?:\d+)?(?:e(?:(?:\-|\+))?\d+)?'
        "Will match plain_float as well as things like 1.23e-10 and 1.23e+10"
        int_or_float       = r'(?:(?:\-|\+))?\d+\.(?:\d+)?(?:e(?:(?:\-|\+))?\d+)?(?:\-)?\d+(?:\.(?:\d+)?)?'
        "Will match a full float, as well as a signed (and unsigned) integer"
        ow                 = r'\s*'
        "\"Optional Whitechunk\""

        @add_greedy_possessive
        def match_range(min, max, input, greedy=True, possessive=False, cur=...):
            """ Match between `min` and `max` sequences of `input` in the string. This also accepts `greedy` and `possessive` parameters
                Max can be an empty string to indicate no maximum
                `greedy` means it will try to match as many repititions as possible
                non-greedy will try to match as few repititions as possible
                `possessive` means it won't backtrack to try to find any repitions
                see https://docs.python.org/3/library/re.html for more help
            """
            raise_if_empty(input, 'match_range')

            s = cur
            if len(input):
                s += r'(?:' + input + r')'
            s += r'{' + str(min) + r',' + str(max) + r'}'
            if not greedy:
                s += r'?'
            if possessive:
                s += r'+'
            return s

        # Choices
        @add_greedy_possessive
        def optional(input, greedy=True, possessive=False, cur=...):
            """ Match `input` if it's there. This also accepts `greedy` and `possessive` parameters
                `greedy` means it will try to match as many repititions as possible
                non-greedy will try to match as few repititions as possible
                `possessive` means it won't backtrack to try to find any repitions
                see https://docs.python.org/3/library/re.html for more help
            """
            raise_if_empty(input, 'optional')

            s = cur
            if len(input) > 1:
                s += fr'(?:{input})?'
            else:
                if len(input) == 1:
                    s += fr'{input}?'
            if not greedy:
                s += r'?'
            if possessive:
                s += r'+'
            return s

        @staticmethod
        @EZRegex.exclude
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
            """ Match any of the given `inputs`. Note that `inputs` can be multiple parameters,
                or a single string. Can also accept parameters chars and split. If char is set
                to True, then `inputs` must only be a single string, it interprets `inputs`
                as characters, and splits it up to find any of the chars in the string. If
                split is set to true, it forces the ?(...) regex syntax instead of the [...]
                syntax. It should act the same way, but your output regex will look different.
                By default, it just optimizes it for you.
            """
            chars, inputs = BaseMixin._parse_any_of_params(*inputs, chars=chars, split=split)

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
            """ This matches any char that is NOT in `inputs`. `inputs` can be multiple parameters,
                or a single string of chars to split. """

            # If it's just a string, split it up
            if len(inputs) == 1 and len(inputs[0]) > 1:
                inputs = list(inputs[0])

            cur += r'[^'
            for i in inputs:
                cur += i
            cur += r']'
            return cur

        def any_between(char, and_char, cur=...):
            """Match any char between `char` and `and_char`, using the ASCII table for reference"""
            raise_if_empty(char, 'any_between', 'char')
            raise_if_empty(and_char, 'any_between', 'and_char')
            return cur + r'[' + char + r'-' + and_char + r']'

        def either(input, or_input, cur=...):
            raise_if_empty(input, 'either')
            return cur + rf'(?:{input}|{or_input})'

        # Amounts
        def match_max(input, cur=...):
            """ Match as many of `input` in the string as you can. This is equivelent to using the unary + operator.
            If `input` is not provided, it works on the previous regex pattern. That's not recommended for
            clarity's sake though
            """
            raise_if_empty(input, 'match_max')
            return cur + r'(?:' + input + r')' + r'+'

        def match_num(num, input, cur=...):
            """ Match `num` amount of `input` in the string """
            raise_if_empty(input, 'match_num')
            return cur + r'(?:' + input + r')' + r'{' + str(num) + r'}'

        def match_more_than(min, input, cur=...):
            """ Match more than `min` sequences of `input` in the string """
            raise_if_empty(input, 'match_more_than')
            return cur + r'(?:' + input + r')' + r'{' + str(int(min) + 1) + r',}'

        def match_at_least(min, input, cur=...):
            """ Match at least `min` sequences of `input` in the string """
            raise_if_empty(input, 'match_at_least')
            return cur + r'(?:' + input + r')' + r'{' + str(min) + r',}'

        def match_at_most(max, input, cur=...):
            """ Match at most `max` sequences of `input` in the string """
            raise_if_empty(input, 'match_at_most')
            return cur + r'(?:' + input + r')' + r'{0,' + str(max) + r'}'

        @add_greedy_possessive
        def at_least_one(input, greedy=True, possessive=False, cur=...):
            """ Match at least one of `input` in the string. This also accepts `greedy` and `possessive` parameters
                `greedy` means it will try to match as many repititions as possible
                non-greedy will try to match as few repititions as possible
                `possessive` means it won't backtrack to try to find any repitions
                see https://docs.python.org/3/library/re.html for more help
            """
            raise_if_empty(input, 'at_least_one')

            s = cur
            if len(input) > 1:
                s += fr'(?:{input})+'
            else:
                if len(input) == 1:
                    s += fr'{input}+'
            if not greedy:
                s += '?'
            if possessive:
                s += '+'
            return s

        @add_greedy_possessive
        def at_least_none(input, greedy=True, possessive=False, cur=...):
            """ Match 0 or more sequences of `input`. This also accepts `greedy` and `possessive` parameters
                `greedy` means it will try to match as many repititions as possible
                non-greedy will try to match as few repititions as possible
                `possessive` means it won't backtrack to try to find any repitions
                see https://docs.python.org/3/library/re.html for more help
            """
            raise_if_empty(input, 'at_least_none')

            s = cur
            if len(input) > 1:
                s += fr'(?:{input})*'
            else:
                if len(input) == 1:
                    s += fr'{input}*'
            if not greedy:
                s += '?'
            if possessive:
                s += '+'
            return s

    return _BaseMixin

def GroupsMixin(*,
    advanced=False,
    named_group=lambda input, name, cur=...: f'{cur}(?P<{name}>{input})',
    earlier_numbered_group=lambda num, cur=...: f'{cur}\\{num}',
    earlier_named_group=lambda name, cur=...: f'{cur}(?P={name})'
):
    """ A function which returns a class with the group and passive_group methods. Optionally
        specify how to handle named groups.
    """
    class _GroupsMixin:
        def group(input, name=None, cur=...):
            "Causes `input` to be captured as an unnamed group. Only useful when replacing regexs"
            raise_if_empty(input, 'group')
            if name is not None:
                if named_group is None:
                    raise ValueError(f'Named groups are not implemented in this dialect')
                raise_if_empty(name, 'group', 'name')
            return f'{cur}({input})' if name is None else named_group(input, name, cur=cur)

        def passive_group(input, cur=...):
            "As all regexs in EZRegex capture passively, this is entirely useless. But if you really want to, here it is"
            raise_if_empty(input, 'passive_group')
            return f'{cur}(?:{input})'

        if advanced:
            def earlier_group(num_or_name, cur=...):
                """ Matches whatever the group referenced by `num_or_name` matched earlier. Must be *after* a
                    group which would match `num_or_name`
    """
                raise_if_empty(num_or_name, 'earlier_group', num_or_name)
                return earlier_numbered_group(num_or_name, cur=cur) \
                    if isinstance(num_or_name, int) or num_or_name in digits \
                    else earlier_named_group(num_or_name, cur=cur)

            def if_exists(num_or_name, does_pattern, doesnt_pattern=None, cur=...):
                """ Matches `does` if the group `num_or_name` exists, otherwise it matches `doesnt` """
                raise_if_empty(num_or_name, 'earlier_group', num_or_name)
                return f'{cur}(?({num_or_name}){does_pattern}{("|" + str(doesnt_pattern)) if doesnt_pattern is not None else ""})'

    return _GroupsMixin

def AssertionsMixin():
    """ Also called "lookahead"/"lookbehind". Adds associated singleton members which use them """

    # TODO: enforce these only being at the end or beginning of a chain -- maybe
    class _AssertionsMixin:
        def any_except(input, type='.*', cur=...):
            """ Matches anything other than `input`, which must be a single string or EZRegex chain, **not** a list. Also
            optionally accepts the `type` parameter, which works like this: \"Match any `type` other than `input`\". For example,
            \"match any word which is not foo\". Do note that this function is new, and I'm still working out the kinks.
            """
            raise_if_empty(input, 'any_except')
            return cur + f'(?!{input}){type}'

        def if_proceded_by(input, cur=...):
            """ Matches the pattern if it has `input` coming after it. Can only be used once in a given pattern,
                as it only applies to the end
            """
            raise_if_empty(input, 'if_proceded_by')
            return fr'{cur}(?={input})'

        def each(*inputs, cur=...):
            "Matches if the next part of the string can match all of the given inputs. Like the + operator, but out of order."
            inputs = list(inputs)
            last = inputs.pop()
            s = cur
            for i in inputs:
                s += fr'(?={i})'
            s += last
            return s

        def if_not_proceded_by(input, cur=...):
            """ Matches the pattern if it does **not** have `input` coming after it. Can only be used once in
                a given pattern, as it only applies to the end
            """
            raise_if_empty(input, 'if_not_proceded_by')
            return fr'{cur}(?!{input})'

        def if_preceded_by(input, cur=...):
            """ Matches the pattern if it has `input` coming before it. Can only be used once in a given pattern,
                as it only applies to the beginning
            """
            raise_if_empty(input, 'if_preceded_by')
            return fr'(?<={input}){cur}'

        def if_not_preceded_by(input, cur=...):
            """ Matches the pattern if it does **not** have `input` coming before it. Can only be used once
                in a given pattern, as it only applies to the beginning
            """
            raise_if_empty(input, 'if_not_preceded_by')
            return fr'(?<!{input}){cur}'

        def if_enclosed_with(open, stuff, close=..., cur=...):
            """ Matches if the string has `open`, then `stuff`, then `close`, but only \"matches\"
                stuff. Just a convenience combination of ifProceededBy and ifPreceededBy.
            """
            raise_if_empty(input, 'if_enclosed_with')
            if close is Ellipsis:
                close = open
            return fr'((?<={open}){stuff}(?={open if close is None else close}))'

    return _AssertionsMixin

def AnchorsMixin(*, string=True, line=True, word_boundaries=True, word=True, string_end=r'\z'):
    """ String anchors, where string/line/word starts/ends. You can disable specific ones via parameters"""
    class _AnchorsMixin:
        if string:
            string_starts_with = lambda input='', cur=...: r'\A' + input + cur
            string_ends_with   = lambda input='', cur=...: input + string_end + cur
            is_exactly = lambda input, cur=...: r"\A" + input + string_end
            "This matches the string if and only if the entire string is exactly equal to `input`"

        if line:
            # Always use the multiline flag, so as to distinguish between start of a line vs start of the string
            line_starts_with   = lambda input='', cur=...: r'^' + input + cur, {'flags':'m'}
            line_ends_with     = lambda input='', cur=...: cur + input + r'$', {'flags':'m'}

        if word_boundaries:
            word_boundary      = lambda input='', cur=...: r'\b' + input + cur
            "Matches the boundary of a word, i.e. the empty space between a word character and not a word character, or the end of a string"
            not_word_boundary  = lambda input='', cur=...: cur + input + r'\B'
            "The opposite of `word_boundary`"


        if word:
            word_starts_with   = lambda input='', cur=...: r'\<' + input + cur
            word_ends_with     = lambda input='', cur=...: input + r'\>' + cur

    return _AnchorsMixin

def ReplacementsMixin(*,
    named_group:None|Callable[[str,str],str]=lambda name, cur=...: f"{cur}$<{name}>",
    numbered_group:None|Callable[[int,str],str]=lambda num, cur=...: f"{cur}${{{num}}}",
    entire_match:None|EZRegexFunc=None,
    advanced=False,
    entire_string:None|EZRegexFunc='$_',
    string_before_match:None|EZRegexFunc='$`',
    string_after_match:None|EZRegexFunc="$'",
):
    # if entire_match isn't specified, most of the time the 0th number group is the same thing
    if entire_match is None:
        entire_match = partial(numbered_group, args=(0,))

    # Weird scope error I guess
    _entire_string = entire_string
    _string_before_match = string_before_match
    _string_after_match = string_after_match

    def _rgroup(num_or_name, cur=...):
        """ Puts in its place the group specified, either by group number (for unnamed
            groups) or group name (for named groups). Named groups are also counted by
            number, I'm pretty sure. Groups are numbered starting from 1
        """
        raise_if_empty(num_or_name, 'rgroup', num_or_name)
        is_num = isinstance(num_or_name, int) or num_or_name in digits

        if not is_num and named_group is None:
            raise ValueError('named groups are not supported by this dialect')

        if is_num and numbered_group is None:
            raise ValueError('numbered groups are not supported by this dialect')

        return numbered_group(num_or_name, cur=cur) \
            if is_num \
            else named_group(num_or_name, '', cur=cur)

    class CustomFormatter(Formatter):
        def get_value(self, key, args, kwargs):
            return _rgroup(key, '')
    formatter = CustomFormatter()

    class _ReplacementsMixin:
        @EZRegex.exclude
        @classmethod
        def replace(cls, string, rtn_str=True):
            """ Generates a valid regex replacement string, using Python f-string like syntax.

                Example:
                    ``` replace("named: {group}, numbered: {1}, entire: {0}") ```

                Like Python f-strings, use {{ and }} to specify { and }

                Set the `rtn_str` parameter to True to have it return an EZRegex type instead of a string

                Note: Remember that index 0 is the entire match

                There's a few of advantages to using this instead of just the regular regex replacement syntax:
                - It's consistent between dialects
                - It's closer to Python f-string syntax, which is cleaner and more familiar
                - It handles numbered, named, and entire replacement types the same
            """
            string = formatter.format(string)
            return string if rtn_str else cls(string, sanatize=False, replacement=True)

        rgroup = _rgroup, {'replacement': True}
        replace_entire = entire_match, {'replacement': True}
        "Puts in its place the entire match"


        if advanced:
            if _entire_string:
                entire_string = _entire_string, {'replacement': True}
            if _string_before_match:
                string_before_match = _string_before_match, {'replacement': True}
            if _string_after_match:
                string_after_match = _string_after_match, {'replacement': True}

    return _ReplacementsMixin