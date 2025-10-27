import re, json

with open('data/compiled_regexs.json') as f:
    regexs = json.load(f)['py']

def myassert(b, should_be, i, failing):
    if bool(b) != should_be:
        print(f'''
----------------------- TEST FAILED -----------------------
language       = `py`
pattern        = `{i['ezregex']}`
compiled regex = `{i['regex']}`
pattern should {'' if should_be else 'NOT '}match `{failing.replace('\n', '\\n')}`
''')
        exit(1)

for i in regexs:
    for m in i['should']:
        myassert(re.search(i['regex'], m), True, i, m)
    for m in i['shouldnt']:
        myassert(re.search(i['regex'], m), False, i, m)

print('pass')