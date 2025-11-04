import re
import sys

from ezregex import EZRegex

# TODO: make all the flag functions here also accept re.FLAG types (internally they should work the same though)

class PythonEZRegex(EZRegex):
    _escape_chars=b'()[]{}?*+-|^$\\.&~# \t\n\r\v\f'
    _repl_escape_chars=b''
    _compiled = None

    def compile(self, add_flags=True):
        return re.compile(self._compile(add_flags))

    @property
    def compiled(self):
        if self._compiled is None:
            self.__setattr__('_compiled', self.compile(), True)
        return self._compiled

    # Shadowing the re functions
    def search(self, string, pos=0, endpos=sys.maxsize):
        return self.compile().search(string, pos, endpos)

    def match(self, string, pos=0, endpos=sys.maxsize):
        return self.compile().match(string, pos, endpos)

    def fullmatch(self, string, pos=0, endpos=sys.maxsize):
        return self.compile().fullmatch(string, pos, endpos)

    def split(self, string, maxsplit=0):
        return self.compile().split(string, maxsplit)

    def findall(self, string, pos=0, endpos=sys.maxsize):
        return self.compile().findall(string, pos, endpos)

    def finditer(self, string, pos=0, endpos=sys.maxsize):
        return self.compile().finditer(string, pos, endpos)

    def sub(self, repl, string, count=0):
        return self.compile().sub(repl, string, count)

    def subn(self, repl, string, count=0):
        return self.compile().subn(repl, string, count)
