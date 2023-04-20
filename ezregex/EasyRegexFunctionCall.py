from .RegexDialect import RegexDialect

# This is a helper class that just holds the args and function so we can call them last
class EasyRegexFunctionCall:
    def __init__(self, genericFunc, args=(), pythonFunc=None, perlFunc=None):
        self.genericFunc  = genericFunc
        self.pythonFunc   = pythonFunc if pythonFunc else self.genericFunc
        self.perlFunc     = perlFunc   if perlFunc   else self.genericFunc

        self.args = args

    def __call__(self, cur, dialect=RegexDialect.GENERIC):
        if dialect == RegexDialect.GENERIC:
            return self.genericFunc(cur, *self.args)
        if dialect == RegexDialect.PYTHON:
            return self.pythonFunc(cur, *self.args)
        if dialect == RegexDialect.PERL:
            return self.perlFunc(cur, *self.args)
