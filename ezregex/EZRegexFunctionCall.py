# This is a helper class that just holds the args and function so we can call them last
class EZRegexFunctionCall:
    def __init__(self, func, args=(), kwargs={}):
        self.func  = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, cur):
        return self.func(cur, *self.args, **self.kwargs)
