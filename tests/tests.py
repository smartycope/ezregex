import re
from inspect import currentframe, getframeinfo

from rich import print as rprint
from rich.table import Table
from rich.text import Text

import ezregex as er
from ezregex import *
from ezregex.invert import *

_regexsLine = getframeinfo(currentframe()).lineno + 3
# This goes (regex, ((things it should match), (things it shouldnt match)))
regexs = (
    ('stuff' + ' ' + optional(comma) + space + ifFollowedBy('*'), (['stuff , *', 'stuff  *'], None)),
    ('stuff' + anyof('a', 'b', 'c') + ' ' + optional(comma) + space + ifFollowedBy('*'), (['stuffa , *', 'stuffb  *'], None)),
    (anyof('a', 'b', 'c') + ' ' + optional(comma) + space + ifFollowedBy('*'), (['a , *', 'b  *'], None)),
    ('stuff' + anyof('a', 'b', 'c'), (['stuffa', 'stuffb'], None)),
    (anyof('a', 'b', 'c'), (['a', 'b', 'c'], None)),
    ('a' + ifFollowedBy('*'), (['a*'], None)),
    (optional(comma) + space, ([', ', ' '], None)),
    (optional(word + ow + ',' + ow) + group(word) + optional(',') + ow, (['word\t ,word2, ', 'word', 'worddsfs    ', 'word,   '], ('', '  '))),
    (optional(whitechunk + 'as' + word), ([' asword'], None)),
    (group(optional(matchMax(er.match('.') + word))), (['..........word', ''], None)),
    (matchNum(3, either("'", '"')), (['"""'], None)),
    (matchNum(2, '0'), (['00'], None)),
    (matchNum(1, raw('6')), (['6'], None)),
    (raw(r'\A'), ([''], None)),
    (raw(r'\Z'), ([''], None)),
    (exactly('test'), (['test'], None)),
    (raw(r'(test)+'), (['test', 'testt', 'testtt', 'testttt'], None)),
    (raw(r'test+'), (['testtesttest'], None)),
    (raw(r'(test){3}'), (['testtesttest'], None)),
    (raw(r'test{3}'), (['testttt'], None)),
    (raw(r'(test){3,5}'), (['testtesttest', 'testtesttesttesttest'], None)),
    (raw(r'(test){3, 5}'), (None, None)),
    (raw(r'test{3, 5}'), (None, None)),
    (raw(r'test{3,5}'), (['testttt', 'testttttt'], None)),
    (raw(r'(test){3,}'), (['testtesttest', 'testtesttesttest', 'testtesttesttesttest'], None)),
    (raw(r'test{3,}'), (['testttt', 'testtttt', 'testttttt'], None)),
    (raw(r'\d'), (['0', '1', '2'], None)),
    (raw(r'\s'), ([' ', '\t', '\n'], None)),
    (raw(r'\w'), (['a', 'Z', '5', '_'], None)),
    (raw(r'\w+'), (['abc', '123', 'test_'], None)),
    (raw(r'.'), ('sahrdhcfGSGD87w3ue84125asd_;.,?.134*&^`'.split(), None)),
    (raw(r'\n'), (['\n'], None)),
    (raw(r'\r'), (['\r'], None)),
    (raw(r'\t'), (['\t'], None)),
    (raw(r'\v'), (['\v'], None)),
    (raw(r'\f'), (['\f'], None)),
    (raw(r'\S'), ('sdgSGHR5122$%^&*Z`'.split(), None)),
    (raw(r'\D'), ('sdfGSDG;([]'.split(), None)),
    (raw(r'\W'), ('/*-#^&*`?><'.split(), None)),
    (raw(r'(stuff)?'), (['stuff', ''], None)),
    (raw(r'(stuff)*'), (['', 'stuff', 'stuffstuff', 'stuff'*3], None)),
    (raw(r'(stuff|things)'), (['stuff', 'things'], None)),
    (raw(r'[s,t]'), (['s', 't'], None)),
    (raw(r'[^s,t]'), ('qwruiopahjkBNM34#$'.split(), None)),
    (raw(r'(?=stuff)'), (['stuff'], None)),
    (raw(r'(?!stuff)'), (['stuff'], None)),
    (raw(r'(stuff)'), (['stuff'], None)),
    (raw(r'(stuff)?'), (["stuff", ''], None)),
    (raw(r'(?P<name>stuff)'), (['stuff'], None)),
    (raw(r'(?<=stuff)'), (['thingstuffs'], None)),
    (raw(r'(?<!stuff)'), (['thingstuffs'], None)),
    (raw(r'(a|b|c|thing|st)uff'), (["auff", "buff", "cuff", "thinguff", "stuff"], None)),
    (stringStartsWith('a'), (('asdfs', 'a 89sdf a', 'a'), (' asdf', 'sdfa', 'sdf'))),
    (lineStartsWith('a'), (('asdfs', 'a 89sdf a', 'a', 'sdfs\nasdfd'), (' asdf', 'sdf\nsdf', 'sdf\n a', 'sdfa', 'sdf'))),
    (stringEndsWith('a'), (('lklkjfda', 'sdf 8 a', 'a'), ('asdfds', 'sd fd'))),
    (lineEndsWith('a'), (('lklkjfda', 'sdf 8 a', 'a', 'sdf\na', 'sdfse\nsdafsda', 'sdfa\nsdf'), ('asdfds', 'sd fd'))),
    (er.match('test'), (('test', ' sdfstestsdfs',), ('te st',))),
    (isExactly('test'), (('test',), ('a test', 'test '))),
    (matchMax('a'), (('aaa', 'a'), ('b',))),
    (matchMoreThan(3, 'a'), (('aaaa', 'tesaaaaaat'), ('aaa',' aa'))),
    (matchAtLeast(3, 'a'), (('aaa', 'aaaa'), ('aa',))),
    (optional('a'), (('', 'a', 'aa'), None)),
    (either('a', 'b'), (('a', 'b'), ('c',))),
    (either('aa', 'ba'), (('aa', 'ba',), ('bb', 'a'))),
    (whitespace, ((' ', '\t', '\t  ', '\n'), ('dfsd',))),
    (whitechunk, ((' ', '\t', '\t  ', '\n'), ('dfsd',))),
    (digit, (('6',), ('_', '-', 'a'))),
    (number, (('6', '69'), ('-a', 'A'))),
    (wordChar, (('w',), ('-',))),
    (hexDigit, (('A', 'a', '0'), ('g', 'G'))),
    (octDigit, (('7',), ('9', 'a', 'A', '8'))),
    (chunk, (('wordssdf   asdf\n',), ('\n',))),
    (spaceOrTab, ((' ', '\t', ' \t  '), ('\n',))),
    (newLine, (('\n',), ('\r',))),
    (carriageReturn, (('\r',), ('\n',))),
    (tab, (('\t',), (' ',))),
    (space, ((' ',), ('\t',))),
    (quote, (('"', "'"), ('`',))),
    (comma, ((',',), ('.', '`'))),
    (period, (('.',), (',',))),
    (matchRange(3, 5, 'a'), (('aaa', 'aaaa', 'a'*5, 'a'*6), ('aa',))),
    (matchRange(3, 5, 'a', greedy=False)+'aa', (('a'*5, 'a'*6), ('aa',))),
    (optional('a') + 'b', (('b', 'ab','cb'), ('','c'))),
    (optional('a', greedy=False) + 'b', (('b', 'ab','cb'), ('','c'))),
    (atLeastOne('a'), (('a','aa', 'a'*20), ('', 'b'))),
    (atLeastOne('a', greedy=False), (('a','aa', 'a'*20), ('', 'b'))),
    (atLeastNone('a'), (('', 'a', 'a'*20, 'b'), None)),
    ((optional('a') + 'b') * 3, (('abbb', 'bbb', 'ababab', 'bbab'), ('', 'aaa', 'aa', 'a'))),
    (word + whitechunk + group('func') + ':' + '()' + namedGroup('test', either('|', '7')), (('wo  func:()|', 'wo  func:()7'), None)),
    (word + whitechunk + group('func') + ':' + namedGroup('test', anyof('8', '7')), (('wo  func:8', 'wo  func:7'), None)),
    # TODO:
    # (matchRange(3, 5, 'a', possessive=True) + 'aa', (('a'*7,), ('a'*6,))),
    # (optional('a', possessive=True) + 'b', (('',), ('',))),
    # (atLeastOne(possessive=True), (('',), ('',))),
    # (atLeastNone(possessive=True), (('',), ('',))),
    # verticalTab, (('',), ('',)),
    # formFeed, (('',), ('',)),
    # either('a', 'b'), (('a', 'b'), None)),
    # multiOptional, (('',), ('',)),
    # anyBetween, (('',), ('',)),
    # (unicode, (('',), ('',)),
    # (word, (('word',), ('33a',))), # Is this *supposed* to work??
)


def runTests(singletons=True, invert=False, unitTests=True, replacement=False, testMethod=False, strictness=20, dontIncludePassed=True):
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

        assert er.anyCharExcept('abcd')._compile(False) == '[!abcd]'
        assert er.anyCharExcept(*list('abcd'))._compile(False) == '[!abcd]'

        # Test flags
        assert str(word + ASCII + stuff)      == '(?a)\w+.+', f"{word + ASCII + stuff}      != (?a)\w+.+"
        assert str(word) == '\w+', f'{word}'
        assert str(word + DOTALL + stuff)     == '(?s)\w+.+', f"{word + DOTALL + stuff}     != (?s)\w+.+"
        assert str(word + IGNORECASE + stuff) == '(?i)\w+.+', f"{word + IGNORECASE + stuff} != (?i)\w+.+"
        assert str(word + LOCALE + stuff)     == '(?L)\w+.+', f"{word + LOCALE + stuff}     != (?L)\w+.+"
        assert str(word + MULTILINE + stuff)  == '(?m)\w+.+', f"{word + MULTILINE + stuff}  != (?m)\w+.+"
        assert str(word + UNICODE + stuff)    == '(?u)\w+.+', f"{word + UNICODE + stuff}    != (?u)\w+.+"

        a = word + ow
        b = stuff + UNICODE
        c = IGNORECASE + '9'
        assert a + b + c == word + ow + stuff + UNICODE + IGNORECASE + '9', f"{a + b + c} != {word + ow + stuff + UNICODE + IGNORECASE + '9'}"

        for cnt, r in enumerate(regexs):
            regex, matches = r
            match, dontMatch = matches
            try:
                if match is not None:
                    for m in match:
                        assert m in regex, f"{regex} does not match '{m}' (approx. {__file__}, line {_regexsLine+cnt})"
                if dontMatch is not None:
                    for m in dontMatch:
                        assert m not in regex, f"{regex} DOES match '{m}' (approx. {__file__}, line {_regexsLine+cnt})"
            except Exception as err:
                print(f'Error @ approx. {__file__}, line {_regexsLine+cnt}: \nregex = `{regex}`, match = `{match}`, dontMatch = `{dontMatch}`')
                raise err

    if unitTests:
        print("Running EasyRegex Singleton Unit Tests...")
        a = str(EZRegexMember('\s+'))
        b = str(EZRegexMember(raw('\s+')))
        c = '\s+'
        d = str(raw('\s+'))
        e = str(whitespace + matchMax)
        assert a == b == c == d == e, f'\na: {a}\n b: {b}\n c: {c}\n d: {d}\n e: {e}'
        assert (word + ow + anything + ':').test('word    d:', show=False)
        assert not (word + ow + anything + ':').test('word', show=False)
        assert 'word    d:' in (word + ow + anything + ':')

        test = word + chunk
        test += word
        assert str(test) == str(word + chunk + word), f"{str(test)} != {str(word + chunk + word)}"
        assert test == word + chunk + word
        assert either('(' + word + ')', '.') == either(er.match('(') + word() + er.match(')'), '.'), f"{either('(' + word + ')', '.')} != {either(er.match('(') + word() + er.match(')'), '.')}"
        # assert (word + ow + anything + ':') in 'word    d:'
        # assert (word + ow + anything + ':') not in 'word'

    if invert:
        print("Testing Invert...")

        table = Table(title="invert tests", expand=False)
        table.add_column("Line", justify="center", style="grey37")#, max_width=2)
        table.add_column("Regex", justify="right", style="green")#, max_width=40)
        table.add_column("Inverse", justify="left", style="dim green")
        table.add_column("Success", justify="center")

        for cnt, r in enumerate(regexs):
            regex, matches = r
            match, dontMatch, = matches
            if match is None:
                continue
            try:
                for _ in range(strictness):
                    # -1 means return it even if it's bad
                    inv = invertRegex(regex, tries=-1)
                    if inv not in regex or not dontIncludePassed:
                        table.add_row(str(_regexsLine+cnt), Text(regex.str()), '`' + inv + '`', Text('passed', style='blue') if inv in regex else Text('failed', style='red'))
            except Exception as err:
                print(f'Error @ approx. {__file__}, line {_regexsLine+cnt}: \nregex = `{regex}`')#, inv = `{inv}`')
                raise err

        rprint(table)

    if replacement:
        print('Testing replacement singletons...')
        r = group(word + number) + ':' + ow + group(word)
        sub = replace_group(1) + ' - ' + replace_group(2)
        subbed = re.sub(r.str(), sub.str(), 'test1:    thing')
        assert subbed == 'test1 - thing', f'`{subbed}` != `test1 - thing`'

        r = namedGroup('a', word + number) + ':' + ow + namedGroup('b', word)
        sub = replace_group('a') + ' - ' + replace_group('b')
        subbed = re.sub(r.str(), sub.str(), 'test1:    thing')
        assert subbed == 'test1 - thing', f'`{subbed}` != `test1 - thing`'

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

    print('All Tests Passed!')

runTests(
    singletons=False,
    invert=True,
    unitTests=True,
    replacement=True,
    testMethod=True,
    strictness=2,
    dontIncludePassed=True
)
