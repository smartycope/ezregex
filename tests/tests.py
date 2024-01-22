import re
from inspect import currentframe, getframeinfo

from rich import print as rprint
from rich.table import Table
from rich.text import Text

import ezregex.python as er
from ezregex.python import *
from ezregex.invert import *

import random

try:
    from Cope import debug
except ImportError:
    pass

# TODO: Someday, move all this to a json file instead
# This goes (regex,                                                                         (things it should match),                                    (things it shouldnt match))
_regexsLine = getframeinfo(currentframe()).lineno + 2
regexs = (
    ('stuff' + ' ' + optional(comma) + space + ifFollowedBy('*'),                           ['stuff , *', 'stuff  *'],                                              None),
    ('stuff' + anyof('a', 'b', 'c') + ' ' + optional(comma) + space + ifFollowedBy('*'),    ['stuffa , *', 'stuffb  *'],                                            None),
    (anyof('a', 'b', 'c') + ' ' + optional(comma) + space + ifFollowedBy('*'),              ['a , *', 'b  *'],                                                      None),
    ('stuff' + anyof('a', 'b', 'c'),                                                        ['stuffa', 'stuffb'],                                                   None),
    (anyof('a', 'b', 'c'),                                                                  ['a', 'b', 'c'],                                                        None),
    (one_of('a', 'b', 'c'),                                                                 ['a', 'b', 'c'],                                                        None),
    ('a' + ifFollowedBy('*'),                                                               ['a*'],                                                                 None),
    (optional(comma) + space,                                                               [', ', ' '],                                                            None),
    (optional(word + ow + ',' + ow) + group(word) + optional(',') + ow,                     ['word\t ,word2, ', 'word', 'worddsfs    ', 'word,   '],                ('', '  ')),
    (optional(whitechunk + 'as' + word),                                                    [' asword'],                                                            None),
    (group(optional(matchMax(er.literal('.') + word))),                                     ['..........word', ''],                                                 None),
    (matchNum(3, either("'", '"')),                                                         ['"""'],                                                                None),
    (matchNum(2, '0'),                                                                      ['00'],                                                                 None),
    (matchNum(1, raw('6')),                                                                 ['6'],                                                                  None),
    (raw(r'\A'),                                                                            [''],                                                                   None),
    (raw(r'\Z'),                                                                            [''],                                                                   None),
    (exactly('test'),                                                                       ['test'],                                                               None),
    (raw(r'(test)+'),                                                                       ['test', 'testt', 'testtt', 'testttt'],                                 None),
    (raw(r'test+'),                                                                         ['testtesttest'],                                                       None),
    (raw(r'(test){3}'),                                                                     ['testtesttest'],                                                       None),
    (raw(r'test{3}'),                                                                       ['testttt'],                                                            None),
    (raw(r'(test){3,5}'),                                                                   ['testtesttest', 'testtesttesttesttest'],                               None),
    (raw(r'(test){3, 5}'),                                                                  None,                                                                   None),
    (raw(r'test{3, 5}'),                                                                    None,                                                                   None),
    (raw(r'test{3,5}'),                                                                     ['testttt', 'testttttt'],                                               None),
    (raw(r'(test){3,}'),                                                                    ['testtesttest', 'testtesttesttest', 'testtesttesttesttest'],           None),
    (raw(r'test{3,}'),                                                                      ['testttt', 'testtttt', 'testttttt'],                                   None),
    (raw(r'\d'),                                                                            ['0', '1', '2'],                                                        None),
    (raw(r'\s'),                                                                            [' ', '\t', '\n'],                                                      None),
    (raw(r'\w'),                                                                            ['a', 'Z', '5', '_'],                                                   None),
    (raw(r'\w+'),                                                                           ['abc', '123', 'test_'],                                                None),
    (raw(r'.'),                                                                             'sahrdhcfGSGD87w3ue84125asd_;.,?.134*&^`'.split(),                      None),
    (raw(r'\n'),                                                                            ['\n'],                                                                 None),
    (raw(r'\r'),                                                                            ['\r'],                                                                 None),
    (raw(r'\t'),                                                                            ['\t'],                                                                 None),
    (raw(r'\v'),                                                                            ['\v'],                                                                 None),
    (raw(r'\f'),                                                                            ['\f'],                                                                 None),
    (raw(r'\S'),                                                                            'sdgSGHR5122$%^&*Z`'.split(),                                           None),
    (raw(r'\D'),                                                                            'sdfGSDG;([]'.split(),                                                  None),
    (raw(r'\W'),                                                                            '/*-#^&*`?><'.split(),                                                  None),
    (raw(r'(stuff)?'),                                                                      ['stuff', ''],                                                          None),
    (raw(r'(stuff)*'),                                                                      ['', 'stuff', 'stuffstuff', 'stuff'*3],                                 None),
    (raw(r'(stuff|things)'),                                                                ['stuff', 'things'],                                                    None),
    (raw(r'[s,t]'),                                                                         ['s', 't'],                                                             None),
    (raw(r'[^s,t]'),                                                                        'qwruiopahjkBNM34#$'.split(),                                           None),
    (raw(r'(?=stuff)'),                                                                     ['stuff'],                                                              None),
    (raw(r'(?!stuff)'),                                                                     ['stuff'],                                                              None),
    (raw(r'(stuff)'),                                                                       ['stuff'],                                                              None),
    (raw(r'(stuff)?'),                                                                      ["stuff", ''],                                                          None),
    (raw(r'(?P<name>stuff)'),                                                               ['stuff'],                                                              None),
    (raw(r'(?<=stuff)'),                                                                    ['thingstuffs'],                                                        None),
    (raw(r'(?<!stuff)'),                                                                    ['thingstuffs'],                                                        None),
    (raw(r'(a|b|c|thing|st)uff'),                                                           ["auff", "buff", "cuff", "thinguff", "stuff"],                          None),
    (raw(r"A AB ABC [^A] [^ABC] A+ A* A? AA* A{2} A{2,4} A{9,12} A{2,} A{,9}"),             None,                                                                   None), # I found these online for testing a different regex suite.
    (raw(r"[\d] [^\d] [A-Za-z0-9_]+ . .*"),                                                 None,                                                                   None), # Figured they'd make good tests.
    (raw(r"AB|CD AB|CD|EF|GH (AB|CD)*"),                                                    None,                                                                   None),
    (raw(r"(a??) a*? a{3,}? ab{4,7}?"),                                                     None,                                                                   None),
    (raw(r"(?P<test>ABC*) (?P<a>x)|(?P<b>y)"),                                              None,                                                                   None),
    (raw(r"[b:]+ (b)|(:+) a|(b)"),                                                          None,                                                                   None),
    (raw(r"(?:(?P<a1>a)|(?P<b2>b))(?P<c3>c)?"),                                             None,                                                                   None),
    (raw(r"(?P<name>[a-zA-Z]+)(?P=name)"),                                                  None,                                                                   None),
    (group(+letter, name='g') + earlierGroup('g'),                                          ('AA', 'tt'),                                                           ('ABt','t', '9d9', 'tdt')),
    (group(+letter) + ' ' + earlierGroup(1),                                                ('the the', 'at at'),                                                   ('att', 'thethe')),
    (raw(r"[AB\]C] [--A] [ABC\-D] [\^ABC]"),                                                None,                                                                   None),
    (stringStartsWith('a'),                                                                 ('asdfs', 'a 89sdf a', 'a'),                                            (' asdf', 'sdfa', 'sdf')),
    (lineStartsWith('a'),                                                                   ('asdfs', 'a 89sdf a', 'a', 'sdfs\nasdfd'),                             (' asdf', 'sdf\nsdf', 'sdf\n a', 'sdfa', 'sdf')),
    (stringEndsWith('a'),                                                                   ('lklkjfda', 'sdf 8 a', 'a'),                                           ('asdfds', 'sd fd')),
    (lineEndsWith('a'),                                                                     ('lklkjfda', 'sdf 8 a', 'a', 'sdf\na', 'sdfse\nsdafsda', 'sdfa\nsdf'),  ('asdfds', 'sd fd')),
    (er.literal('test'),                                                                    ('test', ' sdfstestsdfs',),                                             ('te st',)),
    (underscore,                                                                            ('_',),                                                                 ('a test', 'test ', '\ntest\n', '\ntest', 'test\n')),
    (quote,                                                                                 ('"', "'", '`'),                                                        ('a test', 'test ', '\ntest\n', '\ntest', 'test\n')),
    (isExactly('test'),                                                                     ('test',),                                                              ('a test', 'test ', '\ntest\n', '\ntest', 'test\n')),
    (matchMax('a'),                                                                         ('aaa', 'a'),                                                           ('b',)),
    (matchMoreThan(3, 'a'),                                                                 ('aaaa', 'tesaaaaaat'),                                                 ('aaa',' aa')),
    (matchAtLeast(3, 'a'),                                                                  ('aaa', 'aaaa'),                                                        ('aa',)),
    (optional('a'),                                                                         ('', 'a', 'aa'),                                                        None),
    (either('a', 'b'),                                                                      ('a', 'b'),                                                             ('c',)),
    (either('aa', 'ba'),                                                                    ('aa', 'ba',),                                                          ('bb', 'a')),
    (whitespace,                                                                            (' ', '\t', '\t  ', '\n'),                                              ('dfsd',)),
    (whitechunk,                                                                            (' ', '\t', '\t  ', '\n'),                                              ('dfsd',)),
    (white,                                                                                 (' ', '\t', '\t  ', '\n'),                                              ('dfsd',)),
    (digit,                                                                                 ('6',),                                                                 ('_', '-', 'a')),
    (number,                                                                                ('6', '69'),                                                            ('-a', 'A')),
    (punctuation,                                                                           '@#$%^&*()'.split(),                                                    '12345678sdfsdf'.split()),
    (wordChar,                                                                              ('w',),                                                                 ('-',)),
    (hexDigit,                                                                              ('A', 'a', '0'),                                                        ('g', 'G')),
    (octDigit,                                                                              ('7',),                                                                 ('9', 'a', 'A', '8')),
    (chunk,                                                                                 ('wordssdf   asdf\n',),                                                 ('\n',)),
    (spaceOrTab,                                                                            (' ', '\t', ' \t  '),                                                   ('\n',)),
    (newLine,                                                                               ('\n',),                                                                ('\r',)),
    (carriageReturn,                                                                        ('\r',),                                                                ('\n',)),
    (tab,                                                                                   ('\t',),                                                                (' ',)),
    (space,                                                                                 (' ',),                                                                 ('\t',)),
    (quote,                                                                                 ('"', "'"),                                                             ('wer',)),
    (comma,                                                                                 (',',),                                                                 ('.', '`')),
    (period,                                                                                ('.',),                                                                 (',',)),
    (matchRange(3, 5, 'a'),                                                                 ('aaa', 'aaaa', 'a'*5, 'a'*6),                                          ('aa',)),
    (matchRange(3, 5, 'a', greedy=False)+'aa',                                              ('a'*5, 'a'*6),                                                         ('aa',)),
    (optional('a') + 'b',                                                                   ('b', 'ab','cb'),                                                       ('','c')),
    (optional('a', greedy=False) + 'b',                                                     ('b', 'ab','cb'),                                                       ('','c')),
    (atLeastOne('a'),                                                                       ('a','aa', 'a'*20),                                                     ('', 'b')),
    (atLeastOne('a', greedy=False),                                                         ('a','aa', 'a'*20),                                                     ('', 'b')),
    (atLeastNone('a'),                                                                      ('', 'a', 'a'*20, 'b'),                                                 None),
    ((optional('a') + 'b') * 3,                                                             ('abbb', 'bbb', 'ababab', 'bbab'),                                      ('', 'aaa', 'aa', 'a')),
    (word + whitechunk + group('func') + ':' + '()' + group(either('|', '7'), name='test'), ('wo  func:()|', 'wo  func:()7'),                                       None),
    (word + whitechunk + group('func') + ':' + group(anyof('8', '7'), 'test'),              ('wo  func:8', 'wo  func:7'),                                           None),
    (7 + anyof('abc') + lineEnd,                                                            ('7a', 'sdfsd7b', 'sdf\nsdf7b', 'sdf\nsdf7b\n'),                        ('7asdfsd', '7v')),
    (7 + anyof('abc') + stringEnd,                                                          ('7a', 'sdfsd7b'),                                                      ('7asdfsd', '7v', 'sdf\nsdf7bds', 'sdf\nsdf7bf\n')),
    (lineStart + 7 + anyof('abc'),                                                          ('7a', '7bsdfsd', '\n7a', '\n7bsdfsd'),                                 ('ds7asdfsd', '7v')),
    (stringStart + 7 + anyof('abc'),                                                        ('7a', '7bsdfsd'),                                                      ('ds7asdfsd', '7v', '\n7a', '\n7bsdfsd')),
    (+alpha,                                                                                ('a', 'asd'),                                                           ('89', '._78')),
    (+alphanum,                                                                             ('a', 'asd', '3sd', '88'),                                              ('.+',)),
    (raw(r'(<)?(\w+@\w+(?:\.\w+)+)(?(1)>|$)'),                                              ('<user@host.com>', 'user@host.com'),                                   ('user@host.com>',)), # https://docs.python.org/3/library/re.html says '<user@host.com' shouldn't match this pattern, but it's wrong...
    ('foo' + each(chunk + 'here' + chunk, chunk + anyOf('this', 'that') + chunk) + 'bar',   ('fooum here there that bar', 'foo that there here bar'),               None),
    # ('foo' + ((chunk + 'here' + chunk) & (chunk + anyOf('this', 'that') + chunk)) + 'bar',  ('fooum here there that bar', 'foo that there here bar'),               None),
    # ('foo' + ((chunk + 'here' + chunk) & (chunk + anyOf('this', 'that') + chunk) & (chunk + 'the' + chunk)) + 'bar',  ('fooum the here there that bar', 'foo that there thehere bar'), ('fooum here there that bar', 'foo that there here bar')),
    (opt(group('<')) + group(word + '@' + word + +('.' + word)) + ifExists(1, '>', string_end), ('<user@host.com>', 'user@host.com'),                               ('user@host.com>',)), # https://docs.python.org/3/library/re.html says '<user@host.com' shouldn't match this pattern, but it's wrong...
    # (,                                                                                    (,),                                                                    (,)),
    # (word_boundary + word_char[...,3] + wordBoundary,                                       ('yes', 'hey', 'sup', 'thi'),                                           ('none', 'no', 'foo3', '333', 'jar_')), # This does what it's supposed to do, but doesn't search correctly, as far as I understand it
    #TODO ('foo ' + anyExcept('bar') + ' baz',                                               ('foo thing baz', 'foo bax baz'),                                       ('foo bar baz',)),
    #TODO: (exactly('foo' + anyExcept('boo') + 'bar'),                                             ('foonotbar', 'foobar'),                                                ('fooboobar', 'boobar', 'fooboo')), # not sure where 'foo boo bar' goes
    #TODO: (exactly('foo' + anyExcept('boo', number) + 'bar'),                                     ('foo999bar', 'foo8bar'),                                               ('fooboobar','foonotbar', 'foo boo bar', 'foobar', 'boobar')),
    #TODO: (exactly('foo' + anyExcept('boo', match_amt(3, number)) + 'bar'),                       ('foo999bar', 'foo989bar'),                                             ('fooboobar','foonotbar', 'foo boo bar', 'foobar', 'boobar', 'foo8bar', 'foo98')),
    #TODO: (exactly(matchAtMost(3, digit)),                                                        ('444', '33', '1'),                                                     ('9999','9830')),
    #TODO: (exactly('foo' + anyExcept('888', match_amt(3, number)) + 'bar'),                       ('foo999bar', 'foo989bar'),                                             ('fooboobar','foonotbar', 'foo boo bar', 'foobar', 'foo888bar', 'boobar', 'foo8bar', 'foo98')),
    #TODO: (exactly('foo' + anyExcept('boo', word) + 'bar'),                                       ('foonotbar',),                                                         ('fooboobar', 'foo99bar', 'fooboo', 'boobar', 'foobar')),
    # TODO: punctuation
    # TODO: anyExcept(punctuation)
    # TODO: anyExcept(anyof(punctuation))
    # (,                                                                                    (,),                                                                    (,)),
    # TODO:
    # (raw(r"[ABC]+(?=D).*$ <.*?>"),                                                          None,                                                                   None),
    # (raw(r"(?:Q)(Q) ^A*$"),                                                                  None,                                                                   None), # I'm not actually sure what this is supposed to do
    # (raw(r"(?=AB)C (?!CD)DC AB(?<=CD) AB(?<!CD)"),                                           None,                                                                   None), # also not sure how this is actually supposed to work
    # (matchRange(3, 5, 'a', possessive=True) + 'aa',                                       ('a'*7,),                                                               ('a'*6,)),
    # (optional('a', possessive=True) + 'b',                                                ('',),                                                                  ('',)),
    # (atLeastOne(possessive=True),                                                         ('',),                                                                  ('',)),
    # (atLeastNone(possessive=True),                                                        ('',),                                                                  ('',)),
    # verticalTab,                                                                          ('',),                                                                  ('',),
    # formFeed,                                                                             ('',),                                                                  ('',),
    # either('a', 'b'),                                                                     ('a', 'b'),                                                             None),
    # multiOptional,                                                                        ('',),                                                                  ('',),
    # anyBetween,                                                                           ('',),                                                                  ('',),
    # (unicode,                                                                             ('',),                                                                  ('',),
    # (word,                                                                                ('word',),                                                              ('33a',)), # Is this *supposed* to work?
)

# This goes ("regex pattern", "replacement regex", "base string", "what the base string should look like after substitution"),
replacements = (
    (digit,                         "*",        "123abc",   "***abc"),  # Replace digits with *
    (anyof('aeiou'),                "_",        "hello",    "h_ll_"),  # Replace vowels with _
    (digit,                         "#",        "a1b2c3",   "a#b#c#"),  # Replace digits with #
    (group(digit) + group(digit),   rgroup(2) + rgroup(1),  "12345", "21435"),  # Swap the first two digits
    (group(anyof('aeiou')),         rgroup(1) * 2,          "hello", "heelloo"),  # Duplicate vowels
    (group(number),                 "num:" + rgroup(1),     "abc123xyz456", "abcnum:123xyznum:456"),  # Prefix numbers with "num:"
    (group(word_char) * 2,          rgroup(1) + '-' + rgroup(2), "Python", "P-yt-ho-n"),  # Separate adjacent characters with -
    (group(+uppercase),             rgroup(1) * 2,          "HelloWorld", "HHelloWWorld"),  # Duplicate uppercase words
    (group(+not_word),              " ",        "a@b#c",    "a b c"),  # Replace non-word characters with space
    # ("(\\b\\w{3}\\b)", "[\\1]", "The cat sat on the mat", "The [cat] [sat] on the [mat]"),  # Enclose 3-letter words in square brackets
    (group(digit) + group(lowercase), rgroup(1) + '_' + rgroup(2), "1a2b3c", "1_a2_b3_c"),  # Add underscore between digits and lowercase letters
    (group(+not_whitespace),        f"<{rgroup(1)}>", "Hello World", "<Hello> <World>"),  # Enclose non-space sequences in angle brackets
    # ("(\\b\\w+\\b)", "\\U\\1", "python is fun", "PYTHON IS FUN"),  # Convert words to uppercase
    (group(digit, 'digit') + group(lowercase, 'letter'), rgroup('letter') + rgroup('digit'), "1a2b3c", "a1b2c3"),  # Swap digit and letter with named groups
    (group(anyof('aeiou'), 'vowel'), f"[{rgroup('vowel')}]", "hello", "h[e]ll[o]"),  # Enclose vowels in square brackets with named group
    # ("(?P<number>[0-9]+)", "num: \\g<number>", "abc123xyz456", "abcnum: 123xyznum: 456"),  # Prefix numbers with "num:" using named group
    # ("(?P<upper>[A-Z]+)", "\\g<upper>\\g<upper>", "HelloWorld", "HELLOHELLO"),  # Duplicate uppercase words with named group
    # ("(?P<word>\\w+)", "<\\g<word>>", "Python is great", "<Python> <is> <great>"),  # Enclose words in angle brackets with named group
    ('foo' + group(number, 'num') + 'bar', f"foo-{rgroup('num')}-bar", 'foo87bar', 'foo-87-bar'),
    # ("(?P<non_space>\\S+)", "<\\g<non_space>>", "Hello World", "<Hello> <World>"),  # Enclose non-space sequences in angle brackets with named group
    # ("(?P<word>\\b\\w+\\b)", "\\U\\g<word>", "python is cool", "PYTHON IS COOL"),  # Convert words to uppercase with named group
    (group(word + number) + ':' + ow + group(word), replace_group(1) + ' - ' + replace_group(2), 'test1:    thing', 'test1 - thing'),
    (group(word + number, 'a') + ':' + ow + group(word, 'b'), replace_group('a') + ' - ' + replace_group('b'), 'test1:    thing', 'test1 - thing'),
    (stringStart + '(' + group(chunk + optional(',' + chunk)) + ')' + chunk, '(' + '${' + rgroup(1) + '})', '(name, input) -> ezregex.EZRegex.EZRegex', '(${name, input})'),
)

def runTests(singletons=True, _invert=True, replacement=True, testMethod=False, internal=False, operators=True, strictness=20, dontIncludePassed=True, invertBackend='re_parser', invert_tries=1):
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
        assert str(word + UNICODE + stuff)    == r'(?u)\w+.+', fr"{word + UNICODE + stuff}    != (?u)\w+.+"

        a = word + ow
        b = stuff + UNICODE
        c = IGNORECASE + '9'
        assert a + b + c == word + ow + stuff + UNICODE + IGNORECASE + '9', f"{a + b + c} != {word + ow + stuff + UNICODE + IGNORECASE + '9'}"

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
                raise err.with_traceback(None)

        a = str(EZRegex(r'\s+'))
        b = str(EZRegex(raw(r'\s+')))
        c = r'\s+'
        d = str(raw(r'\s+'))
        # e = str(whitespace + matchMax)
        assert a == b == c == d, f'\na: {a}\n b: {b}\n c: {c}\n d: {d}\n e: {e}'
        assert (word + ow + anything + ':').test('word    d:', show=False)
        assert not (word + ow + anything + ':').test('word', show=False)
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
runTests(
    # These should remain on, for the GitHub automated tests
    singletons=True,
    _invert=True,
    replacement=True,
    operators=True,
    # These display for you to check that they look correct
    testMethod=False,
    internal=False,
    # Settings
    strictness=difficulty,
    invert_tries=101-difficulty,
    dontIncludePassed=True,
    invertBackend='re_parser',
)
