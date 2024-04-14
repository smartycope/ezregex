from .python import spec as python_spec
from .javascript import spec as javascript_spec

# This is the final say of what's supported
dialects = {
    'python': python_spec,
    'javascript': javascript_spec,
}
