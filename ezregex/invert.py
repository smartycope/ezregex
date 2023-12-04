from random import randint, choice, choices
# import sre_parse36 as sre
from re import _parser as sre
from rich import print
from .invert_old import invertRegex
from ezregex import *
from functools import partial
from random_word.services.local import Local
import json
from typing import Union, Literal

with open(Local().source) as f:
    words = json.load(f).keys()

# rtn = sre_parse36.parse("(?:foo (?:bar) | (?:baz))")
# regex = str(word + chunk + ow + ifFollowedBy(number) + 'thing')
# rtn = sre.parse(regex)

_digits       = '0123456789'
_letters      = 'abcdefghijklmnopqrstuvwxyz'
_letters     += _letters.upper()
_punctuation  = "./;=-&%$#@~"
_whitespace   = '  '
_everything   = _digits + _letters + _punctuation + _whitespace + '_'


def unsanitize(string):
    return re.sub(r'\\([' + re.escape(')([]{}+*$^-\\?| ,') + r'])', '\g<1>', string)

def randbool():
    return bool(randint(0, 1))

def _randWord(length, word='lookup'):
    if word == 'random':
        return ''.join(choices(_letters + '_', k=length))
    elif word == 'lookup':
        return choice(list(filter(lambda i: len(i) == 4, words)))
    elif word is None:
        return 'word'
    else:
        raise TypeError(f"invalid parameter given for word {word}. Accepted values are either random, lookup, or None")

def _randNumber(length, random=False):
    if random:
        return randint(0, 10**length)
    else:
        return ''.join(map(lambda i: str(i)[-1], range(1, length+1)))

def invert(
        expr:Union[str, 'EZRegexMember'],
        words:Literal['lookup', 'random', None]='lookup',
        randomNumbers=False,
        alot=6,
        tries:int=10,
        backend:Literal['sre_parse', 'regex', 'xeger', 'sre_yield']='sre_parse',
    ):
    expr = str(expr)

    match backend:
        case 'xeger':
            from xeger import Xeger
            return Xeger().xeger(expr)
        case 'regex':
            return invertRegex(expr, tries)
        case 'sre_yield':
            import sre_yield
            for i in sre_yield.AllStrings(expr):
                return i
        case 'sre_parse':
            def handle(pattern, amt=1):
                # print(f'Handling {pattern} * {amt}')
                s = ''
                for op, args in pattern:
                    match op:
                        case sre.LITERAL:
                            s += chr(args) * amt
                        case sre.RANGE:
                            start, end = args
                            s += chr(randint(start, end))
                        case sre.MAX_REPEAT | sre.MIN_REPEAT:
                            min, max, sub = args
                            # s += f'\n--- min: {min}, max: {max} ---\n'
                            if max is None or max is sre.MAXREPEAT:
                                max = randint(min, alot)
                            try:
                                # If we know we're getting word chars, make a word of it
                                if type(sub[0][1][0]) is not int and sub[0][1][0][1] in (sre.CATEGORY_WORD, sre.CATEGORY_UNI_WORD, sre.CATEGORY_LOC_WORD):
                                    s += _randWord(randint(1, alot), word=words)
                                elif type(sub[0][1][0]) is not int and sub[0][1][0][1] in (sre.CATEGORY_DIGIT, sre.CATEGORY_UNI_DIGIT):
                                    s += _randNumber(randint(1, alot), random=randomNumbers)
                                else:
                                    s += handle(sub, randint(min, max) * amt)
                            except:
                                s += handle(sub, randint(min, max) * amt)
                        # case sre.MIN_REPEAT:
                        #     min, max, sub = args
                        #     s += handle(sub, amt * randint(min, max))
                        case sre.ANY:
                            for _ in range(amt):
                                s += choice(_everything)
                        case sre.ASSERT:
                            num, sub = args
                            s += handle(sub, amt)
                        case sre.ASSERT_NOT:
                            num, sub = args
                            # If it needs to be followed by that sequence, simply add that sequence
                            s += handle(sub)
                        case sre.CATEGORY:
                            for _ in range(amt):
                                match args:
                                    case sre.CATEGORY_DIGIT | sre.CATEGORY_UNI_DIGIT:
                                        s += str(randint(0, 10))
                                    case sre.CATEGORY_LINEBREAK | sre.CATEGORY_UNI_LINEBREAK:
                                        s += '\n'
                                    case sre.CATEGORY_NOT_DIGIT | sre.CATEGORY_UNI_NOT_DIGIT:
                                        s += choice(_letters + _punctuation + _whitespace)
                                    case sre.CATEGORY_NOT_LINEBREAK | sre.CATEGORY_UNI_NOT_LINEBREAK:
                                        s += choice(_everything)
                                    case sre.CATEGORY_NOT_SPACE | sre.CATEGORY_UNI_NOT_SPACE:
                                        s += choice(_punctuation + _letters + _digits)
                                    case sre.CATEGORY_NOT_WORD | sre.CATEGORY_UNI_NOT_WORD | sre.CATEGORY_LOC_NOT_WORD:
                                        s += choice(_punctuation + _whitespace)
                                    case sre.CATEGORY_SPACE | sre.CATEGORY_UNI_SPACE:
                                        s += ' '
                                    case sre.CATEGORY_WORD | sre.CATEGORY_UNI_WORD | sre.CATEGORY_LOC_WORD:
                                        s += choice(_letters + '_')
                                    case _:
                                        s += f'\n--- Unknown catagory {args} ---\n'
                        case sre.IN:
                            # If this is a pattern like [^abc]
                            if args[0][0] is sre.NEGATE:
                                # Handle all the args except the negate flag and remove it from the options
                                otherthan = handle(args[1:])
                                if otherthan in _everything:
                                    s += choice(list(_everything).remove(otherthan))
                                else:
                                    s += choice(_everything)
                            else:
                                s += handle([choice(args)], amt)
                        case sre.SUBPATTERN:
                            idk, num, num2, sub = args
                            s += handle(sub)  * amt
                        case sre.AT:
                            if args is sre.AT_BEGINNING_STRING:
                                # Whatever comes next better be first
                                s = ''
                            elif args is sre.AT_END_STRING:
                                # Whatever comes next better be last
                                return s
                            elif args is sre.AT_BEGINNING:
                                s += '\n'
                            elif args is sre.AT_END:
                                s += '\n'
                            else:
                                raise NotImplementedError(f'Unknown parameter[s] given for AT op: {args}')
                        case sre.BRANCH:
                            something, branches = args
                            s += handle(choice(branches), amt)
                        case sre.NEGATE:
                            pass
                        case _:
                            raise NotImplementedError(f'Unknown op {op} given with args {args}')
                            # s += f'\n--- Unknonwn op {op} has args {args} ---\n'
                return s
            return handle(sre.parse(expr))
