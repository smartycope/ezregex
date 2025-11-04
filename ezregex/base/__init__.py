from string import Formatter
from types import EllipsisType
from typing import Callable

from .elements import base, psuedonymns, not_empty, input_not_empty, _parse_any_of_params


def load_base(cls, rgroup_func: Callable[[int|str, EllipsisType], str], replace_entire_func=...) -> dict:
    rtn = {}
    for name, kwargs in base.items():
        rtn[name] = cls(**kwargs)

    # I'm creating this here, so we don't have to reimplement both of them every time
    def replace(string, rtn_str=True):
        class CustomFormatter(Formatter):
            def get_value(self, key, args, kwargs):
                return rgroup_func(key, '')

        string = CustomFormatter().format(string)

        return string if rtn_str else cls(string, sanatize=False, replacement=True)


    rtn['replace'] = replace
    rtn['rgroup'] = cls(rgroup_func, replacement=True)
    rtn['replace_entire'] = cls(
        lambda cur=...: rgroup_func(0, cur=cur) if replace_entire_func is Ellipsis else replace_entire_func,
        replacement=True
    )

    for original, aliases in psuedonymns.items():
        for alias in aliases:
            rtn[alias] = rtn[original]

    return rtn
