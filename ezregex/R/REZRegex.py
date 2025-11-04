from ..EZRegex import EZRegex
import re

class REZRegex(EZRegex):
    # Source: https://www.rdocumentation.org/packages/base/versions/3.6.2/topics/regex
    _escape_chars=b'|()[{^$*+?.-'
    _repl_escape_chars=b''

    def _final_func(self, s:str) -> str:
        # Double escape all backslashes
        s = s.replace('\\', '\\\\')
        # Things which are control characters should *not* be double escaped
        s = re.sub(r'\\\\([abtnvfrxuU])', r'\\\g<1>', s)
        return s
