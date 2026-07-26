import json
from logging import warning
from sys import version_info
from types import ModuleType

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
from ezregex.api import _describe_dialects
from ezregex.EZRegex import EZRegex

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
        # match = i['should']
        # dontmatch = i['shouldnt']
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
            try:
                raise AssertionError(f"Failed on pattern `{regex_str}` -> `{regex}`") from err
            except Exception as err:
                raise AssertionError(f"Failed to compile pattern `{regex_str}`") from err
        try:
            TypeAdapter(APIStructure).validate_python(resp)
        except ValidationError as err:
            raise AssertionError(f"Invalid schema from {regex_str}:\n{json.dumps(resp, indent=4)}\n{'-'*20}\nErrors:\n{err.errors()}\n{'-'*20}\n") from err


def test_api_escapes_legacy_html():
    response = api(python.literal('<span>'), test_string='<span>')
    assert '<span>' not in response['string HTML']
    assert '&lt;span&gt;' in response['string HTML']
    assert any(part[-1] == '<span>' for part in response['parts'])


def test_frontend_dialect_catalog():
    catalog = _describe_dialects()
    assert catalog['schema_version'] == 1
    assert catalog['ezregex_version'] == '3.1.3'
    assert [dialect['id'] for dialect in catalog['dialects']] == [
        'python', 'javascript', 'r', 'pcre2'
    ]

    python_dialect = catalog['dialects'][0]
    names = {element['name'] for element in python_dialect['elements']}
    assert {'literal', 'group', 'match_range', 'rgroup'} <= names
    assert 'or' not in names
    assert 'one_of' not in names
    assert python_dialect['testing'] == 'python'
    assert python_dialect['capabilities'] == {
        'greedy': True,
        'possessive': True,
    }

    any_of = next(
        element for element in python_dialect['elements']
        if element['name'] == 'any_of'
    )
    assert {'anyOf', 'anyof', 'one_of', 'oneOf', 'oneof'} <= set(any_of['aliases'])
    assert any_of['parameters'][0]['kind'] == 'variadic_pattern'
    replace = next(
        function for function in python_dialect['functions']
        if function['name'] == 'replace'
    )
    assert [parameter['name'] for parameter in replace['parameters']] == [
        'string', 'compile'
    ]
    assert replace['parameters'][1]['kind'] == 'boolean'

    all_parameter_kinds = {
        parameter['kind']
        for dialect in catalog['dialects']
        for element in dialect['elements']
        for parameter in element['parameters']
    }
    assert 'python_expression' not in all_parameter_kinds


def test_catalog_discovers_an_imported_dialect_and_element(monkeypatch):
    import ezregex

    class SyntheticEZRegex(EZRegex, escape_chars=b'', flags={}):
        novel_element = 'synthetic'

    module = ModuleType('ezregex.synthetic')
    SyntheticEZRegex.__module__ = module.__name__
    module.SyntheticEZRegex = SyntheticEZRegex
    monkeypatch.setattr(ezregex, 'synthetic', module, raising=False)

    synthetic = next(
        dialect for dialect in _describe_dialects()['dialects']
        if dialect['id'] == 'synthetic'
    )
    assert synthetic['testing'] == 'compile'
    assert [element['name'] for element in synthetic['elements']] == [
        'novel_element'
    ]
