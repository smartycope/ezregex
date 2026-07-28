from typing import Any, TypedDict

from ezregex.EZRegex import EZRegex

Group = TypedDict(
    'Group',
    {
        'string': str,
        'end': int,
        'start': int,
        'color': str
    }
)

Match = TypedDict(
    'Match',
    {
        'string': str,
        'parts': list[list[str|None]],
        'end': int,
        'start': int,
        'color': str
    }
)

Matches = TypedDict(
    'Matches',
    {
        'match': Match,
        'unnamed groups': dict[int, Group],
        'named groups': dict[str, Group],
    }
)
APIStructure = TypedDict(
    "APIStructure",
    {
        'regex': str,
        'string': str,
        'parts': list[list[str|None]],
        'matches': list[Matches],
        'replaced': str | None,
        'split': list[str | None] | None,
    }
)

def api(
    pattern:EZRegex,
    replacement_pattern:EZRegex|str|None=None,
    test_string:str|None=None, *,
    replacement_count:int=0,
    split_count:int=0,
    background_color:str='#FFFFFF',
    readability_distinctness_ratio:float=4.5
) -> APIStructure: ...

class _ParameterDescription(TypedDict):
    name: str
    python_name: str
    kind: str
    required: bool
    default: Any
    variadic: bool
    keyword_only: bool

class _ElementDescription(TypedDict):
    name: str
    aliases: list[str]
    documentation: str
    origin: str
    replacement: bool | None
    parameters: list[_ParameterDescription]

class _FlagDescription(TypedDict):
    name: str
    value: str
    documentation: str

class _FunctionDescription(TypedDict):
    name: str
    aliases: list[str]
    documentation: str
    parameters: list[_ParameterDescription]

class _Capabilities(TypedDict):
    greedy: bool
    possessive: bool

class _DialectDescription(TypedDict):
    id: str
    label: str
    class_name: str
    documentation_url: str
    testing: str
    capabilities: _Capabilities
    flags: list[_FlagDescription]
    elements: list[_ElementDescription]
    functions: list[_FunctionDescription]

class _DialectCatalog(TypedDict):
    schema_version: int
    ezregex_version: str
    dialects: list[_DialectDescription]

def _describe_dialects() -> _DialectCatalog: ...
