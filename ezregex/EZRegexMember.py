from .EZRegexFunctionCall import EZRegexFunctionCall
from .invert import invertRegex
import re
from copy import deepcopy
from typing import List
from warnings import warn
from ._escapeChars import escapeChars

# For tests
def printColor(s, color=(0, 0, 0), curColor=(204, 204, 204), **kwargs):
    r, g, b = color
    curr, curg, curb = curColor
    print(f'\033[38;2;{r};{g};{b}m', end='')
    print(s, **kwargs)
    print(f'\033[38;2;{curr};{curg};{curb}m', end='')


def _sanitizeInput(i):
    """ Instead of rasising an error if passed a strange datatype, it now trys to cast it to a string """
    i = deepcopy(i)

    # If it's another chain, compile it
    if isinstance(i, EZRegexMember):
        return i._compile()
    # It's a string (so we need to escape it)
    elif isinstance(i, str):
        for part in escapeChars:
            i = re.sub(r'(?<!\\)' + part, part, i)
        return i
    # It's something we don't know, but try to cast it to a string anyway
    else:
        try:
            s = str(i)
            msg = f"Type {type(i)} passed to EZRegexMember, auto-casting to a string. Special characters will will not be escaped."
            try:
                from Cope import debug
                debug(msg, trace=True, color=ERROR)
            except:
                warn(msg)
            return s
        except:
            raise TypeError(f'Incorrect type {type(i)} given to EZRegexMember parameter: Must be string or another EZRegexMember chain.')

# These are mutable parts of the Regex statement, produced by EasyRegexElements. Should not be used directly.
class EZRegexMember:
    def __init__(self, funcs:List[EZRegexFunctionCall], sanatize=True, init=True):
        """ This should only be called internally """
        # Parse params
        if type(funcs) is not list:
            funcs = [funcs]
        self.sanatize = sanatize
        self.funcList = funcs
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

    def __call__(self, *args):
        """ This should be called by the user to specify the specific parameters of this instance
            i.e. anyof('a', 'b')
        """
        # If this is being called without parameters, just compile the chain.
        # If it's being called *with* parameters, then it better be a fundemental member, otherwise
        # that doesn't make any sense.
        if len(self.funcList) > 1:
            if not len(args):
                return self._compile()
            else:
                raise TypeError("You're trying to pass parameters to a chain of expressions. That doesn't make any sense. Stop that.")

        args = list(args)
        for cnt, i in enumerate(args):
            args[cnt] = _sanitizeInput(i) if self.sanatize else deepcopy(i)
            # args[cnt] = _sanitizeInput(i) if self.sanatize else i
        return EZRegexMember([EZRegexFunctionCall(self.funcList[0], args)], init=False)

    # Magic Functions
    def __str__(self):
        return self._compile()

    def __repr__(self):
        return 'ezregex("' + self._compile() + '")'

    def __eq__(self, thing):
        return _sanitizeInput(thing) == self._compile()

    def __add__(self, thing):
        return EZRegexMember(self.funcList + [EZRegexFunctionCall(lambda cur: cur + _sanitizeInput(thing))], init=False)

    def __radd__(self, thing):
        return EZRegexMember([EZRegexFunctionCall(lambda cur: _sanitizeInput(thing) + cur)] + self.funcList, init=False)

    def __iadd__(self, thing):
        return self + _sanitizeInput(thing)

    # The shift operators just shadow the add operators
    def __lshift__(self, thing):
        return self.__add__(thing)

    def __rlshift__(self, thing):
        return self.__radd__(thing)

    def __ilshift__(self, thing):
        return self.__iadd__(thing)

    def __not__(self):
        NotImplementedError('The not operator is not currently implemented')

    # Regular functions
    def _compile(self):
        regex = r''
        for func in self.funcList:
            regex = func(regex)
        return regex

    def compile(self):
        return re.compile(self._compile())

    def str(self):
        return self.__str__()

    def debug(self):
        try:
            from Cope import debug
        except ModuleNotFoundError:
            print(f"Compiled EasyRegex String = {self}")
        else:
            debug(self, name='Compiled EasyRegex String', calls=2)
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

    def test(self, testString) -> (re.Match, None):
        """ Tests the current regex expression to see if it's in @param testString.
            Returns the match objects (None if there was no match)
        """
        try:
            from Cope import printContext
            _cope = True
        except ImportError:
            _cope = False

        red = (220, 0, 0)
        green = (34, 179, 99)
        subtle = (128, 64, 64)
        results = (255, 190, 70)

        printColor('-' * 30, red)
        if _cope:
            printContext(calls=2, color=subtle)
            print()
        print("Testing regex expression:")
        printColor(self._compile(), green)
        print("for matches in:")
        printColor(str(testString), green)
        match = re.search(self._compile(), testString)
        printColor('Result: ', results, end='')
        if match:
            printColor('Found', green)
            # if len(match.groups()):
            printColor(f'Match = "{match.group()}"',              subtle)
            printColor(f'Named Groups   = {match.groupdict()}', subtle)
            printColor(f'Unnamed Groups = {match.groups()}',    subtle)
            # else:
            printColor(f'Span = {match.span()} ', subtle)
        else:
            printColor('Not Found', red)
        printColor('-' * 30, red)

        return match

    def inverse(self, **kwargs):
        """ "Inverts" the current Regex expression to give an example of a string it would match.
            Useful for debugging purposes.
        """
        return invertRegex(self._compile(), **kwargs)

    def invertTest(self, count=10, colors=True, groupNames=False, explicitConditionals=False):
        """ Invert the regex a number of times """
        prettyInvert(self._compile(True), count, colors, groupNames, explicitConditionals)
