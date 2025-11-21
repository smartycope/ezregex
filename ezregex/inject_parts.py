def inject_parts(cls):
    rtn = {i: getattr(cls, i) for i in cls.parts()}
    # It's technically a function, so it's handled differently
    if hasattr(cls, 'replace'):
        rtn['replace'] = cls.replace
    return rtn
