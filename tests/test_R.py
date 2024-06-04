import jstyleson
from ezregex.R import *
from ezregex import EZRegex, R


def test_R():
    print(word + group(digit + '45') + raw('\\w+'))
    assert str(word + group(digit + '45') + raw('\\w+')) == r'\\w+(\\d45)\\w+'
