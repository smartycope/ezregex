"""
To tests parts of induvidual regexs that can't be covered by regexs.jsonc tests, things like throwing errors
These tests are not specific to any given dialect
This file gets run by pytest
"""

import pytest
import ezregex.javascript as js
import ezregex.R as r

def test_js_string_anchor_throws_errors():
    assert js.string_starts_with.string_anchor_used is True
    assert js.string_ends_with.string_anchor_used is True
    assert js.digit.string_anchor_used is False
    with pytest.raises(ValueError):
        (js.string_starts_with + js.MULTILINE).str()
    with pytest.raises(ValueError):
        (js.string_ends_with + js.MULTILINE).str()
    with pytest.raises(ValueError):
        (js.string_starts_with + js.line_ends_with).str()
    with pytest.raises(ValueError):
        (js.string_ends_with + js.line_starts_with).str()
    assert js.string_starts_with.str() == '/^/'
    assert js.string_ends_with.str() == '/$/'

# TODO: this test should probably be in test_misc.py instead
def test_js_flags_added_on_outside():
    assert js.digit.str() == r'/\d/'
    assert (js.digit + js.MULTILINE).str() == r'/\d/m'
    assert js.line_starts_with.str() == '/^/m'
    assert js.line_ends_with.str() == '/$/m'
    assert (js.line_ends_with + js.MULTILINE).str() == '/$/m'

def test_r_no_named_groups():
    with pytest.raises(ValueError):
        r.group('test', name='test').str()
    with pytest.raises(ValueError):
        r.group('test', 'test').str()
    with pytest.raises(ValueError):
        r.group('test', '1').str()