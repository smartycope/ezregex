spec = {
    "beginning": '',
    "end": '',
    'flag_func': lambda final, flags: f'(?{flags}){final}',
    'escape_chars': b'()[]{}?*+-|^$\\.&~# \t\n\r\v\f',
}
