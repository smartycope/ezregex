from ..EZRegex import EZRegex
from .elements import base


def load_base(dialect, exclude=[]) -> dict:
    rtn = {}
    for name, kwargs in base.items():
        rtn[name] = EZRegex(**kwargs, dialect=dialect)
    return rtn
