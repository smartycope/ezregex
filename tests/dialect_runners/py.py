import re, json

with open('data/compiled_regexs.json') as f:
    regexs = json.load(f)['py']

def myassert(b, should_be, i, failing, e=None):
    if bool(b) != should_be:
        print(f'''
----------------------- TEST FAILED -----------------------
language       = `py`
pattern        = `{i['ezregex']}`
compiled regex = `{i['regex']}`
pattern should {'' if should_be else 'NOT '}match `{failing.replace('\n', '\\n')}`
''')
        if e:
            raise e
        exit(1)

for i in regexs:
    for m in i['should']:
        try:
            myassert(re.search(i['regex'], m), True, i, m)
        except Exception as e:
            myassert(False, True, i, m, e)
    for m in i['shouldnt']:
        try:
            myassert(re.search(i['regex'], m), False, i, m)
        except Exception as e:
            myassert(True, False, i, m, e)

with open('data/compiled_replacements.json') as f:
    replacements = json.load(f)['py']

def repl_assert(i, actual):
    if actual != i['after']:
        print(f'''
----------------------- TEST FAILED -----------------------
language       = `py`
pattern        = `{i['ezregex']}`
compiled regex = `{i['regex']}`
replacement    = `{i['ezrepl']}`
compiled repl  = `{i['repl']}`
base           = `{i['base']}`
after          = `{i['after']}`

Replacing
    `{i["ezregex"]}`
with
    `{i["repl"]}`
in
    `{i["base"]}`
yielded
    `{actual}`
not
    `{i["after"]}`
''')
        exit(1)

for i in replacements:
    try:
        repl_assert(i, re.sub(i['regex'], i['repl'], i['base']))
    except Exception as e:
        print(f'Error replacing `{i["ezregex"]}` with `{i["repl"]}` in `{i["base"]}`: {str(e)}')
        exit(1)

print('pass')