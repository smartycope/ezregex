from ..EZRegex import EZRegex


class REZRegex(EZRegex):
    _escape_chars=b'()[]{}?*+-|^$\\.&~# '

    def _flag_func(self, final):
        return f'(?{self.flags}){final}'

    def _final_func(self, s:str) -> str:
        return s.replace('\\', '\\\\')
