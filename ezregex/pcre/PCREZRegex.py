from ..EZRegex import EZRegex


class PCREZRegex(EZRegex):
    _escape_chars=b'()[]{}?*+-|^$\\.&~# \t\n\r\v\f'

    def _flag_func(self, final):
        return f'(?{self.flags}){final}'
