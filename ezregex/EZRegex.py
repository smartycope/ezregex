import colorsys
import re
from copy import deepcopy
from functools import partial
from typing import List, Literal, LiteralString
from warnings import warn
import logging

from .invert import invert
from .generate import *

from .specs import dialects

# TODO: consider changing addFlags to "outer" or "end" or something
# TODO: Seriously consider removing the debug functions

# These functions comprise the color algorithm for _matchJSON()
def toHtml(r, g, b):
            return f'#{r:02x}{g:02x}{b:02x}'

def toRgb(html: str) -> tuple:
    hex_color = html.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return rgb

def generate_colors(amt, s=1, v=1, offset=0):
    """ Generate `amt` number of colors evenly spaced around the color wheel
        with a given saturation and value
    """
    amt += 1
    return [toHtml(*map(lambda c: round(c*255), colorsys.hsv_to_rgb(*((offset + ((1/amt) * (i + 1))) % 1.001, s, v)))) for i in range(amt-1)]

def furthest_colors(html, amt=5, v_bias=0, s_bias=0):
    """ Gets the `amt` number of colors evenly spaced around the color wheel from the given color
        `v_bias` and `s_bias` are between 0-1 and offset the colors
    """
    amt += 1
    h, s, v = colorsys.rgb_to_hsv(*map(lambda c: c/255, toRgb(html)))

    return [toHtml(*map(lambda c: round(c*255), colorsys.hsv_to_rgb(*((h + ((1/amt) * (i + 1))) % 1.001, (s+s_bias) % 1.001, (v+v_bias) % 1.001)))) for i in range(amt-1)]


class EZRegex:
    """ Represent parts of the Regex syntax. Should not be instantiated by the user directly."""

    def __init__(self,
                 definition:List[partial[str]]|str|"EZRegex"|partial[str],
                 dialect: str,
                 sanatize:bool=True,
                 init:bool=True,
                 replacement:bool=False,
                 flags:str='',
        ):
        """
        The workhorse of the EZRegex library. This represents a regex pattern that can be combined
        with other EZRegexs and strings. Ideally, this should only be called internally, but it should
        still work from the user's end
        """

        if dialect not in dialects.keys():
            raise ValueError(f'Unsupported dialect `{dialect}` given. Supported dialects are: {list(dialects.keys())}')

        self.flags = flags
        # Parse params
        # Add flags if it's another EZRegex
        if isinstance(definition, EZRegex):
            self.flags = definition.flags
            if definition.dialect != dialect:
                raise ValueError('Cannot mix regex dialects')

        if isinstance(definition, (str, EZRegex)):
            definition = [str(definition)]
        elif not isinstance(definition, (list, tuple)):
            definition = [definition]

        self.sanatize = sanatize
        self.replacement = replacement
        self.funcList = list(definition)
        # Just some psuedonymns
        self.example = self.invert = self.inverse
        self.dialect = dialect
        # The dict that has the values
        self._dialect = dialects[dialect]


        # The init parameter is not actually required, but it will make it more
        # efficient, so we don't have to check that the whole chain is callable
        if init:
            # Go through the chain (most likely of length 1) and parse any strings
            # This is for simplicity when defining all the members
            for i in range(len(self.funcList)):
                if isinstance(self.funcList[i], str):
                    # I *hate* how Python handles lambdas
                    stringBecauseHatred = deepcopy(self.funcList[i])
                    self.funcList[i] = lambda cur=...: cur + stringBecauseHatred
                elif not callable(self.funcList[i]) and self.funcList[i] is not None:
                    raise ValueError(f"Invalid type {type(self.funcList[i])} passed to EZRegex constructor")

    def _escape(self, pattern:str):
        """ This function was modified from the one in /usr/lib64/python3.12/re/__init__.py line 255 """
        _special_chars_map = {i: '\\' + chr(i) for i in self._dialect['escape_chars']}
        return pattern.translate(_special_chars_map)


    def _sanitizeInput(self, i, addFlags=False):
        """ Instead of rasising an error if passed a strange datatype, it now trys to cast it to a string """
        i = deepcopy(i)

        # Don't sanatize anything if this is a replacement string
        if self.replacement:
            return str(i)

        # If it's another chain, compile it
        if isinstance(i, EZRegex):
            return i._compile(addFlags=addFlags)
        # It's a string (so we need to escape it)
        elif isinstance(i, str):
            return self._escape(i)
        # A couple of singletons use bools and None as kwargs, just ignore them and move on
        elif i is None or isinstance(i, bool):
            return i
        # A couple singletons use ints as input, just cast it to a string and don't throw a warning
        elif isinstance(i, int):
            return str(i)
        # It's something we don't know, but try to cast it to a string anyway
        else:
            try:
                logging.warning(f"Type {type(i)} passed to EZRegex, auto-casting to a string. Special characters will will not be escaped.")
                return str(i)
            except:
                raise ValueError(f'Incorrect type {type(i)} given to EZRegex parameter: Must be string or another EZRegex chain.')

    def __call__(self, *args, **kwargs):
        """ This should be called by the user to specify the specific parameters of this instance i.e. anyof('a', 'b') """
        # If this is being called without parameters, just compile the chain.
        # If it's being called *with* parameters, then it better be a fundemental
        # member, otherwise that doesn't make any sense.
        if len(self.funcList) > 1:
            if not len(args) and not len(kwargs):
                return self._compile()
            else:
                raise ValueError("You're trying to pass parameters to a chain of expressions. That doesn't make any sense. Stop that.")

        # Sanatize the arguments
        args = list(map(self._sanitizeInput if self.sanatize else deepcopy, args))

        _kwargs = {}
        for key, val in kwargs.items():
            _kwargs[key] = self._sanitizeInput(val) if self.sanatize else deepcopy(val)

        return EZRegex(
            [partial(self.funcList[0], *args, **_kwargs)],
            dialect=self.dialect,
            init=False,
            sanatize=self.sanatize,
            replacement=self.replacement,
            flags=self.flags
        )

    # Magic Functions
    def __str__(self, addFlags=True):
        return self._compile(addFlags)

    def __repr__(self):
        return 'EZRegex("' + self._compile() + '")'

    def __eq__(self, thing):
        return self._sanitizeInput(thing, addFlags=True) == self._compile()

    def __mul__(self, amt):
        if amt is Ellipsis:
            return EZRegex(f'(?{self})*', self.dialect, sanatize=False)
        rtn = self
        # This isn't optimal, but it's unlikely anyone will use this with large numbers
        for i in range(amt-1):
            # This doesn't work
            # rtn += self
            # But this does??
            rtn = rtn + self
        return rtn

    def __rmul__(self, amt):
        return self * amt

    def __imul__(self, amt):
        return self * amt

    def __add__(self, thing):
        return EZRegex(self.funcList + [partial(lambda cur=...: cur + self._sanitizeInput(thing))],
            dialect=self.dialect,
            init=False,
            sanatize=self.sanatize or thing.sanatize if isinstance(thing, EZRegex) else self.sanatize,
            replacement=self.replacement or thing.replacement if isinstance(thing, EZRegex) else self.replacement,
            flags=(self.flags + thing.flags) if isinstance(thing, EZRegex) else self.flags
        )

    def __radd__(self, thing):
        return EZRegex([partial(lambda cur=...: self._sanitizeInput(thing) + cur)] + self.funcList,
            dialect=self.dialect,
            init=False,
            sanatize=self.sanatize or thing.sanatize if isinstance(thing, EZRegex) else self.sanatize,
            replacement=self.replacement or thing.replacement if isinstance(thing, EZRegex) else self.replacement,
            flags=(self.flags + thing.flags) if isinstance(thing, EZRegex) else self.flags
        )

    def __iadd__(self, thing):
        # return self + self._sanitizeInput(thing)
        return self + thing

    def __and__(self, thing):
        warn('The & operator is unstable still. Use each() instead.')
        return EZRegex(fr'(?={self}){thing}', self.dialect, sanatize=False)

    def __rand__(self, thing):
        warn('The & operator is unstable still. Use each() instead.')
        return EZRegex(fr'(?={thing}){self}', self.dialect, sanatize=False)

    # The shift operators just shadow the add operators
    def __lshift__(self, thing):
        return self.__add__(thing)

    def __rlshift__(self, thing):
        return self.__radd__(thing)

    def __ilshift__(self, thing):
        return self.__iadd__(thing)

    # I don't think right and left shifts should be any different, right?
    def __rshift__(self, thing):
        return self.__add__(thing)

    def __rrshift__(self, thing):
        return self.__radd__(thing)

    def __irshift__(self, thing):
        return self.__iadd__(thing)

    def __invert__(self):
        return self.invert()

    def __not__(self):
        raise NotImplementedError('The not operator is not implemented. What you probably want is one of anyExcept(), anyCharExcept(), ifNotProceededBy(), or ifNotPreceededBy()')

    def __pos__(self):
        comp = self._compile()
        return EZRegex(('' if not len(comp) else r'(?:' + comp + r')') + r'+', self.dialect, sanatize=False)

    def __ror__(self, thing):
        print('ror called')
        return EZRegex(f'(?:{self._sanitizeInput(thing)}|{self._compile()})', self.dialect, sanatize=False)

    def __or__(self, thing):
        warn('The or operator is unstable and likely to fail, if used more than twice. Use anyof() instead, for now.')
        return EZRegex(f'(?:{self._compile()}|{self._sanitizeInput(thing)})', self.dialect, sanatize=False)

    def __xor__(self, thing):
        return NotImplemented

    def __rxor__(self, thing):
        return NotImplemented

    def __mod__(self, other):
        """ I would prefer __rmod__(), but it doesn't work on strings, since __mod__() is already specified for string formmating. """
        # I don't need to check this, re will do it for me
        # if not isisntance(other, str):
            # raise TypeError(f"Can't search type {type(other)} ")
        return re.search(other, self._compile())

    def __hash__(self):
        if len(self.funcList) > 1:
            return hash(self._compile())
        # If we only have 1 function lined up, that means we haven't
        # been called at all. And that means we're one of the basic singletons,
        # because users aren't supposed to instantiate this class directly.
        # THAT means we can use this instance's pointer as a unique identifier.
        else:
            return hash(id(self))

    def __contains__(self, thing):
        assert isinstance(thing, str), "`in` statement can only be used with a string"
        return re.search(self._compile(), thing) is not None

    # I guess this isn't a thing? But it really should be.
    def __rcontains__(self, thing):
        assert isinstance(thing, str), "`in` statement can only be used with a string"
        return re.search(self._compile(), thing) is not None

    def __getitem__(self, args):
        # digit[2, 3]    # (2, 3)
        # digit[2, ...]  # (2, Ellipsis)
        # digit[2, None] # (2, None)
        # digit[2, ]     # (2,)
        # digit[..., 3]  # (Ellipsis, 3)
        # digit[None, 3] # (None, 3)
        # digit[...:3]   # slice(Ellipsis, 3, None)
        # digit[None:3]  # slice(None, 3, None)
        # digit[:3]      # slice(None, 3, None)
        # digit[:]       # slice(None, None, None)
        # digit[2]       # 2

        # assert digit[2, 3] == match_range(2, 3, digit)
        # assert digit[2, ...] == digit[2,] == digit[2, None] == digit[2] == match_at_least(2, digit)
        # # assert digit[..., 2] == digit[0, 2] == digit[None, 2] == match_at_most(2, digit)
        # assert digit[...] == digit[0, ...] == digit[None] == at_least_0(digit)
        # assert digit[1, ...] == digit[1] == digit[1,] == digit[1, None] == at_least_1(digit)

        if type(args) is slice:
            # expr[...:end_expr] is equivalent to ZeroOrMore(expr, stop_on=end_expr)
            # assert digit[...:'foo'] == digit[None:'foo'] == digit[,'foo'] ==
            pass
        elif type(args) is not tuple or len(args) == 1:
            if type(args) is tuple:
                args = args[0]
            if args is None or args is Ellipsis or args == 0:
                # at_least_0(self)
                return EZRegex(fr'(?:{self._compile()})*', self.dialect, sanatize=False)
            elif args == 1:
                # at_least_1(self)
                return EZRegex(fr'(?:{self._compile()})+', self.dialect, sanatize=False)
            else:
                # match_at_least(args, self)
                return EZRegex(fr'(?:{self._compile()}){{{args},}}', self.dialect, sanatize=False)
        else:
            start, end = args
            if start is None or start is Ellipsis:
                # match_at_most(2, self)
                return EZRegex(fr'(?:{self._compile()}){{0,{end}}}', self.dialect, sanatize=False)
            elif end is None or end is Ellipsis:
                if start == 0:
                    # at_least_0(self)
                    return EZRegex(fr'(?:{self._compile()})*', self.dialect, sanatize=False)
                elif start == 1:
                    # at_least_1(self)
                    return EZRegex(fr'(?:{self._compile()})+', self.dialect, sanatize=False)
                else:
                    # match_at_least(start, self)
                    return EZRegex(fr'(?:{self._compile()}){{{start},}}', self.dialect, sanatize=False)
            else:
                # match_range(start, end, self)
                return EZRegex(fr'(?:{self._compile()}){{{start},{end}}}', self.dialect, sanatize=False)

    def __reversed__(self):
        return self.inverse()

    def __rich__(self):
        return self._compile()

    def __pretty__(self):
        return self._compile()

    # Regular functions
    def _compile(self, addFlags=True):
        regex = ''
        for func in self.funcList:
            regex = func(cur=regex)

        # Add the flags
        if addFlags:
            regex = self._dialect['beginning'] + regex + self._dialect['end']
            if len(self.flags):
                regex = self._dialect['flag_func'](regex, self.flags)
        return regex

    def compile(self, addFlags=True):
        return re.compile(self._compile(addFlags))

    def str(self):
        return self.__str__()

    def debug(self):
        try:
            from Cope import debug
        except ModuleNotFoundError:
            print(f"Compiled ezregex string = {self}")
        else:
            debug(self, name='Compiled ezregex string', calls=2)
        return self

    def debugStr(self):
        return self.debug().str()

    def copy(self, addFlags=True):
        try:
            from clipboard import copy
        except ImportError as err:
            raise ModuleNotFoundError('Please install the clipboard module in order to auto copy '
                                      'ezregex expressions (i.e. pip install clipboard)') from err
        else:
            copy(self._compile(addFlags=addFlags))

    def test(self, testString=None, show=True, context=True) -> bool:
        """ Tests the current regex expression to see if it's in @param testString.
            Returns the match objects (None if there was no match)"""
        from rich import print as rprint
        from rich.panel import Panel
        from rich.text import Text

        # json = self._matchJSON(testString=testString)
        json = api(self, test_string=testString)
        if not show:
            return bool(len(json['matches']))

        _cope = False
        if context:
            # Use the nice context function in the Cope library
            try:   from Cope import get_context, get_metadata
            except ImportError: pass
            else:  _cope = True

        st = Text()  # String
        gt = Text()  # Groups (all the group-related text)
        defaultColor = 'bold'
        textColor = ''

        st.append("Testing expression", style=defaultColor)
        # Add the context line
        if _cope:
            st.append(f' (from {get_context(get_metadata(2), False, True, True).strip()})', style=defaultColor)
        st.append(':\n', style=defaultColor)

        # The expression we're testing
        st.append(f'\t{json["regex"]}\n', style=textColor)
        st.append("for matches in:\n\t", style=defaultColor)

        # Add the main string
        for color, background, part in json['parts']:
            st.append(part, style=color if background is None else f'{color} on {background}')
        st.append('\n')

        # Add all the matches and groups
        for m in json['matches']:
            gt.append('Match = "')
            for color, background, part in m['match']['parts']:
                gt.append(part, style=color if background is None else f'{color} on {background}')
            gt.append('" ')
            gt.append(f"({m['match']['start']}:{m['match']['end']})", style='italic bright_black')
            gt.append('\n')
            if len(m['unnamedGroups']):
                gt.append('Unnamed Groups:\n')
            for cnt, group in enumerate(m['unnamedGroups']):
                gt.append(f'\t{cnt+1}: "')
                gt.append(group['string'], style=group['color'])
                gt.append('" ')
                gt.append(f"({group['start']}:{group['end']})", style='italic bright_black')
                gt.append('\n')
            if len(m['namedGroups']):
                gt.append('Named Groups:\n')
            for name, group in m['namedGroups'].items():
                gt.append(f'\t{name}: "')
                gt.append(group['string'], style=group['color'])
                gt.append('" ')
                gt.append(f"({group['start']}:{group['end']})", style='italic bright_black')
                gt.append('\n')
            gt.append('\n')

        # Assemble everything into a panel
        rprint(Panel(Text.assemble(*st, '\n', *gt),
            title='Testing Regex',
            subtitle=Text('Found\n', style='blue') if len(json['matches'])
                else Text('Not Found\n', style='red')))  #, border_style='dim green')

        return bool(len(json['matches']))

    def inverse(self, amt=1, **kwargs):
        """ "Inverts" the current Regex expression to give an example of a string it would match.
            Useful for debugging purposes. """
        return '\n'.join([invert(self._compile(), **kwargs) for _ in range(amt)])
