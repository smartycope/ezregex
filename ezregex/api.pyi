from typing import TypedDict

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
        'string HTML': str,
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
        'string HTML': str,
        'parts': list[list[str|None]],
        'matches': list[Matches],
        'replaced': str | None,
        'split': list[str] | None,
    }
)

def api(
    pattern:EZRegex,
    replacement_pattern:EZRegex|str|None=None,
    test_string:str|None=None, *,
    replacement_count:int=0,
    split_count:int=0
) -> APIStructure: ...
