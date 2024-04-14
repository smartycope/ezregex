# This is the final say of what's supported
# Even though they can still import elements directly from the other modules, they'll fail if they're not here
dialects = {
    'python': {
        "beginning": '',
        "end": '',
        'flag_func': lambda final, flags: f'(?{flags}){final}',
        'escape_chars': b'()[]{}?*+-|^$\\.&~# \t\n\r\v\f',
    },
    'javascript': {
        "beginning": '/',
        "end": '/',
        'flag_func': lambda final, flags: final + flags,
        'escape_chars': b'()[]{}?*+-|^$\\.&~# \t\n\r\v\f',
    },
    'perl': {
        "beginning": '',
        "end": '',
        'flag_func': lambda final, flags: f'(?{flags}){final}',
        'escape_chars': b'()[]{}?*+-|^$\\.&~# \t\n\r\v\f',
    },

}
