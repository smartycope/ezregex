import json
from logging import warning
from sys import version_info

if version_info < (3, 12):
    from typing_extensions import TypedDict
else:
    from typing import TypedDict

from warnings import warn

import jstyleson
from pydantic import TypeAdapter, ValidationError

# from ezregex.api import APIStructure
from ezregex import *
from ezregex import api, python

# from typing_extensions import TypedDict # Required by pydantic for python < 3.12
# import importlib, sys

# def import_stub(stubs_path, module_name):
#     sys.path_hooks.insert(0,
#         importlib.machinery.FileFinder.path_hook(
#             (importlib.machinery.SourceFileLoader, ['.pyi']))
#     )
#     sys.path.insert(0, stubs_path)

#     try:
#         return importlib.import_module(module_name)
#     finally:
#         sys.path.pop(0)
#         sys.path_hooks.pop(0)


# import importlib.util
# import sys

# file = "/home/anastasia/hello/python/ezregex/ezregex/api.pyi"
# sys.path_hooks.insert(0,
#     importlib.machinery.FileFinder.path_hook(
#         (importlib.machinery.SourceFileLoader, ['.pyi']))
# )
# sys.path.insert(0, file)
# spec = importlib.util.spec_from_file_location("module.name", file)
# api = importlib.util.module_from_spec(spec)
# sys.modules["module.name"] = api
# spec.loader.exec_module(api)
# print(api)

# def import_stub(stub_path, module_name):
#     spec = importlib.util.spec_from_file_location(module_name, stub_path)
#     module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(module)
#     return module

# import_stub("/home/anastasia/hello/python/ezregex/ezregex/api.pyi", 'api')

# print(api_types)


# This is just copied from api.pyi, because I'm tired of trying to figure out how to import .pyi files for the moment
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
        'split': list[str|None] | None,
    }
)

# TODO: test that a pattern like <span> does not break things
def test_correct_output():
    with open('data/regexs.jsonc') as f:
        regexs = jstyleson.load(f)

    for i in regexs:
        regex_str = i['re']
        match = i['should']
        dontmatch = i['shouldnt']
        if 'worksIn' in i and 'py' not in i['worksIn']:
            continue
        if 'doesntWorkIn' in i and 'py' in i['doesntWorkIn']:
            continue

        try:
            regex = eval(regex_str, python.__dict__)
        except Exception as err:
            raise AssertionError(f"Failed to parse pattern `{regex_str}`") from err
        try:
            resp = api(regex)
        except NotImplementedError as err:
            warning(err)
        except Exception as err:
            raise AssertionError(f"Failed on pattern `{regex_str}` -> `{regex}`") from err
        try:
            TypeAdapter(APIStructure).validate_python(resp)
        except ValidationError as err:
            raise AssertionError(f"Invalid schema from {regex_str}:\n{json.dumps(resp, indent=4)}\n{'-'*20}\nErrors:\n{err.errors()}\n{'-'*20}\n") from err
