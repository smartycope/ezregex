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

def _parse_options_params(flag_map, *args, auto_add_uppercase=True, **kwargs):
    if auto_add_uppercase:
        for key, value in flag_map.copy().items():
            flag_map[key.upper()] = value

    flags = set()
    for arg in args:
        if arg in flag_map:
            flags.add(flag_map[arg])
        else:
            raise ValueError(f'Unknown flag: {arg}. Available flags: {tuple(flag_map.keys())}')

    for key, value in kwargs.items():
        if key in flag_map:
            if value:
                flags.add(flag_map[key])
            else:
                try:
                    flags.remove(flag_map[key])
                except KeyError:
                    pass
        else:
            raise ValueError(f'Unknown flag: {key}. Available flags: {tuple(flag_map.keys())}')

    return ''.join(flags)

standard_flag_docs = {
    'ascii': '''Make matching words, word boundaries, digits, and whitespace \
perform ASCII-only matching instead of full Unicode matching (which is \
default). This is only meaningful for Unicode (str) patterns, and is \
ignored for bytes patterns''',
    'ignore_case': '''Perform case-insensitive matching, including expressions that \
explicitly use uppercase members. Full Unicode matching (such as Ü \
matching ü) also works unless the ASCII flag is used to disable \
non-ASCII matches. The current locale does not change the effect of \
this flag unless the LOCALE flag is also used''',
    'unicode': '''Match using the full unicode standard, instead of just ASCII. \
Enabled by default, and therefore redundant''',
    'global': '''Global mode. Match everything in the given string, instead of just the first match''',
    'anchor': '''The pattern is forced to become anchored at the start of the \
search or at the position of the last successful match.''',
    'single_line': '''Not recommended. Makes the '.' special character match any character at all, including \
a newline. It's recommended you simply use literally_anything instead''',
    'multiline': '''Not recommended. Makes the '^' and '$' special characters match the start and end of \
lines, instead of the start and end of the string. This is automatically inserted when using \
line_start and line_end, you shouldn\'t need to add it manually''',
    'verbose': '''Not recommended. Allows for comments and whitespace, which both don\'t do anything \
in this library.''',
    'lazy': '''The engine will per default to lazy matching, instead of greedy. It's recommended you \
just specify greedy=False instead''',
    'duplicate_groups': '''This allows regex to accept duplicate pattern names, \
however each capture group still has its own ID. Thus the two capture \
groups produce their own match instead of a single combined one''',
}

def _generate_options_from_flags(cls, flag_map, auto_add_uppercase=True, docs_map={}, docs_link=''):
    # This is a function, not an EZRegex subclass, by intention
    def options(*args, **kwargs):
        flags = _parse_options_params(flag_map, *args, auto_add_uppercase=auto_add_uppercase, **kwargs)
        return cls(lambda cur=...: cur, flags=flags, options_specified=True)

    docs = ''
    if docs_link:
        docs += f"Documentation: \n\t{docs_link}\n\n"
    docs += '''Usage:
    word + options(ignore_case=True)
    word + options('ignore_case')
    word + options('ignore_case', 'multiline')
    word + options('ignore_case', multiline=True)

Args:
'''
    _docs = standard_flag_docs.copy()
    _docs.update({k.lower(): v for k, v in docs_map.items()})
    for flag in flag_map.keys():
        try:
            docs += f"\t{flag.lower()}:\n\t\t{_docs[flag.lower()]}\n"
        except KeyError:
            docs += f"\t{flag.lower()}\n"
    options.__doc__ = docs

    return options

