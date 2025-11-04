import re

import jstyleson

from ezregex import *
from ezregex import python


def test_replace_func():
    assert replace('|{g}|{1}|{0}|') == '|' + rgroup('g') + '|' + rgroup(1) + '|' + replace_entire + '|'
    assert replace("{group}this is am{group}mtest") == rgroup('group') + 'this is am' + rgroup('group') + "mtest"
    assert replace("this is {{ not a thing") == "this is { not a thing"
    assert replace("also not }} a thing") == "also not } a thing"
    assert replace("still }}not{{ a thing") == "still }not{ a thing"
    assert replace("also {{not}} a thing") == "also {not} a thing"
    assert replace("but {group} is and {1} is") == "but " + rgroup('group') + " is and " + rgroup(1) + " is"
    assert replace("{group}{g}") == rgroup('group') + rgroup('g')
