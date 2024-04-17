from types import EllipsisType
from typing import Callable
from ..EZRegex import EZRegex
from .elements import base
from string import Formatter


def load_base(dialect, rgroup_func: Callable[[int|str, EllipsisType], str], replace_entire_func=...) -> dict:
    rtn = {}
    for name, kwargs in base.items():
        rtn[name] = EZRegex(**kwargs, dialect=dialect)

    # I'm creating this here, so we don't have to reimplement both of them every time
    def replace(string, rtn_str=True):
        class CustomFormatter(Formatter):
            def get_value(self, key, args, kwargs):
                return rgroup_func(key, '')

        string = CustomFormatter().format(string)

        return string if rtn_str else EZRegex(string, dialect, sanatize=False, replacement=True)


    rtn['replace'] = replace
    rtn['rgroup'] = EZRegex(rgroup_func, dialect, replacement=True)
    rtn['replace_entire'] = EZRegex(
        lambda cur=...: rgroup_func(0, cur=cur) if replace_entire_func is Ellipsis else replace_entire_func,
        dialect,
        replacement=True
    )

    return rtn
