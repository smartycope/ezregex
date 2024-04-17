# import jsonc
from ezregex import javascript
# import js2py
import py_js_runner
import jstyleson
from Cope import RedirectStd

def runjs(js):
    pass
    # with RedirectStd(stdout=):
    #     py_js_runner.javascript().run(js)


def test_javascript():
    return # This should be written in the javascript branch
    offset = 2

    with open('tests/regexs.jsonc') as f:
        regexs = jstyleson.load(f)

    for cnt, r in enumerate(regexs):
        regex_str, match, dontMatch = r
        regex = eval(regex_str, javascript.__dict__)
        try:
            if match:
                for m in match:
                    assert runjs(f'{regex}.exec({m})'), f"{regex} does not match '{m}' (approx. {__file__}, line {offset+(cnt*4)})"
                    # assert m in regex, f"{regex} does not match '{m}' (approx. {__file__}, line {offset+(cnt*4)})"
            if dontMatch:
                for m in dontMatch:
                    assert not runjs(f'{regex}.exec({m})'), f"{regex} DOES match '{m}' (approx. {__file__}, line {offset+(cnt*4)})"
        except Exception as err:
            print(regex)
            print(f'Error @ approx. {__file__}, line {offset+(cnt*4)}: \nregex = `{regex}`, match = `{match}`, dontMatch = `{dontMatch}`')
            raise err#.with_traceback(None)
