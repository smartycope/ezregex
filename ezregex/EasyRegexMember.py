from .EasyRegexFunctionCall import EasyRegexFunctionCall
from .RegexDialect import RegexDialect
import re
from copy import deepcopy
from typing import List

escapeChars = (r'\)', r'\(', r'\[', r'\]', r'\{', r'\}', r'\+', r'\*', r'\$', r'\@', r'\^', r'\:', r'\=', r'\-', r'\/', r'\?', r'\|', r'\,')  #, r'\\')

# For tests
def printColor(s, color=(0, 0, 0), curColor=(204, 204, 204), **kwargs):
    r, g, b = color
    curr, curg, curb = curColor
    print(f'\033[38;2;{r};{g};{b}m', end='')
    print(s, **kwargs)
    print(f'\033[38;2;{curr};{curg};{curb}m', end='')


def _sanitizeInput(i):
    """ Instead of rasising an error if passed a strange datatype, it now trys to cast it to a string """
    # r'\<', r'\>', r'//'
    i = deepcopy(i)

    # If it's another chain, compile it
    if type(i) is EasyRegexMember:
        return str(i)
    elif isinstance(i, str):
        for part in escapeChars:
            i = re.sub(r'(?<!\\)' + part, part, deepcopy(i))
        return deepcopy(i)
    else:
        try:
            return str(i)
        except:
            raise TypeError(f'Incorrect type {type(i)} given to EasyRegex parameter: Must be string or another EasyRegex chain.')

# These are mutable parts of the Regex statement, produced by EasyRegexElements. Should not be used directly.
class EasyRegexMember:
    def __init__(self, funcs:List[EasyRegexFunctionCall]):
        self.funcList = funcs
        self.dialect = RegexDialect.GENERIC

    # Magic Functions
    def __str__(self):
        return self._compile()

    def __repr__(self):
        return 'EasyRegex("' + self.__str__() + '")'

    def __eq__(self, thing):
        return _sanitizeInput(thing) == self._compile()

    def __add__(self, thing):
        # new = deepcopy(self)
        # new.funcList.append(EasyRegexFunctionCall(lambda cur: cur + _sanitizeInput(thing)))
        # Because we don't want to edit the current instance, it might be a variable they use later.
        # return new
        # TODO This doesn't include dialects
        return EasyRegexMember(self.funcList + [EasyRegexFunctionCall(lambda cur: cur + _sanitizeInput(thing))])

    def __radd__(self, thing):
        # new = deepcopy(self)
        # TODO This doesn't include dialects
        # EasyRegexMember([EasyRegexFunctionCall(lambda cur: _sanitizeInput(thing) + cur)] + self.funcList)
        # new.funcList.insert(0, EasyRegexFunctionCall(lambda cur: _sanitizeInput(thing) + cur))
        # Because we don't want to edit the current instance, it might be a variable they use later.
        return EasyRegexMember([EasyRegexFunctionCall(lambda cur: _sanitizeInput(thing) + cur)] + self.funcList)

    def __iadd__(self, thing):
        return self + _sanitizeInput(thing)

    # The shift operators just shadow the add operators
    def __lshift__(self, thing):
        return __add__(thing)

    def __rlshift__(self, thing):
        return __radd__(thing)

    def __ilshift__(self, thing):
        return __iadd__(thing)

    def __not__(self):
        NotImplementedError('The not operator is not currently implemented')

    # Regular functions
    def _compile(self):
        regex = r''
        for func in self.funcList:
            regex = func(regex, self.dialect)
        return regex

    def compile(self):
        return re.compile(self._compile())

    def str(self):
        return self.__str__()

    def debug(self):
        try:
            from Cope import debug
        except ImportError:
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
            print('please install the clipboard module in order to copy EasyRegex Expressions (i.e. pip install clipboard)')
        else:
            copy(str(self))

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

    def inverse(self):
        """ "Inverts" the current Regex expression to give an example of a string it would match.
            Useful for debugging purposes.
        """
        return invert(self._compile(True))

    def invert(self):
        """ Alias of inverse
        """
        return self.inverse()

    def invertTest(self, count=10, colors=True, groupNames=False, explicitConditionals=False):
        """ Invert the regex a number of times """
        prettyInvert(self._compile(True), count, colors, groupNames, explicitConditionals)

    # Dialect Setters
    def usePythonDialect(self):
        self.dialect = RegexDialect.PYTHON

    def useGenericDialect(self):
        self.dialect = RegexDialect.GENERIC

    def usePerlDialect(self):
        self.dialect = RegexDialect.PERL

    def setDialect(self, dialect:RegexDialect):
        self.dialect = dialect
