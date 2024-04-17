# import jsonc
from ezregex import python
import jstyleson


def test_python():
    offset = 2

    with open('tests/regexs.jsonc') as f:
        regexs = jstyleson.load(f)

    for cnt, r in enumerate(regexs):
        regex_str, match, dontMatch = r
        regex = eval(regex_str, python.__dict__)
        try:
            if match:
                for m in match:
                    assert m in regex, f"{regex} does not match '{m}' (approx. {__file__}, line {offset+(cnt*4)})"
            if dontMatch:
                for m in dontMatch:
                    assert m not in regex, f"{regex} DOES match '{m}' (approx. {__file__}, line {offset+(cnt*4)})"
        except Exception as err:
            print(regex)
            print(f'Error @ approx. {__file__}, line {offset+(cnt*4)}: \nregex = `{regex}`, match = `{match}`, dontMatch = `{dontMatch}`')
            raise err#.with_traceback(None)
