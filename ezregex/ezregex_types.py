from typing import Any, Callable, Tuple, Dict

try:
    from mypy_extensions import DefaultNamedArg, VarArg
    EZRegexFunc = Callable[[VarArg, DefaultNamedArg("cur", str)], str]
except ImportError:
    EZRegexFunc = Callable[[..., str], str]

# Lazily evaluated types have only been added in 3.14+. Until then, this works
EZRegexType = Any
EZRegexDefinition = str|EZRegexFunc|Tuple[str|EZRegexFunc, Dict[str, Any]]
EZRegexOther = str|EZRegexType|int
EZRegexParam = str|EZRegexType|int|bool|None
