import re
from typing import Callable
from mypy_extensions import DefaultNamedArg, VarArg
from .base.interface import InputType

class EZRegex:
    """ Represent parts of the Regex syntax. Should not be instantiated by the user directly."""

    def __init__(self,
            definition:str|"EZRegex"|Callable[[VarArg, DefaultNamedArg[str, "cur"]], str],
            dialect: str,
            sanatize:bool=True,
            init:bool=True,
            replacement:bool=False,
            flags:str='',
        ) -> None:
        """
        The workhorse of the EZRegex library. This represents a regex pattern that can be combined
        with other EZRegexs and strings. Ideally, this should only be called internally, but it should
        still work from the user's end
        """

    # Private functions
    def _escape(self, pattern:str) -> str:
        """ This function was modified from the one in /usr/lib64/python3.12/re/__init__.py line 255 """
    def _sanitizeInput(self, i:InputType, addFlags:bool=False) -> str:
        """ Instead of rasising an error if passed a strange datatype, it now trys to cast it to a string """
    def _compile(self, addFlags=True) -> str: ...

    # Regular functions
    def compile(self, addFlags=True) -> re.Pattern: ...
    def str(self) -> str: ...
    def debug(self) -> EZRegex: ...
    def copy(self, addFlags=True) -> None: ...
    def test(self, testString:str=None, show=True, context=True) -> bool:
        """ Tests the current regex expression to see if it's in @param testString.
            Returns the match objects (None if there was no match)
        """
    def invert(self, amt=1, **kwargs) -> str: ...
    def inverse(self, amt=1, **kwargs) -> str:
        """ "Inverts" the current Regex expression to give an example of a string it would match.
            Useful for debugging purposes. """

    # Magic Functions
    def __call__(self, *args, **kwargs) -> EZRegex | str:
        """ This should be called by the user to specify the specific parameters of this instance i.e. anyof('a', 'b') """
    def __str__(self, addFlags:bool=True) -> str: ...
    def __repr__(self) -> str: ...
    def __eq__(self, thing:InputType) -> bool: ...
    def __mul__(self, amt:int) -> EZRegex: ...
    def __rmul__(self, amt:int) -> EZRegex: ...
    def __imul__(self, amt:int) -> EZRegex: ...
    def __add__(self, thing:InputType) -> EZRegex: ...
    def __radd__(self, thing:InputType) -> EZRegex: ...
    def __iadd__(self, thing:InputType) -> EZRegex: ...
    def __and__(self, thing:InputType) -> EZRegex: ...
    def __rand__(self, thing:InputType) -> EZRegex: ...
    # The shift operators just shadow the add operators
    def __lshift__(self, thing:InputType) -> EZRegex: ...
    def __rlshift__(self, thing:InputType) -> EZRegex: ...
    def __ilshift__(self, thing:InputType) -> EZRegex: ...
    # I don't think right and left shifts should be any different, right?
    def __rshift__(self, thing:InputType) -> EZRegex: ...
    def __rrshift__(self, thing:InputType) -> EZRegex: ...
    def __irshift__(self, thing:InputType) -> EZRegex: ...
    def __invert__(self) -> str: ...
    def __pos__(self) -> EZRegex:
        """ TODO: Add documentation here """
    def __ror__(self, thing:InputType) -> EZRegex:
        """ TODO: Add documentation here """
    def __or__(self, thing:InputType) -> EZRegex: ...
    def __xor__(self, thing:InputType) -> EZRegex: ...
    def __rxor__(self, thing:InputType) -> EZRegex: ...
    def __mod__(self, other:str) -> re.Match|None:
        """ I would prefer __rmod__(), but it doesn't work on strings, since __mod__() is already specified for string formmating. """
    def __hash__(self) -> int: ...
    def __contains__(self, thing:str) -> bool: ...
    def __getitem__(self, args) -> EZRegex: ...
    def __reversed__(self) -> str: ...
    def __rich__(self) -> str: ...
    def __pretty__(self) -> str: ...
    # To make EZRegex instances immutable
    def __setattr__(self, name:str, value, ignore=False): ...
    def __delattr__(self, *args): ...
