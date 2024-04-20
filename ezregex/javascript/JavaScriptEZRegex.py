from ..EZRegex import EZRegex


class JavaScriptEZRegex(EZRegex):
    _escape_chars=b'()[]{}?*+-|^$\\.&~# \t\n\r\v\f'
    _end = '/'
    _beginning = '/'

    def _flag_func(self, final):
        return final + self.flags
