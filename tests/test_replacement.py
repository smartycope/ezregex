import re

import jstyleson

from ezregex import *
from ezregex import python


def test_replace_func():
    assert replace('|{g}|{1}|{0}|') == ('|' + rgroup('g') + '|' + rgroup(1) + '|' + replace_entire + '|').str()
    assert replace("{group}this is am{group}mtest") == (rgroup('group') + 'this is am' + rgroup('group') + "mtest").str()
    assert replace("this is {{ not a thing") == "this is { not a thing"
    assert replace("also not }} a thing") == "also not } a thing"
    assert replace("still }}not{{ a thing") == "still }not{ a thing"
    assert replace("also {{not}} a thing") == "also {not} a thing"
    assert replace("but {group} is and {1} is") == ("but " + rgroup('group') + " is and " + rgroup(1) + " is").str()
    assert replace("{group}{g}") == (rgroup('group') + rgroup('g')).str()

    assert replace('|{g}|{1}|{0}|', compile=False) == '|' + rgroup('g') + '|' + rgroup(1) + '|' + replace_entire + '|'
    assert replace("{group}this is am{group}mtest", compile=False) == rgroup('group') + 'this is am' + rgroup('group') + "mtest"
    assert replace("this is {{ not a thing", compile=False) == rliteral("this is { not a thing")
    assert replace("also not }} a thing", compile=False) == rliteral("also not } a thing")
    assert replace("still }}not{{ a thing", compile=False) == rliteral("still }not{ a thing")
    assert replace("also {{not}} a thing", compile=False) == rliteral("also {not} a thing")
    assert replace("but {group} is and {1} is", compile=False) == "but " + rgroup('group') + " is and " + rgroup(1) + " is"
    assert replace("{group}{g}", compile=False) == rgroup('group') + rgroup('g')
