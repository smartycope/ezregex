import re

from ezregex.invert import *
from ezregex import python
from ezregex import *

import jstyleson


def test_replacement():
    offset = 2
    with open('tests/replacements.jsonc') as f:
        replacements = jstyleson.load(f)

    for pattern, repl, s, ans in replacements:
        pattern = eval(pattern, python.__dict__)
        assert re.sub(str(pattern), str(repl), s) == ans, \
            f'Replacing\n\t{pattern}\nwith\n\t{repl}\nin\n\t{s}\nyielded\n\t{re.sub(str(pattern), str(repl), s)}\nnot\n\t{ans}'

def test_replace_func():
    assert replace('|{g}|{1}|{0}|') == '|' + rgroup('g') + '|' + rgroup(1) + '|' + replace_entire + '|'
    assert replace("{group}this is am{group}mtest") == rgroup('group') + 'this is am' + rgroup('group') + "mtest"
    assert replace("this is {{ not a thing") == "this is { not a thing"
    assert replace("also not }} a thing") == "also not } a thing"
    assert replace("still }}not{{ a thing") == "still }not{ a thing"
    assert replace("also {{not}} a thing") == "also {not} a thing"
    assert replace("but {group} is and {1} is") == "but " + rgroup('group') + " is and " + rgroup(1) + " is"
    assert replace("{group}{g}") == rgroup('group') + rgroup('g')
