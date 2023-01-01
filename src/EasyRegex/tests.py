from EasyRegex import *
from EasyRegex.invert import *
# from .invert import *
# from .__init__ import *
import re
from Cope import *

todo('test invert of (stuff)? some more (it might be always removing it)')
todo('invert notAnyCha/rs ([^s,t]) failed, it selected a char specified')
todo('invert [:punct:]')
todo('invert colors dont work')
todo('add a letter singleton')


def runTests(singletons=True, invert=True, unsanitize_=False, unitTests=False, strictness=20):
    # test = word() + whitespace() # + whiteChunk()
    # test = wordChar() + whitespace()
    # test = wordChar()
    # str(test)
    # debug()
    # return

    ow = optional(whitechunk())
    # debug()
    w = whitechunk()
    regexs = [
        'stuff' + anyof('a', 'b', 'c') + ' ' + optional(comma()) + space() + ifFollowedBy('*'),
        optional(word() + ow + ':' + ow) + group(word()) + optional(',') + ow,
        optional(w + 'as' + word()),
        group(optional(matchMax(match('.') + word()))),
        matchNum(3, either("'", '"')),
        raw(r'\A'),
        raw(r'\Z'),
        exactly('test'),
        raw(r'(test)+'),
        raw(r'test+'),
        raw(r'(test){3}'),
        raw(r'test{3}'),
        raw(r'(test){3,5}'),
        # raw(r'(test){3, 5}'), These *should* fail
        # raw(r'test{3, 5}'),
        raw(r'test{3,5}'),
        raw(r'(test){3,}'),
        raw(r'test{3,}'),
        raw(r'\d'),
        raw(r'\s'),
        raw(r'\w'),
        raw(r'\w+'),
        raw(r'.'),
        raw(r'\n'),
        raw(r'\r'),
        raw(r'\t'),
        raw(r'\v'),
        raw(r'\f'),
        raw(r'\S'),
        raw(r'\D'),
        raw(r'\W'),
        raw(r'(stuff)?'),
        raw(r'(stuff)*'),
        raw(r'(stuff|things)'),
        raw(r'[s,t]'),
        raw(r'[^s,t]'),
        raw(r'(?=stuff)'),
        raw(r'(?!stuff)'),
        raw(r'(stuff)'),
        raw(r'(?:stuff)'),
        raw(r'(?P<name>stuff)'),
        raw(r'(?<=stuff)'),
        raw(r'(?<!stuff)'),
        raw(r'(a|b|c|thing|st)uff'),
        # ifEnclosedWith('(', namedGroup('stuff', word()), ')')
    ]

    shouldMatch = [
        (
            'stuffa , *',
            'stuffb  *',
        ),
    ]

    if singletons:
        debug("Testing EasyRegex Singletons:", color=2)

        test = word() + whiteChunk()
        assert str(test) == '\w+\s+'
        debug(test)
        # str(test)
        # debug()
        # return

        for cnt, r in enumerate(regexs):
            # r.debug()
            if cnt < len(shouldMatch):
                for should in shouldMatch[cnt]:
                    assert r.test(should)

    if unsanitize_:
        debug("Testing unsantize:", color=2)
        for i in (
            ', ? : ( ) a d %      ',
            ', ? : \( \) a g %    ',
            '\, \? \: \( \) 2 4 %,',
            '\, \? \: \( \) d %   ',
        ):
            debug(unsanitize(i), name=f'Unsanitized <{i}>')

    if unitTests:
        debug("Running EasyRegex Singleton Unit Tests:", color=2)
        # Tests __radd__()
        assert either('(' + word() + ')', '.') == either(match('(') + word() + match(')'), '.')

    if invert:
        debug("Testing EasyRegex Invert:", color=2)
        # for r in regexs:
        #     print(f'{r} should match:')
        #     invertTest(r, colors=False, groupNames=False)

        for r in regexs:
            debug()
            for _ in range(strictness):
                assert r.test(invertRegex(r, colors=False, groupNames=False, explicitConditionals=False))

runTests(
    singletons=False,
    invert=True,
    unsanitize_=False,
    unitTests=False,
)