from ..EZRegex import EZRegex


class JavaScriptEZRegex(EZRegex):
    _escape_chars=b'()[]{}?*+-|^$\\.&~# \t\n\r\v\f'

    def _flag_func(self, final):
        return final + self.flags

    def _final_func(self, s:str) -> str:
        return f'/{s}/'
