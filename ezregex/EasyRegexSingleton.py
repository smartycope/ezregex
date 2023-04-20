from .EasyRegexMember import EasyRegexMember, _sanitizeInput
from .EasyRegexFunctionCall import EasyRegexFunctionCall
from copy import deepcopy

# These are constant singletons that do not change. When called, they produce EasyRegexMembers.
# This should not be used directly (except when making singletons)
class EasyRegexSingleton:
    def __init__(self, func, pythonFunc=None, perlFunc=None, sanatize=True):
        def parseFuncParam(p):
            if callable(p):
                return p
            elif type(p) is str:
                return lambda cur: cur + p
            elif p is None:
                return None
            else:
                raise TypeError(f"Invalid type {type(p)} passed to EasyRegexSingleton constructor")

        self.func       = parseFuncParam(func)
        self.pythonFunc = parseFuncParam(pythonFunc)
        self.perlFunc   = parseFuncParam(perlFunc)
        self.sanatize   = sanatize

    def __call__(self, *args):
        args = list(args)
        for cnt, i in enumerate(args):
            args[cnt] = _sanitizeInput(i) if self.sanatize else deepcopy(i)
            args[cnt] = _sanitizeInput(i) if self.sanatize else i
        return EasyRegexMember([EasyRegexFunctionCall(self.func, args, self.pythonFunc, self.perlFunc)])
