from ..EZRegex import EZRegex


class PCRE2EZRegex(EZRegex):
    _escape_chars=b'()[]{}?*+-|^$\\.&~# \t\n\r\v\f'
    _repl_escape_chars=b'$'

    def _final_func(self, s:str) -> str:
        if self.replacement:
            # This is how you escape a $ in a replacement string
            return s.replace(r'\$', '$$')
        return s