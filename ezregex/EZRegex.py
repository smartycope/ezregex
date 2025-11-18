from abc import ABC
from functools import partial
from inspect import signature
import logging
import re
# TODO: Unpack is only 3.11+
from typing import Any, Callable, Tuple, Dict, Unpack, List, Set

# from mypy_extensions import DefaultNamedArg, VarArg

from .api import api
from .psuedonyms import psuedonyms, all_psuedonyms
# from ezregex.generate import generate_regex
from .invert import invert
from .types import EZRegexFunc, EZRegexType, EZRegexDefinition, EZRegexOther, EZRegexParam

# TODO: Seperate EZRegex into a "bytes" mode vs "string" mode
# TODO: consider changing add_flags to "outer" or "end" or something
# TODO: a lot of the raised ValueErrors should probably a custom Exception. Something like UnimplementedDialect or something

# TODO: tests to ensure adding cur to the end AND begining and modifying cur in a singleton method works properly

# These are here because having it be a class member as part of the parent and child classes
# seems to cause problems
initial_variables = {
    # Cast to sets so it can accept strings
    'flags': (set(), lambda l, r: set(l) | set(r)),
    'replacement': (False, lambda l, r: l or r),
    '_sanitize': (True, lambda l, r: l or r),
    '_options_specified': (False, lambda l, r: l or r),
}
"These propagate through the EZRegex chain, in ways defined by the lambda"

class EZRegex(ABC):
    """Represent parts of the Regex syntax. Should not be instantiated by the user directly"""

    _exclusions = ['_escape_chars', '_repl_escape_chars', '_variables', '_parse_any_of_params']
    "Excluded methods"
    _added_vars = {}
    "A dict of {method name: dict} to manually add variables to methods"

    # For linting's sake
    flags: set[str]
    replacement: bool
    _sanitize: bool
    _options_specified: bool
    _func_list: list[EZRegexFunc]

    @classmethod
    def exclude(cls:type, method:Callable):
        """ Exclude a method from being instantiated as a singleton member """
        cls._exclusions.append(method.__name__)
        return method

    # I thiiiiink this will work?
    @classmethod
    def add_vars(cls, method:Callable):
        """ Add variables to a method, similar to the `singleton = "abc", {"flags": "m"}` syntax """
        def inner(**kwargs):
            cls._added_vars[method.__name__] = kwargs
            return method
        return inner

    @staticmethod
    def _interpret_definition(type_:type, definition:EZRegexDefinition|list):
        """ Interpret a definition into an instantiated EZRegex subclass object of type `type_`"""

        if isinstance(definition, str):
            return type_([lambda cur=...: cur + definition])

        elif isinstance(definition, tuple):
            assert len(definition) == 2, f'Definition {definition} is not a tuple of length 2'
            assert isinstance(definition[1], dict), f'Definition {definition} is a tuple of 2, but the second element is not a dictionary'
            if type(definition[0]) is str:
                assert all(k in type_._variables for k in definition[1].keys()), f'Definition {definition} is a tuple of 2, but not all of the keys are in the dialect\'s variables (avilable variables: {type_._variables})'
                return type_([lambda cur=...: cur + definition[0]], **definition[1])
            elif callable(definition[0]):
                return type_([definition[0]], **definition[1])
            else:
                raise ValueError(f'Definition {definition} is a tuple of 2, but the first element is not a string or callable')

        elif callable(definition):
            # Make sure the callable has the right signature
            sig = signature(definition)
            assert 'cur' in sig.parameters, f'Definition {definition} does not have cur as a keyword parameter'
            assert sig.parameters['cur'].default == ..., f'Definition {definition} does not have cur as a keyword parameter with default value of ...'
            return type_([definition], **type_._added_vars.get(definition.__name__, {}))

        elif isinstance(definition, list):
            return type_(definition)

    @staticmethod
    def _parse_options_params(flag_map, *args, normalize_case=True, **kwargs):
        if normalize_case:
            for key, value in flag_map.copy().items():
                flag_map[key.upper()] = flag_map[key.lower()] = value

        flags = set()
        for arg in args:
            if arg in flag_map:
                flags.add(flag_map[arg])
            else:
                raise ValueError(f'Unknown flag: {arg}. Available flags: {tuple(flag_map.keys())}')

        for key, value in kwargs.items():
            if key in flag_map:
                if value:
                    flags.add(flag_map[key])
                else:
                    try:
                        flags.remove(flag_map[key])
                    except KeyError:
                        pass
            else:
                raise ValueError(f'Unknown flag: {key}. Available flags: {tuple(flag_map.keys())}')

        return ''.join(flags)

    @staticmethod
    def _generate_options_from_flags(type_:type, flag_map, normalize_case=True, docs_map={}, docs_link=''):
        # This is a function, not an EZRegex subclass, by intention, even though it's used like one
        def options(*args, **kwargs):
            flags = EZRegex._parse_options_params(flag_map, *args, normalize_case=normalize_case, **kwargs)
            return type_(lambda cur=...: cur, flags=flags, options_specified=True)

        docs = ''
        if docs_link:
            docs += f"Documentation: \n\t{docs_link}\n\n"
        docs += '''Usage:
        word + options(ignore_case=True)
        word + options('ignore_case')
        word + options('ignore_case', 'multiline')
        word + options('ignore_case', multiline=True)

    Args:
    '''
        _docs = {k.lower(): v for k, v in docs_map.items()}
        for flag in flag_map.keys():
            try:
                docs += f"\t{flag.lower()}:\n\t\t{_docs[flag.lower()]}\n"
            except KeyError:
                docs += f"\t{flag.lower()}\n"
        options.__doc__ = docs

        return options

    def __init_subclass__(
        cls:type,
        escape_chars:bytes,
        flags:dict[str, str],
        repl_escape_chars:bytes=b'',
        flags_docs_map:dict[str, str]={},
        flags_docs_link:str='',
        variables:Unpack[Dict[str, EZRegexDefinition]]={},
        **kwargs
    ):
        # Validate & set escape_chars
        assert isinstance(escape_chars, bytes), f'Escape chars {escape_chars} is not bytes'
        assert isinstance(repl_escape_chars, bytes), f'Replacement escape chars {repl_escape_chars} is not bytes'
        cls._escape_chars = escape_chars
        cls._repl_escape_chars = repl_escape_chars

        # Validate & set variables
        for v in variables.values():
            assert isinstance(v, tuple), f'Value {v} is not a tuple'
            assert len(v) == 2, f'Value {v} is not a tuple of length 2'
            assert callable(v[1]), f'Value {v} is a tuple of 2, but the second element is not callable'
            # Make sure the callable has the right signature
            sig = signature(v[1])
            assert len(sig.parameters) == 2, f'Value {v} is a tuple of 2, but the second element is not a callable with 2 parameters'
        cls._variables = variables | initial_variables

        # Instantiate members & methods
        for name in cls.parts(include_psuedonyms=False):
            value = getattr(cls, name)
            if value is None:
                delattr(cls, name)
            else:
                setattr(cls, name, EZRegex._interpret_definition(cls, value))

        # Validate flag params, and generate the options function
        assert isinstance(flags, dict), f'Flags {flags} is not a dictionary'
        assert isinstance(flags_docs_map, dict), f'Flags docs map {flags_docs_map} is not a dictionary'
        assert isinstance(flags_docs_link, str), f'Flags docs link {flags_docs_link} is not a string'
        cls.options = cls._generate_options_from_flags(cls, flags, True, flags_docs_map, flags_docs_link)

        # For the sake of brevity, these are here. No different than being defined below
        cls.__imul__ = cls.__mul__
        cls.__iadd__ = cls.__add__
        # The shift operators just shadow the add operators
        # I don't think right and left shifts should be any different, right?
        cls.__lshift__ = cls.__rshift__ = cls.__add__
        cls.__rlshift__ = cls.__rrshift__ = cls.__radd__
        cls.__ilshift__ = cls.__irshift__ = cls.__iadd__

        cls.invert = cls.__invert__ = cls.__reversed__ = cls.inverse

        # Add all the psuedonymns
        def to_camel_case(s):
            return ''.join((word.capitalize() if cnt else word) for cnt, word in enumerate(s.split('_')))

        for name, ps in psuedonyms.items():
            if hasattr(cls, name):
                value = getattr(cls, name)
                setattr(cls, to_camel_case(name), value)

                for p in ps:
                    setattr(cls, p, value)
                    # also add camelCase versions of the psuedonyms
                    setattr(cls, to_camel_case(p), value)

        # Make the subclass immutable
        cls.__setattr__ = cls._raise_immutibility
        cls.__delattr__ = cls._raise_immutibility
        cls.__set__ = cls._raise_immutibility
        cls.__delete__ = cls._raise_immutibility

        return super().__init_subclass__(**kwargs)

    def __init__(self, func_list:list[EZRegexFunc]=[], **variable_values):
        # Use the defaults, which can get overriden if we're given variable values (i.e. by _combine())
        self.__dict__.update({k: v[0] for k, v in self._variables.items()})
        self.__dict__.update(variable_values)

        # Now that we're instantiated, we're immutable
        self.__dict__['_func_list'] = func_list

    def _combine(self, other:EZRegexOther, cls:type, add_to_end:bool=True):
        if isinstance(other, EZRegex) and not isinstance(other, type(self)):
            raise ValueError('Cannot combine EZRegex objects of different dialects')

        if add_to_end:
            func_list = self._func_list + [self._sanitize_other(other)]
            # func_list = self._func_list + [lambda cur=...: cur + self._sanitize_input(other)]
        else:
            func_list = [self._sanitize_other(other)] + self._func_list
            # func_list = [lambda cur=...: self._sanitize_input(other) + cur] + self._func_list
        return cls(
            func_list,
            # Use the combination functions to combine & propagate the variables
            **{
                # combine_spec is (default_value, lamdba l, r: ...)
                var: combine_spec[1](
                    self.__dict__[var],
                    other.__dict__[var] if isinstance(other, type(self)) else combine_spec[0]
                )
                for var, combine_spec in
                self._variables.items()
            }
        )

    def _sanitize_param(self, i:EZRegexParam, add_flags:bool=False):
        """ Sanitize things that are passed as parameters to a singleton member. """
        # If it's another chain, compile it
        if isinstance(i, EZRegex):
            return i._compile(add_flags=add_flags)
        # It's a string (so we need to escape it)
        # If this is a replacement string, it will automatically escape based on _repl_escape_chars
        elif isinstance(i, str):
            return self._escape(i)
        elif isinstance(i, bool):
            return i
        elif isinstance(i, int):
            return str(i)
        # It's something we don't know, try to cast it to a string anyway
        else:
            try:
                logging.warning(f"Type {type(i)} passed to EZRegex, auto-casting to a string. Special characters will will not be escaped.")
                return str(i)
            except Exception as e:
                raise ValueError(f'Incorrect type {type(i)} given to EZRegex parameter: Must be string or another EZRegex chain.') from e

    def _sanitize_other(self, other:EZRegexOther, add_flags:bool=False) -> Callable[[str], str]:
        """ Sanitize things that are combined with the current chain (i.e. via +) """
        # If it's another chain, compile it
        if isinstance(other, EZRegex):
            return lambda cur=...: other._compile(cur, add_flags=add_flags)
        # It's a string (so we need to escape it)
        # If this is a replacement string, it will automatically escape based on _repl_escape_chars
        elif isinstance(other, str):
            return lambda cur=...: cur + self._escape(other)
        # Allow word + 1 -> "\w+1"
        elif isinstance(other, int):
            return lambda cur=...: cur + str(other)
        # It's something we don't know, try to cast it to a string anyway
        else:
            try:
                logging.warning(f"Attempting to combine type {type(other)} with EZRegex, auto-casting to a string. Special characters will will not be escaped.")
                return lambda cur=...: cur + str(other)
            except Exception as e:
                raise ValueError(f'Incorrect type {type(other)} given to EZRegex parameter: Must be string or another EZRegex chain.') from e

    def _escape(self, pattern:str, replacement:bool=False):
        """ Available as a class method, so we can escape strings when defining singletons
            The user could use this, but I can't think of a reason they would want to.
        """
        # This function was modified from the one in /usr/lib64/python3.12/re/__init__.py line 255
        _special_chars_map = {i: '\\' + chr(i) for i in (self.repl_escape_chars if replacement else self.escape_chars)}
        return pattern.translate(_special_chars_map)

    def _raise_immutibility(self, *_args, **_kwargs):
        raise TypeError('EZRegex objects are immutable')

    def _compile(self, regex:str='', add_flags:bool=True) -> str:
        for func in self._func_list:
            regex = func(cur=regex)

        # Add the flags
        if add_flags:
            regex = self._flag_func(regex)

        # This used to go in the add_flags scope so it only ran at the very end, like flags
        regex = self._final_func(regex)
        return regex

    # Abstract methods
    def _flag_func(self, final:str) -> str:
        """ This function is called to add the flags to the regex. It gets called even if there are no flags """
        if self.flags and not self.replacement:
            return f'(?{''.join(self.flags)}){final}'
        return final

    def _final_func(self, compiled:str) -> str:
        """ Gets called just before returning the compiled string to the user. Useful for adding things like
            Javascript's slashes (i.e. /regex/)
        """
        return compiled

    def _escape(self, pattern:str):
        return self.escape(pattern, self.replacement)

    @classmethod
    def escape(cls, pattern:str, replacement:bool=False) -> str:
        """ Available as a class method, so we can escape strings when defining singletons
            The user could use this, but I can't think of a reason they would want to.
        """
        # This function was modified from the one in /usr/lib64/python3.12/re/__init__.py line 255
        _special_chars_map = {i: '\\' + chr(i) for i in (cls._repl_escape_chars if replacement else cls._escape_chars)}
        return pattern.translate(_special_chars_map)

    # Regular functions
    @classmethod
    def parts(cls, include_psuedonyms=True):
        """ A utility function that lists all the names of all singleton methods in this dialect
            This excludes dunder methods, abstract methods, and any methods marked with @exclude
        """
        return [i
            for i in dir(cls)
            if (
                i not in dir(EZRegex) and
                not i.startswith('__') and
                i not in cls._exclusions and
                (include_psuedonyms or i not in all_psuedonyms)
            )
        ]

    def str(self):
        return self._compile()

    def copy(self, add_flags:bool=True):
        try:
            from clipboard import copy  # type: ignore
        except ImportError as err:
            raise ImportError(
                'Please install the clipboard module in order to auto copy ezregex expressions (i.e. pip install clipboard)'
            ) from err
        else:
            copy(self._compile(add_flags=add_flags))

    def test(self, testString:str=None, show:bool=True, context:bool=True) -> bool:
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

    def inverse(self, amt:int=1, **kwargs) -> str:
        """ "Inverts" the current Regex expression to give an example of a string it would match.
            Useful for debugging purposes. """
        return '\n'.join([invert(self._compile(), **kwargs) for _ in range(amt)])

    # TODO: think through this
    # def or_(self, input):
        # return self._base('either', self, input)

    # Named operator functions
    # TODO: ensure these have tests (there's a possibility these are backwards)
    def append(self, input:EZRegexOther) -> EZRegexType:
        return self._combine(input, type(self))

    def prepend(self, input:EZRegexOther) -> EZRegexType:
        return self._combine(input, type(self), add_to_end=False)

    # TODO: tests for this
    def concat(self, *args):
        """ Join multiple EZRegex singleton members together
        The following are all equivelent:
            Dialect.concat(a, b, c)
            Dialect.concat((a, b, c))
            Dialect.a.b.c
            a + b + c
            a.b.c
        """
        if len(args) == 1 and isinstance(args[0], (tuple, list)):
            args = args[0]

        if len(args) == 0:
            raise ValueError('concat requires at least one argument')

        chain = args[0]
        for i in args[1:]:
            chain += i

        return chain

    # Flag functions
    def set_flags(self, flags:str|Set[str]):
        """ Directly sets flags in an EZRegex instance
            NOTE: you most likely don't want this, you likely want .options()
            This sets flags directly, not the names of the flags
        """
        return type(self)(self._func_list, flags=set(flags))

    def add_flags(self, flags:str|Set[str]):
        """ Adds a flag to an EZRegex instance
            NOTE: you most likely don't want this, you likely want .options()
            This adds flags directly, not the names of the flags
        """
        return type(self)(self._func_list, flags=set(self.flags) | set(flags))

    def remove_flags(self, flags:str|Set[str]):
        """ Removes a flag from an EZRegex instance """
        return type(self)(self._func_list, flags=set(self.flags) - set(flags))

    # Magic Functions
    def __call__(self, *args:Unpack[List[EZRegexParam]], **kwargs:Unpack[Dict[str, EZRegexParam]]):
        """ This should be called by the user to specify the specific parameters of this instance i.e. anyof('a', 'b') """
        # If this is being called without parameters, still complain, that's weird.
        # If it's being called *with* parameters, then it better be a fundemental
        # member, otherwise that doesn't make any sense.
        if len(self._func_list) != 1:
            raise TypeError("You're trying to pass parameters to a chain of expressions. That doesn't make any sense. Stop that.")

        # Sanatize the arguments
        if self._sanitize:
            args = tuple(map(self._sanitize_param, args))

        _kwargs = {}
        for key, val in kwargs.items():
            _kwargs[key] = self._sanitize_param(val) if self._sanitize else val

        return type(self)([partial(self._func_list[0], *args, **_kwargs)], **self.__dict__)

    def __get__(self, instance:EZRegexType|None, owner:type) -> EZRegexType:
        # We're trying to access it as a class member. This is how chains are started
        if instance is None:
            return self
        return instance._combine(self, owner)

    def __eq__(self, other:EZRegexOther) -> bool:
        """ NOTE: This will return True for equivelent EZRegex expressions of different dialects
            ALSO NOTE: This checks flags as well
        """
        if not isinstance(other, type(self)):
            return False
        return other._compile() == self._compile()

    def __add__(self, other:EZRegexOther) -> EZRegexType:
        return self._combine(other, type(self))

    def __radd__(self, other:EZRegexOther) -> EZRegexType:
        return self._combine(other, type(self), add_to_end=False)

    def __mul__(self, amt):
        if amt is Ellipsis:
            try:
                return type(self).at_least_none(self)
            except AttributeError:
                raise ValueError(f'at_least_none is not supported in {type(self).__name__}') from None

        rtn = self
        # This isn't optimal, but it's unlikely anyone will use this with large numbers
        for _ in range(amt-1):
            # This doesn't work
            # rtn += self
            # But this does??
            rtn = rtn + self
        return rtn

    def __rmul__(self, amt):
        return amt.__mul__(self)

    def __and__(self, other:EZRegexOther) -> EZRegexType:
        raise NotImplementedError

    def __rand__(self, other:EZRegexOther) -> EZRegexType:
        raise NotImplementedError

    def __pos__(self):
        try:
            return type(self).at_least_one(self)
        except AttributeError:
            raise ValueError(f'at_least_one is not supported in {type(self).__name__}') from None

    def __or__(self, other:EZRegexOther) -> EZRegexType:
        logging.warning('The or operator is unstable and likely to fail, if used more than twice. Use anyof() instead, for now.')
        try:
            return type(self).either(self, other)
        except AttributeError:
            raise ValueError(f'either is not supported in {type(self).__name__}') from None

        # return self._copy(f'(?:{self._compile(add_flags=False)}|{self._sanitizeInput(other)})', sanatize=False)

    def __ror__(self, other:EZRegexOther) -> EZRegexType:
        return other.__or__(self)

    def __xor__(self, other:EZRegexOther) -> EZRegexType:
        return NotImplementedError

    def __rxor__(self, other:EZRegexOther) -> EZRegexType:
        return NotImplementedError

    def __mod__(self, other:EZRegexOther) -> re.Match|None:
        """ I would prefer __rmod__(), but it doesn't work on strings, since __mod__() is already specified for string formmating. """
        # I don't need to check this, re will do it for me
        # if not isisntance(other, str):
            # raise TypeError(f"Can't search type {type(other)} ")
        return re.search(other, self._compile(add_flags=False))

    def __hash__(self) -> int:
        # TODO: should 2 different dialects who's regexs compile to the same thing have different hashs?
        if len(self._func_list) > 1:
            return hash(self._compile())
        # If we only have 1 function lined up, that means we haven't
        # been called at all. And that means we're one of the basic singletons,
        # because users aren't supposed to instantiate this class directly.
        # THAT means we can use this instance's pointer as a unique identifier.
        else:
            return hash(id(self))

    def __contains__(self, other:str) -> bool:
        # assert isinstance(other, str), "`in` statement can only be used with a string"
        return re.search(self._compile(), other) is not None

    def __rcontains__(self, other:str) -> bool:
        """ I guess this isn't a other? But it really should be. """
        # assert isinstance(other, str), "`in` statement can only be used with a string"
        return re.search(self._compile(), other) is not None

    def __getitem__(self, args:slice|tuple) -> EZRegexType:
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
        try:
            if type(args) is slice:
                # expr[...:end_expr] is equivalent to ZeroOrMore(expr, stop_on=end_expr)
                # assert digit[...:'foo'] == digit[None:'foo'] == digit[,'foo'] ==
                pass
            elif type(args) is not tuple or len(args) == 1:
                if type(args) is tuple:
                    args = args[0]
                if args is None or args is Ellipsis or args == 0:
                    return type(self).at_least_none(self)
                elif args == 1:
                    return type(self).at_least_one(self)
                else:
                    return type(self).match_at_least(args, self)
            else:
                start, end = args
                if start is None or start is Ellipsis:
                    return type(self).match_at_most(end, self)
                elif end is None or end is Ellipsis:
                    if start == 0:
                        return type(self).at_least_none(self)
                    elif start == 1:
                        return type(self).at_least_one(self)
                    else:
                        return type(self).match_at_least(start, self)
                else:
                    return type(self).match_range(start, end, self)
        except AttributeError as e:
            raise ValueError(f'That functionality is not implemented in {type(self).__name__}') from e
        except Exception as e:
            raise ValueError(f'Invalid arguments for __getitem__') from e

    def __str__(self):
        return self._compile()

    def __repr__(self):
        d = {k: v for k, v in self.__dict__.items() if k != "_func_list"}
        return f'{type(self).__name__}({self._compile()}, {d})'

if __name__ == "__main__":
    # Mixins are plain classes (they don't need to inherit from EZRegex)
    class Mixin:
        # The members and methods of the mixin will be added to the subclass (see below)
        mixin_member = 'Mixin member'
        def mixin_method(cur=...):
            # print('mixin method called!')
            return cur + 'Mixin method'

    # Mixins, then EZRegex. EZRegex should be last
    class Subclass(Mixin, EZRegex,
        # escape_chars must be specified
        escape_chars=b'',
        # repl_escape_chars is optional (defaults to b'')
        repl_escape_chars=b'',
        # Variables -- the first one is the default value, the second is the combination function.
        # the 2nd value must be a callable that takes 2 arguments: the left and right values
        next_to_each_other=(False, lambda l, r: l and r),
    ):
        # While defining __init__() is techincally possible, keep in mind that after definition,
        # the class made immutable, so it's not recommended. There's also no real reason to do it.

        # These are what I'm calling "singleton members". They get interpreted by EZRegex._interpret_definition()
        # at define time, and get instantiated as the current type. They can either be a sting, a tuple of
        # (string, dict_of_parameters), or a callable. Lambdas are allowed, they get treated the same as the methods
        subclass_member = 'Subclass member'
        subclass_flags = 'Subclass flags', {'flags': 'i'}
        subclass_flags2 = 'Subclass flags2', {'flags': 'k'}
        subclass_rep = 'Subclass replacement', {'replacement': True}

        # Methods (and member lambdas) must have cur as a keyword parameter with default value of ...
        # cur is the current regex string that's being built. Note that self is *not* a parameter.
        # Just like class members, these get instantiated into singleton members
        def subclass_method(cur=...):
            print('subclass method called with "', cur, '"')
            return cur + 'Subclass method'
            # return 'Subclass method' + cur

        # If you want a method to not be instantiated, and instead just act like a regular method,
        # use @EZRegex.exclude
        # All members will be instantiated, there's not a similar way to exclude them
        @EZRegex.exclude
        def do_normal_thing(self):
            print('normal thing called on', self)

    s = Subclass()
    mixin_member = s.mixin_member
    subclass_member = s.subclass_member
    subclass_flags = s.subclass_flags
    subclass_flags2 = s.subclass_flags2
    subclass_rep = s.subclass_rep
    subclass_method = s.subclass_method
    # s.mixin_method()
    # s.subclass_method()
    # s.mixin_member.mixin_member.mixin_member, s.subclass_member, s.meta_member, s.value

    s.subclass_flags2.subclass_rep.subclass_flags.subclass_method._compile()

