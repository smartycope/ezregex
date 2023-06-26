from .EZRegexFunctionCall import EZRegexFunctionCall
from .invert import invertRegex
import re
from copy import deepcopy
from typing import List
from warnings import warn
from ._escapeChars import escapeChars
from rich import print as rprint
from rich.text import Text
from rich.panel import Panel
from re import RegexFlag

from Cope import debug
from Cope.colors import distinctColor

# These are mutable parts of the Regex statement, produced by EasyRegexElements. Should not be used directly.
class EZRegexMember:
    def __init__(self, funcs:List[EZRegexFunctionCall], sanatize=True, init=True, replacement=False, flags=RegexFlag.NOFLAG):
        """ Ideally, this should only be called internally, but it should still
            work from the user's end
        """
        self.flags = flags

        # Parse params
        # Add flags if it's another EZRegexMember
        if isinstance(funcs, EZRegexMember):
            self.flags = funcs.flags

        if isinstance(funcs, (str, EZRegexMember)):
            funcs = [str(funcs)]
        elif not isinstance(funcs, (list, tuple)):
            funcs = [funcs]

        self.sanatize = sanatize
        self.replacement = replacement
        # if replacement:
        #     self.sanatize = False
        self.funcList = list(funcs)
        self.example = self.invert = self.inverse


        # The init parameter is not actually required, but it will make it more efficient,
        # so we don't have to check that the whole chain is callable
        if init:
            # Go through the chain (most likely of length 1) and parse any strings
            # This is for simplicity when defining all the members
            for i in range(len(self.funcList)):
                if isinstance(self.funcList[i], str):
                    # I *hate* how Python handles lambdas
                    stringBecauseHatred = deepcopy(self.funcList[i])
                    self.funcList[i] = lambda cur: cur + stringBecauseHatred
                elif not callable(self.funcList[i]) and self.funcList[i] is not None:
                    raise TypeError(f"Invalid type {type(self.funcList[i])} passed to EZRegexMember constructor")

    def _sanitizeInput(self, i):
        """ Instead of rasising an error if passed a strange datatype, it now trys to cast it to a string """
        i = deepcopy(i)

        # Don't sanatize anything if this is a replacement string
        if self.replacement:
            return str(i)

        # If it's another chain, compile it
        if isinstance(i, EZRegexMember):
            self.flags |= i.flags
            return i._compile(addFlags=False)
        # It's a string (so we need to escape it)
        elif isinstance(i, str):
            for part in escapeChars:
                i = re.sub(r'(?<!\\)' + part, part, i)
            return i
        # A couple of singletons use bools and None as kwargs, just ignore them and move on
        elif i is None or isinstance(i, bool):
            return i
        # A couple singletons use ints as input, just cast it to a string and don't throw a warning
        elif isinstance(i, int):
            return str(i)
        # It's something we don't know, but try to cast it to a string anyway
        else:
            try:
                s = str(i)
                msg = f"Type {type(i)} passed to EZRegexMember, auto-casting to a string. Special characters will will not be escaped."
                try:
                    from Cope import debug
                except:
                    warn(msg)
                else:
                    # debug(msg, trace=True, color=-1, calls=3)
                    # debug(i)
                    debug(msg, color=-1, calls=3)
                return s
            except:
                raise TypeError(f'Incorrect type {type(i)} given to EZRegexMember parameter: Must be string or another EZRegexMember chain.')

    def __call__(self, *args, **kwargs):
        """ This should be called by the user to specify the specific parameters of this instance
            i.e. anyof('a', 'b')
        """
        # If this is being called without parameters, just compile the chain.
        # If it's being called *with* parameters, then it better be a fundemental member, otherwise
        # that doesn't make any sense.
        if len(self.funcList) > 1:
            if not len(args) and not len(kwargs):
                return self._compile()
            else:
                raise TypeError("You're trying to pass parameters to a chain of expressions. That doesn't make any sense. Stop that.")

        # Sanatize the arguments
        args = list(map(self._sanitizeInput if self.sanatize else deepcopy, args))
        # args = list(args)
        # for cnt, i in enumerate(args):
        #     args[cnt] = self._sanitizeInput(i) if self.sanatize else deepcopy(i)
        _kwargs = {}
        for key, val in kwargs.items():
            _kwargs[key] = self._sanitizeInput(val) if self.sanatize else deepcopy(val)

        return EZRegexMember([EZRegexFunctionCall(self.funcList[0], args, _kwargs)], init=False, sanatize=self.sanatize, replacement=self.replacement, flags=self.flags)

    # Magic Functions
    def __str__(self):
        return self._compile()

    def __repr__(self):
        return 'ezregex("' + self._compile() + '")'

    def __eq__(self, thing):
        return self._sanitizeInput(thing) == self._compile()

    def __mul__(self, amt):
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
        return EZRegexMember(self.funcList + [EZRegexFunctionCall(lambda cur: cur + self._sanitizeInput(thing))],
            init=False,
            sanatize=self.sanatize or thing.sanatize if isinstance(thing, EZRegexMember) else self.sanatize,
            replacement=self.replacement or thing.replacement if isinstance(thing, EZRegexMember) else self.replacement,
            flags=self.flags | thing.flags if isinstance(thing, EZRegexMember) else self.flags
        )

    def __radd__(self, thing):
        return EZRegexMember([EZRegexFunctionCall(lambda cur: self._sanitizeInput(thing) + cur)] + self.funcList,
            init=False,
            sanatize=self.sanatize or thing.sanatize if isinstance(thing, EZRegexMember) else self.sanatize,
            replacement=self.replacement or thing.replacement if isinstance(thing, EZRegexMember) else self.replacement,
            flags=self.flags | thing.flags if isinstance(thing, EZRegexMember) else self.flags
        )

    def __iadd__(self, thing):
        # return self + self._sanitizeInput(thing)
        return self + thing

    # The shift operators just shadow the add operators
    def __lshift__(self, thing):
        return self.__add__(thing)

    def __rlshift__(self, thing):
        return self.__radd__(thing)

    def __ilshift__(self, thing):
        return self.__iadd__(thing)

    def __not__(self):
        # NotImplementedError('The not operator is not currently implemented')
        return self.invert(colors=False, groupNames=False)

    def __hash__(self):
        return hash(self._compile())

    def __contains__(self, thing):
        assert isinstance(thing, str), "`in` statement can only be used with a string"
        # print(self.compile())
        return re.search(self._compile(), thing) is not None

    # I guess this isn't a thing? But it really should be.
    def __rcontains__(self, thing):
        assert isinstance(thing, str), "`in` statement can only be used with a string"
        # print(self.compile())
        return re.search(self._compile(), thing) is not None

    def __reversed__(self):
        return self.inverse()

    def __rich__(self):
        return self._compile()

    # Regular functions
    def _compile(self, addFlags=True):
        regex = ''
        for func in self.funcList:
            regex = func(regex)

        # Add the flags
        _flags = ''
        if addFlags:
            if self.flags & RegexFlag.ASCII:
                _flags += 'a'
            if self.flags & RegexFlag.DEBUG:
                pass
            if self.flags & RegexFlag.DOTALL:
                _flags += 's'
            if self.flags & RegexFlag.IGNORECASE:
                _flags += 'i'
            if self.flags & RegexFlag.LOCALE:
                _flags += 'L'
            if self.flags & RegexFlag.MULTILINE:
                _flags += 'm'
            if self.flags & RegexFlag.TEMPLATE:
                pass
            if self.flags & RegexFlag.UNICODE:
                _flags += 'u'
            if self.flags & RegexFlag.VERBOSE:
                _flags += 'x'
            if len(_flags):
                regex = fr'(?{_flags})' + regex
        return regex

    def compile(self):
        return re.compile(self._compile())

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

    def copy(self):
        try:
            from clipboard import copy
        except ImportError:
            print('Please install the clipboard module in order to auto copy ezregex expressions (i.e. pip install clipboard)')
        else:
            copy(self._compile())

    def test(self, testString, show=True) -> (re.Match, None):
        """ Tests the current regex expression to see if it's in @param testString.
            Returns the match objects (None if there was no match)
        """
        match = re.search(self._compile(), testString)
        if not show:
            return match

        try:
            from Cope import get_context, get_metadata
        except ImportError:
            _cope = False
        else:
            _cope = True

        s = Text()
        defaultColor = 'bold'
        textColor = ''

        s.append("Testing expression", style=defaultColor)
        if _cope:
            s.append(f' (from {get_context(get_metadata(2)).strip()})', style=defaultColor)
        s.append(':\n', style=defaultColor)
        s.append(f'\t{self._compile()}\n', style=textColor)

        s.append("for matches in:\n\t", style=defaultColor)
        if match:
            allGroups = {match.span(i+1) for i in range(len(match.groups()))}
            namedGroups = dict({(i, match.span(i)) for i in match.groupdict().keys()})
            unnamedGroups = allGroups - set(namedGroups.values())
            # + 2, just so we can get different starting colors other than black and red
            colors = dict(zip(allGroups, map(lambda a: a+2, range(len(allGroups)))))

            cursor = 0
            for g in sorted(allGroups, key=lambda x: x[0]):
                s.append(testString[cursor:g[0]], style=textColor)
                s.append(testString[g[0]:g[1]], style=f'white on color({colors[g]})')
                cursor = g[1]
            s.append(testString[cursor:], style=textColor)
        else:
            s.append(testString, style='green')
        s.append('\n\n')

        # s.append('Result: ', style=defaultColor)
        if match:
            toSlice = lambda t: f'({t[0]}:{t[1]})'
            # s.append('Found\n', style='blue')
            s.append('Match = ', style='italic grey37')
            s.append(f'"{match.group()}"', style='grey37')
            s.append(f' {toSlice(match.span())}\n', style='italic grey37')

            s.append('Unnamed Groups:\n', style='italic grey37')
            for i in range(len(unnamedGroups)):
                clr = f'color({colors[match.span(i+1)]})'
                s.append(f'\t{i+1}: "{match.group(i+1)}"', style=clr)
                s.append(f' {toSlice(match.span(i+1))}\n', style='italic ' + clr)

            s.append('Named Groups:\n', style='italic grey37')
            for name, span in namedGroups.items():
                clr = f'color({colors[span]})'
                s.append(f'\t{name}: "{match.group(name)}"', style=clr)
                s.append(f' {toSlice(span)}\n', style='italic ' + clr)


            # s.append(str(match.groups()), style='grey37')
            # s.append('\n\tNamed Groups   = ', style='italic grey37')
            # s.append(str(match.groupdict()), style='grey37')
            # s.append('\n\tSpan = ', style='italic grey37')
            # s.append(str(match.span()), style='grey37')
        else:
            s.append('Not Found', style='red')

        t = Text.assemble(*s)
        p = Panel(t, title='Testing Regex', subtitle=Text('Found\n', style='blue') if match else Text('Not Found\n', style='red'))  #, border_style='dim green')
        rprint(p)

        return match

    def inverse(self, amt=1, **kwargs):
        """ "Inverts" the current Regex expression to give an example of a string it would match.
            Useful for debugging purposes.
        """
        return '\n'.join([invertRegex(self._compile(), **kwargs) for _ in range(amt)])
