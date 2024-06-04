# import jsonc
from ezregex.javascript import *
# import js2py
import jstyleson
import py_js_runner
from Cope import RedirectStd


def runjs(js):
    pass
    # with RedirectStd(stdout=):
    #     py_js_runner.javascript().run(js)


def test_javascript():
    assert str(word + group(digit + 'test') + raw(r'\w+')) == r'/\w+(\dtest)\w+/'
    # TODO: JS dialect tests
    return
    offset = 2

    with open('tests/data/regexs.jsonc') as f:
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
