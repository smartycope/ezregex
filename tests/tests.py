import random
import re
from inspect import currentframe, getframeinfo

from rich import print as rprint
from rich.table import Table
from rich.text import Text
from test_generate import *

import ezregex.python as er
from ezregex import api
from ezregex.generate import *
from ezregex.invert import *
from ezregex.python import *

try:
    from Cope import debug
except ImportError:
    pass

# from tests.groups import *
# from tests.groups import _losers, _winners
# from _regexs import *
# from _regexs import _regexsLine


def runTests(singletons=True, _invert=True, replacement=True, _generate=True, testMethod=False, internal=False, operators=True, strictness=20, dontIncludePassed=True, invertBackend='re_parser', invert_tries=1):
    global ow
    if singletons:
        print("Testing EZRegex singletons...")
        # Test the various parameters of anyof()
        assert er.anyof('aiLmsux', split=True, chars=True)._compile(False) == "[aiLmsux]",                  f"Was supposed to be '[aiLmsux]', was actually '{er.anyof('aiLmsux', split=True, chars=True)._compile(False)}'"
        # assert er.anyof('aiLmsux', split=False, chars=True)._compile(False) == Error,                     f"Was supposed to be 'Error', was actually '{er.anyof('aiLmsux', split=False, chars=True)._compile(False)}'"
        assert er.anyof('aiLmsux', split=None, chars=True)._compile(False) == "[aiLmsux]",                  f"Was supposed to be '[aiLmsux]', was actually '{er.anyof('aiLmsux', split=None, chars=True)._compile(False)}'"
        assert er.anyof('aiLmsux', split=True, chars=False)._compile(False) == '(?:a|i|L|m|s|u|x)',         f"Was supposed to be '(?:a|i|L|m|s|u|x)', was actually '{er.anyof('aiLmsux', split=True, chars=False)._compile(False)}'"
        # assert er.anyof('aiLmsux', split=False, chars=False)._compile(False) == Error,                    f"Was supposed to be 'Error', was actually '{er.anyof('aiLmsux', split=False, chars=False)._compile(False)}'"
        assert er.anyof('aiLmsux', split=None, chars=False)._compile(False) == '(?:a|i|L|m|s|u|x)',         f"Was supposed to be '(?:a|i|L|m|s|u|x)', was actually '{er.anyof('aiLmsux', split=None, chars=False)._compile(False)}'"
        assert er.anyof('aiLmsux', split=True, chars=None)._compile(False) == '(?:a|i|L|m|s|u|x)',          f"Was supposed to be '(?:a|i|L|m|s|u|x)', was actually '{er.anyof('aiLmsux', split=True, chars=None)._compile(False)}'"
        # assert er.anyof('aiLmsux', split=False, chars=None)._compile(False) == Error,                     f"Was supposed to be 'Error', was actually '{er.anyof('aiLmsux', split=False, chars=None)._compile(False)}'"
        assert er.anyof('aiLmsux', split=None, chars=None)._compile(False) == "[aiLmsux]",                  f"Was supposed to be '[aiLmsux]', was actually '{er.anyof('aiLmsux', split=None, chars=None)._compile(False)}'"

        # assert er.anyof(*list('aiLmsux'), split=True, chars=True)._compile(False) == Error,               f"Was supposed to be 'Error', was actually '{er.anyof(*list('aiLmsux'), split=True, chars=True)._compile(False)}'"
        assert er.anyof(*list('aiLmsux'), split=False, chars=True)._compile(False) == "[aiLmsux]",          f"Was supposed to be '[aiLmsux]', was actually '{er.anyof(*list('aiLmsux'), split=False, chars=True)._compile(False)}'"
        assert er.anyof(*list('aiLmsux'), split=None, chars=True)._compile(False) == "[aiLmsux]",           f"Was supposed to be '[aiLmsux]', was actually '{er.anyof(*list('aiLmsux'), split=None, chars=True)._compile(False)}'"
        # assert er.anyof(*list('aiLmsux'), split=True, chars=False)._compile(False) == Error,              f"Was supposed to be 'Error', was actually '{er.anyof(*list('aiLmsux'), split=True, chars=False)._compile(False)}'"
        assert er.anyof(*list('aiLmsux'), split=False, chars=False)._compile(False) == '(?:a|i|L|m|s|u|x)', f"Was supposed to be '(?:a|i|L|m|s|u|x)', was actually '{er.anyof(*list('aiLmsux'), split=False, chars=False)._compile(False)}'"
        assert er.anyof(*list('aiLmsux'), split=None, chars=False)._compile(False) == '(?:a|i|L|m|s|u|x)',  f"Was supposed to be '(?:a|i|L|m|s|u|x)', was actually '{er.anyof(*list('aiLmsux'), split=None, chars=False)._compile(False)}'"
        # assert er.anyof(*list('aiLmsux'), split=True, chars=None)._compile(False) == Error,               f"Was supposed to be 'Error', was actually '{er.anyof(*list('aiLmsux'), split=True, chars=None)._compile(False)}'"
        assert er.anyof(*list('aiLmsux'), split=False, chars=None)._compile(False) == "[aiLmsux]",          f"Was supposed to be '[aiLmsux]', was actually '{er.anyof(*list('aiLmsux'), split=False, chars=None)._compile(False)}'"
        assert er.anyof(*list('aiLmsux'), split=None, chars=None)._compile(False) == "[aiLmsux]",           f"Was supposed to be '[aiLmsux]', was actually '{er.anyof(*list('aiLmsux'), split=None, chars=None)._compile(False)}'"

        assert er.anyCharExcept('abcd')._compile(False) == '[^abcd]'
        assert er.anyCharExcept(*list('abcd'))._compile(False) == '[^abcd]'

        # Test flags
        assert str(word + ASCII + stuff)      == r'(?a)\w+.+', fr"{word + ASCII + stuff}      != (?a)\w+.+"
        assert str(word) == r'\w+', f'{word}'
        assert str(word + DOTALL + stuff)     == r'(?s)\w+.+', fr"{word + DOTALL + stuff}     != (?s)\w+.+"
        assert str(word + IGNORECASE + stuff) == r'(?i)\w+.+', fr"{word + IGNORECASE + stuff} != (?i)\w+.+"
        assert str(word + LOCALE + stuff)     == r'(?L)\w+.+', fr"{word + LOCALE + stuff}     != (?L)\w+.+"
        assert str(word + MULTILINE + stuff)  == r'(?m)\w+.+', fr"{word + MULTILINE + stuff}  != (?m)\w+.+"
        # assert str(word + UNICODE + stuff)    == r'(?u)\w+.+', fr"{word + UNICODE + stuff}    != (?u)\w+.+"

        a = word + ow
        # b = stuff + UNICODE
        c = IGNORECASE + '9'
        assert a + c == word + ow + IGNORECASE + '9', f"{a + b + c} != {word + ow + IGNORECASE + '9'}"

        for cnt, r in enumerate(regexs):
            regex, match, dontMatch = r
            try:
                if match is not None:
                    for m in match:
                        assert m in regex, f"{regex} does not match '{m}' (approx. {__file__}, line {_regexsLine+cnt})"
                if dontMatch is not None:
                    for m in dontMatch:
                        assert m not in regex, f"{regex} DOES match '{m}' (approx. {__file__}, line {_regexsLine+cnt})"
            except Exception as err:
                print(regex)
                print(f'Error @ approx. {__file__}, line {_regexsLine+cnt}: \nregex = `{regex}`, match = `{match}`, dontMatch = `{dontMatch}`')
                raise err#.with_traceback(None)

        a = str(EZRegex(r'\s+', 'python'))
        b = str(EZRegex(raw(r'\s+'), 'python'))
        c = r'\s+'
        d = str(raw(r'\s+'))
        # e = str(whitespace + matchMax)
        assert a == b == c == d, f'\na: {a}\n b: {b}\n c: {c}\n d: {d}\n e: {e}'
        # assert (word + ow + anything + ':').test('word    d:', show=False)
        # assert not (word + ow + anything + ':').test('word', show=False)
        assert 'word    d:' in (word + ow + anything + ':')

        test = word + chunk
        test += word
        assert str(test) == str(word + chunk + word), f"{str(test)} != {str(word + chunk + word)}"
        assert test == word + chunk + word
        assert either('(' + word + ')', '.') == either(er.literal('(') + word() + er.literal(')'), '.'), f"{either('(' + word + ')', '.')} != {either(er.literal('(') + word() + er.literal(')'), '.')}"
        assert str(ifFollowedBy(word)) == r'(?=\w+)'

        #TODO: assert (word + ow + anything + ':') in 'word    d:'
        #TODO: assert (word + ow + anything + ':') not in 'word'

    if _invert:
        print("Testing Invert...")

        table = Table(title="invert tests", expand=False)
        table.add_column("Line", justify="center", style="grey37")#, max_width=2)
        table.add_column("Regex", justify="right", style="green")#, max_width=40)
        table.add_column("Inverse", justify="left", style="dim green")
        table.add_column("Success", justify="center")

        for cnt, r in enumerate(regexs + replacements):
            regex = r[0]

            try:
                for _ in range(strictness):
                    # -1 means return it even if it's bad
                    inv = invert(regex, backend=invertBackend, tries=invert_tries)
                    if inv not in regex or not dontIncludePassed:
                        table.add_row(str(_regexsLine+cnt), Text(regex.str()), '`' + inv + '`', Text('passed', style='blue') if inv in regex else Text('failed', style='red'))
            except (Exception, AssertionError) as err:
                print(f'Error @ approx. {__file__}, line {_regexsLine+cnt}: \nregex = `{regex}`')#, inv = `{inv}`')
                raise err#.with_traceback(None)
        if len(table.rows):
            rprint(table)

    if _generate:
        generate_tests()
        test_bb()
        test_new_parts()

        for w, l in zip(_winners, _losers):
            r = re.compile(generate_regex(w, l, 500, restarts=2))
            for i in w:
                assert r.search(i), f"`{r}` is not in `{i}`"
            for i in l:
                assert not r.search(i), f"`{r}` is in `{i}`"
            # print(r, 'is good')

    if replacement:
        for pattern, repl, s, ans in replacements:
            assert re.sub(str(pattern), str(repl), s) == ans, f'Replacing\n\t{pattern}\nwith\n\t{repl}\nin\n\t{s}\nyielded\n\t{re.sub(str(pattern), str(repl), s)}\nnot\n\t{ans}'

    if testMethod:
        # ow = optional(whitechunk)
        params = er.group(er.atLeastNone(er.ow + er.word + er.ow + er.optional(',') + er.ow))
        function = er.word + er.ow + '(' + params + ')'
        function.test('this should match func(param1, param2 ), foo(), and bar( foo,)')

        r = 'group 1' + ':' + ow + group('stuff') + ' | ' + 'group ' + number + ': ' + group('things') + ' | ' + 'named group "' + word + '": '  + named_group('foo', 'bar')
        s = 'random stuff! and then group 1: stuff | group 2: things | named group "foo": bar  \t oh and then more random stuff'
        r.test(s)

        s = 'word1 word2 word3'
        word.test(s)

        (word + whitechunk + group('func') + ':' + namedGroup('test', anyof('8', '7'))).test()

        # This is actually accurate, if you think about it.
        # ifFollowedBy(word).test("literal(hllow) + isExactly('thing')")# fails in _matchJSON()

        ('(' + +(anything + optional(group(comma))) + ')').test()# -- empty groups print as None

        group(+group(number) + group(anyof('98'))).test('999')

    if internal:
        # rprint((word + number)._matchJSON())
        # rprint((word + whitechunk + group('func') + ':' + namedGroup('test', anyof('8', '7')))._matchJSON())
        rprint(ifFollowedBy(word)._matchJSON())
        rprint(word._matchJSON())
        rprint(number._matchJSON('word'))
        r = 'group 1' + ':' + ow + group('stuff') + ' | ' + 'group ' + number + ': ' + group('things') + ' | ' + 'named group "' + word + '": '  + named_group('foo', 'bar')
        s = 'random stuff! and then group 1: stuff | group 2: things | named group "foo": bar  \t oh and then more random stuff'
        rprint(r._matchJSON(s))

    if operators:
        print('Testing operators...')
        # The ~ operator
        for r in random.choices(regexs, k=strictness):
            regex, match, dontMatch = r
            assert re.search(regex.str(), ~regex), f"Invertting with ~ failed to find {regex} in {~regex}"

        # Not sure why this doesn't work?...
        # try:
        #     not anything
        # except NotImplementedError:
        #     pass
        # else:
        #     assert False

        # This is weird...
        digit = er.digit

        # TODO: Finish this
        # assert digit * ... == matchMax(digit)

        # TODO: Debug this
        # assert digit | word == anyof(digit, word), f"{digit | word} != {anyof(digit, word)}"
        # assert 7 | digit == anyof(7, digit), f"{7 | digit} != {anyof(digit, 7)}"
        # assert re.search(str(digit | word | '1'), '1') == re.search(anyof(digit, word, 1).str(), '1')

        assert +digit == matchMax(digit)

        assert anything + word == anything << word
        assert anything + word == anything >> word

        assert digit[2, 3] == match_range(2, 3, digit)
        assert digit[2, ...] == digit[2,] == digit[2, None] == digit[2] == match_at_least(2, digit)
        assert digit[..., 2] == digit[0, 2] == digit[None, 2] == match_at_most(2, digit)
        assert digit[...] == digit[0, ...] == digit[None] == at_least_0(digit)
        assert digit[1, ...] == digit[1] == digit[1,] == digit[1, None] == at_least_1(digit)
        # expr[...:end_expr] is equivalent to ZeroOrMore(expr, stop_on=end_expr)
        # assert digit[...:'foo'] == digit[None:'foo'] == digit[,'foo'] ==

        test = digit
        test += 6
        assert test == digit + 6, f"{test} != {digit + 6}"

        test = digit
        test *= 3
        assert test == digit * 3

        assert 2 * digit == digit * 2

        assert digit % 'sldkj' is None, f'{digit % "sldkj"} != None'
        assert digit % '77sdsf88' == re.search('77sdsf88', digit.str())

        # Test f-strings
        # As of right now, these may work, but won't necissarily work
        # assert f'|{word}|' == '|' + word + '|'
        # assert f'|{word}|{number}|' == '|' + word + '|' + number + '|'
        # assert f"|{word}{number + ifFollowedBy(word)}|" == '|' + word + number + ifFollowedBy(word) + '|'
        # assert f'|{rgroup("g")}|{replace_group}|' == '|' + rgroup('g') + '|' + replace_entire + '|'

        # Replacement strings are, in fact, a thing
        # print(version_info)
        assert replace('|{g}|{1}|{0}|') == '|' + rgroup('g') + '|' + rgroup(1) + '|' + replace_entire + '|'
        assert replace("{group}this is am{group}mtest") == rgroup('group') + 'this is am' + rgroup('group') + "mtest"
        assert replace("this is {{ not a thing") == "this is { not a thing"
        assert replace("also not }} a thing") == "also not } a thing"
        assert replace("still }}not{{ a thing") == "still }not{ a thing"
        assert replace("also {{not}} a thing") == "also {not} a thing"
        assert replace("but {group} is and {1} is") == "but " + rgroup('group') + " is and " + rgroup(1) + " is"
        assert replace("{group}{g}") == rgroup('group') + rgroup('g')

        # no idea why this doesnt work.
        # assert (anything + word) * 3 == '.\w+' * 3, f"'{(anything + word) * 3}' != '{'.\w+'*3}'"

    print('All Tests Passed!')

# From 1-100, 1 is easy, 100 is hard
difficulty = 1
# runTests(
#     # These should remain on, for the GitHub automated tests
#     singletons=True,
#     _invert=False,
#     replacement=True,
#     operators=True,
#     _generate=True,
#     # These display for you to check that they look correct
#     testMethod=False,
#     _api=False,
#     # Settings
#     strictness=difficulty,
#     invert_tries=101-difficulty,
#     dontIncludePassed=True,
#     invertBackend='re_parser',
# )
