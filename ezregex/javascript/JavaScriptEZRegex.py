from ..EZRegex import EZRegex
from functools import partial

class JavaScriptEZRegex(EZRegex):
    _escape_chars=b'()[]{}?*+-|^$\\.&~# \t\n\r\v\f/'
    _repl_escape_chars=b''

    def __init__(self, *args, string_anchor_used=False, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__setattr__('string_anchor_used', string_anchor_used, True)

    # These 3 methods are copied and modified from EZRegex
    # TODO: I'm sure there's a cleaner way to do this
    def _copy(self, definition=..., sanatize=..., replacement=..., flags=..., string_anchor_used=...):
        if definition is Ellipsis:
            definition = self._compile()
        if sanatize is Ellipsis:
            sanatize = self._sanatize
        if replacement is Ellipsis:
            replacement = self.replacement
        if flags is Ellipsis:
            flags = self._flags
        if string_anchor_used is Ellipsis:
            string_anchor_used = self.string_anchor_used

        return type(self)(definition, sanatize=sanatize, replacement=replacement, flags=flags, string_anchor_used=string_anchor_used)

    def __add__(self, thing):
        return self._copy(
            self._funcList + [partial(lambda cur=...: cur + self._sanitizeInput(thing))],
            sanatize=self._sanatize or thing._sanatize if isinstance(thing, EZRegex) else self._sanatize,
            replacement=self.replacement or thing.replacement if isinstance(thing, EZRegex) else self.replacement,
            flags=(self._flags + thing.flags) if isinstance(thing, EZRegex) else self._flags,
            string_anchor_used=self.string_anchor_used or thing.string_anchor_used if isinstance(thing, EZRegex) else self.string_anchor_used
        )

    def __radd__(self, thing):
        return self._copy([partial(lambda cur=...: self._sanitizeInput(thing) + cur)] + self._funcList,
            sanatize=self._sanatize or thing._sanatize if isinstance(thing, EZRegex) else self._sanatize,
            replacement=self.replacement or thing.replacement if isinstance(thing, EZRegex) else self.replacement,
            flags=(self._flags + thing.flags) if isinstance(thing, EZRegex) else self._flags,
            string_anchor_used=self.string_anchor_used or thing.string_anchor_used if isinstance(thing, EZRegex) else self.string_anchor_used
        )

    def _flag_func(self, final):
        if self.string_anchor_used and 'm' in self.flags:
            raise ValueError('string_starts_with and string_ends_with don\'t work with the multiline flag')
        if self.replacement:
            return final
        else:
            return f'/{final}/{self.flags}'

    # def _final_func(self, s:str) -> str:
    #     return f'/{s}/'
