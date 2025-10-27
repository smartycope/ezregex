# Compile all regexs in regexs.jsonc to their appropriate languages
try:
    import jstyleson
    import json
    import ezregex as ez

    langs = {'py': ez.python, 'js': ez.javascript, 'r': ez.R, 'pcre': ez.pcre}

    with open('data/regexs.jsonc') as f:
        regexs = jstyleson.load(f)

    output = {
        'py': [],
        'js': [],
        'r': [],
        'pcre': []
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
                print(f'Error compiling regex `{i["re"]}` in {lang}: {str(e)}')
                exit(1)

            output[lang].append({
                'ezregex': i['re'],
                'regex': compiled,
                'should': i['should'],
                'shouldnt': i['shouldnt'],
            })

        with open('data/compiled_regexs.json', 'w') as f:
            json.dump(output, f)
except Exception as e:
    print(f'Error in the compile_regexs.py script: {str(e)}')
    raise e