from typing import Any, Callable, Tuple, Dict, Unpack, List, Set
from types import FunctionType

try:
    from mypy_extensions import DefaultNamedArg, VarArg
    type EZRegexFunc = Callable[[VarArg, DefaultNamedArg("cur", str)], str]
except ImportError:
    type EZRegexFunc = Callable[[..., str], str]

type EZRegexType = 'EZRegex'
type EZRegexDefinition = str|EZRegexFunc|Tuple[str|EZRegexFunc, Dict[str, Any]]
type EZRegexOther = str|EZRegexType|int
type EZRegexParam = str|EZRegexType|int|bool|None
