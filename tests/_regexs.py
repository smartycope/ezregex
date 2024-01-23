
import re
from inspect import currentframe, getframeinfo

from rich import print as rprint
from rich.table import Table
from rich.text import Text

import ezregex.python as er
from ezregex.python import *
from ezregex.invert import *

import random

from _regexs import *


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
