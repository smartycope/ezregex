import logging
import re
from abc import ABC
from functools import partial
from .api import api
from .generate import *
from .invert import invert

from .base import base, psuedonymns

# TODO: Seperate EZRegex into a "bytes" mode vs "string" mode
# TODO: consider changing add_flags to "outer" or "end" or something
# TODO: Seriously consider removing the debug functions
# TODO: in all the magic functions assert that we're not mixing dialects
# TODO: figure out if theres a way to make a "change dialect" function
# TODO: B.join((A, C))
# TODO: sre.concatenate((A, B, C)) or A + B + C (if I'd fancy the plus-style syntax more than flow-style)

class EZRegex(ABC):
    """ Represent parts of the Regex syntax. Should not be instantiated by the user directly."""

    def __init__(self, definition, *, sanatize=True, replacement=False, flags='', options_specified=False):
        """
        The workhorse of the EZRegex library. This represents a regex pattern that can be combined
        with other EZRegexs and strings. Ideally, this should only be called internally, but it should
        still work from the user's end
        """
        # Set attributes like this so the class can remain "immutable", while still being usable
        self.__setattr__('_flags', flags, True)
        self.__setattr__('_sanatize', sanatize, True)
        self.__setattr__('_options_specified', options_specified, True)
        self.__setattr__('replacement', replacement, True)

        if isinstance(definition, str):
            self.__setattr__('_funcList', [lambda cur=...: cur + definition], True)
        elif callable(definition):
            self.__setattr__('_funcList', [definition], True)
        elif isinstance(definition, list):
            self.__setattr__('_funcList', definition, True)

    # Private functions
    def _flag_func(self, final:str) -> str:
        """ This function is called to add the flags to the regex. It gets called even if there are no flags """
        if self.flags and not self.replacement:
            return f'(?{self.flags}){final}'
        return final


    def _final_func(self, s:str) -> str:
        return s

    def _escape(self, pattern:str):
        return self.escape(pattern, self.replacement)

    @classmethod
    def escape(cls, pattern:str, replacement=False):
        """ Available as a class method, so we can escape strings when defining singletons
            The user could use this, but I can't think of a reason they would want to.
        """
        # This function was modified from the one in /usr/lib64/python3.12/re/__init__.py line 255
        _special_chars_map = {i: '\\' + chr(i) for i in (cls._repl_escape_chars if replacement else cls._escape_chars)}
        return pattern.translate(_special_chars_map)

    def _sanitizeInput(self, i, add_flags=False):
        """ Instead of raising an error if passed a strange datatype, it now tries to cast it to a string """
        # If it's another chain, compile it
        if isinstance(i, EZRegex):
            return i._compile(add_flags=add_flags)
        # It's a string (so we need to escape it)
        # If this is a replacement string, it will automatically escape based on _repl_escape_chars
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

    def _compile(self, add_flags=True):
        regex = ''
        for func in self._funcList:
            regex = func(cur=regex) # type: ignore

        # Add the flags
        if add_flags:
            # Remove duplicate flags
            self.__setattr__('_flags', ''.join(set(self._flags)), True)

            regex = self._flag_func(regex)

            # This has to go in the add_flags scope so it only runs at the very end, like flags
            regex = self._final_func(regex)
        return regex

    def _copy(self, definition=..., sanatize=..., replacement=..., flags=..., options_specified=...):
        if definition is Ellipsis:
            definition = self._compile()
        if sanatize is Ellipsis:
            sanatize = self._sanatize
        if replacement is Ellipsis:
            replacement = self.replacement
        if flags is Ellipsis:
            flags = self._flags
        if options_specified is Ellipsis:
            options_specified = self._options_specified

        return type(self)(definition, sanatize=sanatize, replacement=replacement, flags=flags, options_specified=options_specified)

    def _base(self, element, /, *args, **kwargs):
        """ Constructs the base element specified, and returns it passed with any additional arguements """
        return type(self)(**base[element])(*args, **kwargs)

    # Regular functions
    def str(self):
        return self.__str__()

    def debug(self):
        try:
            from Cope import debug
        except ImportError:
            print(f"Compiled ezregex string = {self}")
        else:
            debug(self, name='Compiled ezregex string', calls=2)
        return self

    def copy(self, add_flags=True):
        try:
            from clipboard import copy  # type: ignore
        except ImportError as err:
            raise ImportError(
                'Please install the clipboard module in order to auto copy ezregex expressions (i.e. pip install clipboard)'
            ) from err
        else:
            copy(self._compile(add_flags=add_flags))

    def test(self, testString=None, show=True, context=True) -> bool:
        """ Tests the current regex expression to see if it's in @param testString.
            Returns the match objects (None if there was no match)
        """
        try:
            from rich import print as rprint
            from rich.panel import Panel
            from rich.text import Text
        except ImportError:
            raise ImportError("The rich library is required to use the EZRegex.test() method. Try running `pip install rich`")

        # json = self._matchJSON(testString=testString)
        json = api(self, test_string=testString)
        if not show:
            return bool(len(json['matches']))

        st = Text()  # String
        gt = Text()  # Groups (all the group-related text)
        defaultColor = 'bold'
        textColor = ''

        st.append("Testing expression", style=defaultColor)
        # Add the context line
        # st.append(f' (from {get_context(get_metadata(2), False, True, True).strip()})', style=defaultColor)
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
            if len(m['unnamed groups']):
                gt.append('Unnamed Groups:\n')
            for id, group in m['unnamed groups'].items():
                gt.append(f'\t{id}: "')
                gt.append(['string'], style=group['color'])
                gt.append('" ')
                gt.append(f"({group['start']}:{group['end']})", style='italic bright_black')
                gt.append('\n')
            if len(m['named groups']):
                gt.append('Named Groups:\n')
            for name, group in m['named groups'].items():
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

    def invert(self, amt=1, **kwargs):
        return self.inverse(amt, **kwargs)

    # Elemental functions
    def group(self, name=None):
        return self._base('group', self, name=name)

    def named(self, name):
        return self.group(name)

    @property
    def unnamed(self):
        return self.group()

    def if_not_preceded_by(self, input):
        return self._base('if_not_preceded_by', input) + self

    def if_preceded_by(self, input):
        return self._base('if_preceded_by', input) + self

    def if_not_proceded_by(self, input):
        return self + self._base('if_not_proceded_by', input)

    def if_proceded_by(self, input):
        return self + self._base('if_proceded_by', input)

    def if_not_followed_by(self, input):
        return self.if_not_proceded_by(input)

    def if_followed_by(self, input):
        return self.if_proceded_by(input)

    def if_enclosed_with(self, open, closed=None):
        return self._base('if_enclosed_with', self, open, closed)

    @property
    def optional(self):
        return self._base('optional', self)

    @property
    def repeat(self):
        return self._base('repeat', self)

    @property
    def exactly(self):
        return self._base('is_exactly', self)

    def at_least(self, min):
        return self._base('at_least', min, self)

    def more_than(self, min):
        return self._base('more_than', min, self)

    def amt(self, amt):
        return self._base('amt', amt, self)

    def at_most(self, max):
        return self._base('at_most', max, self)

    def between(self, min, max, greedy=True, possessive=False):
        return self._base('between', min, max, self, greedy=greedy, possessive=possessive)

    def at_least_one(self, greedy=True, possessive=False):
        return self._base('at_least_one', self, greedy=greedy, possessive=possessive)

    def at_least_none(self, greedy=True, possessive=False):
        return self._base('at_least_none', self, greedy=greedy, possessive=possessive)

    def or_(self, input):
        return self._base('either', self, input)

    # Named operator functions
    def append(self, input):
        return self + input

    def prepend(self, input):
        return input + self

    # Flag functions
    @property
    def flags(self):
        return self._flags

    def set_flags(self, to):
        return self._copy(flags=to)

    def add_flag(self, flag):
        if flag not in self._flags:
            return self._copy(flags=self._flags + flag)
        return self

    def remove_flag(self, flag):
        if flag in self._flags:
            return self._copy(flags=self._flags.replace(flag, ''))
        return self

    # Magic Functions
    def __call__(self, *args, **kwargs):
        """ This should be called by the user to specify the specific parameters of this instance i.e. anyof('a', 'b') """
        # If this is being called without parameters, just compile the chain.
        # If it's being called *with* parameters, then it better be a fundemental
        # member, otherwise that doesn't make any sense.
        if len(self._funcList) > 1:
            if not len(args) and not len(kwargs):
                return self._compile()
            else:
                raise TypeError("You're trying to pass parameters to a chain of expressions. That doesn't make any sense. Stop that.")

        # Sanatize the arguments
        if self._sanatize:
            args = list(map(self._sanitizeInput, args))

        _kwargs = {}
        for key, val in kwargs.items():
            _kwargs[key] = self._sanitizeInput(val) if self._sanatize else val

        return self._copy([partial(self._funcList[0], *args, **_kwargs)])

    def __str__(self):
        return self._compile()

    def __repr__(self):
        return f'{type(self).__name__}("{self}")'

    def __eq__(self, thing):
        """ NOTE: This will return True for equivelent EZRegex expressions of different dialects """
        return self._sanitizeInput(thing, add_flags=True) == self._compile()

    def __mul__(self, amt):
        if amt is Ellipsis:
            return self._copy(f'(?{self})*', sanatize=False)
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
        if self._options_specified and isinstance(thing, EZRegex) and thing._options_specified:
            raise ValueError('Please only specify options once per EZRegex expression')

        return self._copy(
            self._funcList + [partial(lambda cur=...: cur + self._sanitizeInput(thing))],
            sanatize=self._sanatize or thing._sanatize if isinstance(thing, EZRegex) else self._sanatize,
            replacement=self.replacement or thing.replacement if isinstance(thing, EZRegex) else self.replacement,
            flags=(self._flags + thing.flags) if isinstance(thing, EZRegex) else self._flags,
            options_specified=self._options_specified or thing._options_specified if isinstance(thing, EZRegex) else self._options_specified
        )

    def __radd__(self, thing):
        if self._options_specified and isinstance(thing, EZRegex) and thing._options_specified:
            raise ValueError('Please only specify options once per EZRegex expression')

        return self._copy([partial(lambda cur=...: self._sanitizeInput(thing) + cur)] + self._funcList,
            sanatize=self._sanatize or thing._sanatize if isinstance(thing, EZRegex) else self._sanatize,
            replacement=self.replacement or thing.replacement if isinstance(thing, EZRegex) else self.replacement,
            flags=(self._flags + thing.flags) if isinstance(thing, EZRegex) else self._flags,
            options_specified=self._options_specified or thing._options_specified if isinstance(thing, EZRegex) else self._options_specified,
        )

    def __iadd__(self, thing):
        return self + thing

    def __and__(self, thing):
        raise NotImplementedError
        logging.warning('The & operator is unstable still. Use each() instead.')
        return EZRegex(fr'(?={self}){thing}', self.dialect, sanatize=False)

    def __rand__(self, thing):
        raise NotImplementedError
        logging.warning('The & operator is unstable still. Use each() instead.')
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

    def __pos__(self):
        comp = self._compile(add_flags=False)
        return self._copy(('' if not len(comp) else r'(?:' + comp + r')') + r'+', sanatize=False)

    def __ror__(self, thing):
        return self._copy(f'(?:{self._sanitizeInput(thing)}|{self._compile(add_flags=False)})', sanatize=False)

    def __or__(self, thing):
        logging.warning('The or operator is unstable and likely to fail, if used more than twice. Use anyof() instead, for now.')
        return self._copy(f'(?:{self._compile(add_flags=False)}|{self._sanitizeInput(thing)})', sanatize=False)

    def __xor__(self, thing):
        return NotImplementedError

    def __rxor__(self, thing):
        return NotImplementedError

    def __mod__(self, other):
        """ I would prefer __rmod__(), but it doesn't work on strings, since __mod__() is already specified for string formmating. """
        # I don't need to check this, re will do it for me
        # if not isisntance(other, str):
            # raise TypeError(f"Can't search type {type(other)} ")
        return re.search(other, self._compile(add_flags=False))

    def __hash__(self):
        if len(self._funcList) > 1:
            return hash(self._compile())
        # If we only have 1 function lined up, that means we haven't
        # been called at all. And that means we're one of the basic singletons,
        # because users aren't supposed to instantiate this class directly.
        # THAT means we can use this instance's pointer as a unique identifier.
        else:
            return hash(id(self))

    def __contains__(self, thing):
        # assert isinstance(thing, str), "`in` statement can only be used with a string"
        return re.search(self._compile(), thing) is not None

    def __rcontains__(self, thing):
        """ I guess this isn't a thing? But it really should be. """
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
                return self._copy(fr'(?:{self._compile(False)})*', sanatize=False)
            elif args == 1:
                # at_least_1(self)
                return self._copy(fr'(?:{self._compile(False)})+', sanatize=False)
            else:
                # match_at_least(args, self)
                return self._copy(fr'(?:{self._compile(False)}){{{args},}}', sanatize=False)
        else:
            start, end = args
            if start is None or start is Ellipsis:
                # match_at_most(2, self)
                return self._copy(fr'(?:{self._compile(False)}){{0,{end}}}', sanatize=False)
            elif end is None or end is Ellipsis:
                if start == 0:
                    # at_least_0(self)
                    return self._copy(fr'(?:{self._compile(False)})*', sanatize=False)
                elif start == 1:
                    # at_least_1(self)
                    return self._copy(fr'(?:{self._compile(False)})+', sanatize=False)
                else:
                    # match_at_least(start, self)
                    return self._copy(fr'(?:{self._compile(False)}){{{start},}}', sanatize=False)
            else:
                # match_range(start, end, self)
                return self._copy(fr'(?:{self._compile(False)}){{{start},{end}}}', sanatize=False)

    def __reversed__(self):
        return self.inverse()

    def __rich__(self):
        return self._compile()

    def __pretty__(self):
        return self._compile()

    def __setattr__(self, name, value, ignore=False):
        if ignore:
            self.__dict__[name] = value
        else:
            raise TypeError('EZRegex objects are immutable')

    def __delattr__(self, name, ignore=False):
        if ignore:
            del self.__dict__[name]
        else:
            raise TypeError('EZRegex objects are immutable')
