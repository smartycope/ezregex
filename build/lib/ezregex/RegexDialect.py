from enum import Enum

# This and the singletons are the only things in this file that *can* be used directly
class RegexDialect(Enum):
    GENERIC = 0
    PYTHON = 1
    PERL = 2
