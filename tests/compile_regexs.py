# Compile all regexs in regexs.jsonc to their appropriate languages
import re


try:
    import jstyleson
    import json
    import ezregex as ez
    import traceback

    r_special_chars_map = {
        'a': '\a',
        'b': '\b',
        't': '\t',
        'n': '\n',
        'v': '\v',
        'f': '\f',
        'r': '\r',
    }
    r_special_chars_regex = re.compile(r'\\([abtnvfr])')

    langs = {'py': ez.python, 'js': ez.javascript, 'r': ez.R, 'pcre2': ez.PCRE2}

    with open('data/regexs.jsonc') as f:
        regexs = jstyleson.load(f)

    # Compile regexs
    output = {
        'py': [],
        'js': [],
        'r': [],
        'pcre2': []
    }
    for i in regexs:
        for lang in langs:
            if 'worksIn' in i and lang not in i['worksIn']:
                continue
            if 'doesntWorkIn' in i and lang in i['doesntWorkIn']:
                continue

            try:
                compiled = str(eval(i['re'], langs[lang].__dict__))
            except Exception as e:
                print(f'Error compiling regex `{i["re"]}` in {lang}: {str(e)}\n{traceback.format_exc()}')
                exit(1)

            # This is because the REZRegex class uses doubles backslashes. This is good, when copying to
            # source code (our target use case), but when stuffed directly into a file, and read twice
            # (our tests compilation pipeline) it breaks
            if lang == 'r':
                compiled = compiled.replace('\\\\', '\\')
                compiled = re.sub(r_special_chars_regex, lambda m: r_special_chars_map[m.group(1)], compiled)

            output[lang].append({
                'ezregex': i['re'],
                'regex': compiled,
                'should': i['should'],
                'shouldnt': i['shouldnt'],
            })

    with open('data/compiled_regexs.json', 'w') as f:
        json.dump(output, f)

    # Compile replacements
    with open('data/replacements.jsonc') as f:
        replacements = jstyleson.load(f)

    output = {
        'py': [],
        'js': [],
        'r': [],
        'pcre2': []
    }
    for i in replacements:
        for lang in langs:
            if 'worksIn' in i and lang not in i['worksIn']:
                continue
            if 'doesntWorkIn' in i and lang in i['doesntWorkIn']:
                continue

            try:
                compiled = str(eval(i['re'], langs[lang].__dict__))
                compiled_repl = str(eval(i['repl'], langs[lang].__dict__))
            except Exception as e:
                print(f'Error compiling regex `{i["re"]}` in {lang}: {str(e)}\n{traceback.format_exc()}')
                exit(1)

            if lang == 'r':
                compiled = compiled.replace('\\\\', '\\')
                compiled_repl = compiled_repl.replace('\\\\', '\\')
                compiled = re.sub(r_special_chars_regex, lambda m: r_special_chars_map[m.group(1)], compiled)
                compiled_repl = re.sub(r_special_chars_regex, lambda m: r_special_chars_map[m.group(1)], compiled_repl)

            output[lang].append({
                'ezregex': i['re'],
                'regex': compiled,
                'ezrepl': i['repl'],
                'repl': compiled_repl,
                'base': i['base'],
                'after': i['after'],
            })

    with open('data/compiled_replacements.json', 'w') as f:
        json.dump(output, f)

except Exception as e:
    import sys
    print(f'Error in the compile_regexs.py script: {str(e)}', file=sys.stderr)
    raise e