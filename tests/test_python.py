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
        # try:
        if match:
            for m in match:
                assert m in regex, f"{r[0]} does not match '{m}'"
        if dontMatch:
            for m in dontMatch:
                assert m not in regex, f"{r[0]} DOES match '{m}'"
        # except Exception as err:
            # raise ValueError(f'pattern = `{r[0]}`, match = `{match}`, dontMatch = `{dontMatch}`') from err
