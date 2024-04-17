import json
import string
import traceback
from random import choice, choices, randint
from re import search
from sys import version_info
from typing import Literal, Union
from pathlib import Path
from ezregex import *

if version_info.minor <= 10:
    from re import sre_parse as sre  # type: ignore
else:
    from re import _parser as sre  # type: ignore

# So I can debug this function directly
if __name__ != '__main__':
    from .invert_old import invertRegex

with open(Path(__file__).parent / 'assets' / 'sorted_words.json') as f:
    words = json.load(f).keys()

# Don't use string.whitespace, because we don't want to use weird difficult to print characters.
# We want the replacement to be readable.
_whitespace   = ' '
_everything   = string.digits + string.ascii_letters + string.punctuation + _whitespace + '_'

def _randWord(length=None, word='lookup'):
    if length is None:
        length = randint(3, 9)

    if word == 'random':
        return ''.join(choices(string.ascii_letters, k=length))

    elif word == 'lookup':
        try:
            return choice(words[length])
        except KeyError:
            return _randWord(length, word='random')

    elif word is None:
        return 'word'

    else:
        raise ValueError(f"invalid parameter given for word {word}. Accepted values are either random, lookup, or None")

def _randNumber(length:int, random=False) -> str:
    if random:
        return str(randint(0, 10**length))
    else:
        return ''.join(map(lambda i: str(i)[-1], range(1, length+1)))

def invert(
    expr:Union[str, 'EZRegex'],
    words:Literal['lookup', 'random']='lookup',
    randomNumbers=False,
    alot=8,
    tries:int=10,
    backend:Literal['re_parser', 'regex', 'xeger', 'sre_yield']='re_parser',
    _verbose=False,
    # Here for recursion; not to be used
    _untried=['re_parser', 'regex', 'xeger', 'sre_yield'],
    _tried=...,
) -> str:
    """ "Inverts" a regular expression by returning an example of something which is guaruanteed to
        match the passed expression.
        NOTE: This only works on valid Python regular expressions (it will probably mostly work for
            other dialects, but is not guarenteed.)
        expr: The regular expression to invert. Can be a string, or a EZRegex expression
        words: Controls how works are handled. If `random`, words are made of random letters. If `lookup`,
            it looks up valid english words and inserts them to make it more readable.
        randomNumbers: controls whether all numbers are 12345... to a desired length, or if they're
            just random numbers (again, for readability)
        alot: When given a choice of how many characters to put someone, it inserts a random integer
            between 1 and `alot`.
        tries: Controls how many times to try to invert the expression before giving up. This is effective,
            because there is an element of randomness involved in inverting the regex given.
        backend: One of ('re_parser', 'regex', 'xeger', 'sre_yield').
            `re_parser` is the default, it uses the build-in parser in the re package to create an AST
                of the regex
            `regex` uses regular expressions to parse regular expressions, which is as gross as it sounds.
                It's slightly buggy, but mostly works.
            `xeger` imports the `xeger` pacakge and uses it instead. Xeger inverts work, but are less
                readable. Must have the `xeger` package installed.
            `sre_yield` imports the `sre_yield` package and uses it instead. I don't think this works
                right now, and may be significantly slower.
    """
    expr = str(expr)
    if _tried is Ellipsis:
        _tried = tries

    # If we get an error in the actual inversion part, just handle it as though
    # we generated a bad string that doesn't match, and continue recusing
    try:
        match backend:
            case 'xeger':
                from xeger import Xeger  # type: ignore
                rtn = Xeger().xeger(expr)
            case 'regex':
                # Tries already gets implemented in this function
                try:
                    rtn = invertRegex(expr, 1)
                except NotImplementedError:
                    # Handle the error ourselves
                    rtn = None
            case 'sre_yield':
                import sre_yield  # type: ignore
                for i in sre_yield.AllStrings(expr):
                    rtn = i
            case 're_parser':
                groups = {}
                def handle(pattern, amt=1, opposite=False):
                    if _verbose:
                        print(f'Handling {pattern} * {amt}')
                    s = ''
                    for op, args in pattern:
                        if not opposite:
                            match op:
                                case sre.LITERAL:
                                    s += chr(args) * amt
                                case sre.NOT_LITERAL:
                                    almost_everything = list(_everything)
                                    if chr(args) in almost_everything:
                                        almost_everything.remove(chr(args))
                                    # If it's not in there, great!
                                    s += choice(almost_everything) * amt
                                case sre.RANGE:
                                    start, end = args
                                    s += chr(randint(start, end))
                                case sre.MAX_REPEAT | sre.MIN_REPEAT:
                                    min, max, sub = args
                                    if max is None or max is sre.MAXREPEAT:
                                        max = randint(min, alot)
                                    try:
                                        # If we know we're getting word chars, make a word of it
                                        if type(sub[0][1][0]) is not int and sub[0][1][0][1] in (sre.CATEGORY_WORD, sre.CATEGORY_UNI_WORD, sre.CATEGORY_LOC_WORD):
                                            if _verbose: print('Getting a random word')
                                            s += _randWord(word=words)
                                        elif type(sub[0][1][0]) is not int and sub[0][1][0][1] in (sre.CATEGORY_DIGIT, sre.CATEGORY_UNI_DIGIT):
                                            if _verbose: print('Getting whole number')
                                            s += _randNumber(randint(1, alot), random=randomNumbers)
                                        else:
                                            s += handle(sub, randint(min, max) * amt)
                                    except Exception as err:
                                        if _verbose:
                                            print(err)
                                            print(traceback.format_exc())

                                        s += handle(sub, randint(min, max) * amt)
                                case sre.ANY:
                                    for _ in range(amt):
                                        s += choice(_everything)
                                case sre.ASSERT:
                                    type_, sub = args
                                    if type_ == 1: # ifProcededBy
                                        s = s + handle(sub, amt)
                                    elif type_ == -1: # ifPrecededBy
                                        s += handle(sub, amt)
                                    else:
                                        s += handle(sub, amt)
                                case sre.ASSERT_NOT:
                                    type_, sub = args
                                    if type_ == 1: # ifNotProcededBy
                                        # almost_everything = list(_everything)
                                        # if chr(args) in almost_everything:
                                        #     almost_everything.remove(chr(args))
                                        # # If it's not in there, great!
                                        # s += choice(almost_everything) * amt
                                        s += handle(sub, amt, opposite=True)
                                    if type_ == -1: # ifNotPrecededBy
                                        s = s + handle(sub, amt, opposite=True)
                                    # If it needs to be followed by that sequence, simply add that sequence
                                    else:
                                        s += handle(sub, amt, opposite=True)
                                        # s += handle(sub, amt)
                                case sre.CATEGORY:
                                    for _ in range(amt):
                                        match args:
                                            case sre.CATEGORY_DIGIT | sre.CATEGORY_UNI_DIGIT:
                                                s += str(randint(0, 10))
                                            case sre.CATEGORY_LINEBREAK | sre.CATEGORY_UNI_LINEBREAK:
                                                s += '\n'
                                            case sre.CATEGORY_NOT_DIGIT | sre.CATEGORY_UNI_NOT_DIGIT:
                                                s += choice(string.ascii_letters + string.punctuation + _whitespace)
                                            case sre.CATEGORY_NOT_LINEBREAK | sre.CATEGORY_UNI_NOT_LINEBREAK:
                                                s += choice(_everything)
                                            case sre.CATEGORY_NOT_SPACE | sre.CATEGORY_UNI_NOT_SPACE:
                                                s += choice(string.punctuation + string.ascii_letters + string.digits)
                                            case sre.CATEGORY_NOT_WORD | sre.CATEGORY_UNI_NOT_WORD | sre.CATEGORY_LOC_NOT_WORD:
                                                s += choice(string.punctuation + _whitespace)
                                            case sre.CATEGORY_SPACE | sre.CATEGORY_UNI_SPACE:
                                                s += ' '
                                            case sre.CATEGORY_WORD | sre.CATEGORY_UNI_WORD | sre.CATEGORY_LOC_WORD:
                                                s += choice(string.ascii_letters + '_')
                                            case _:
                                                raise NotImplementedError(f'Unknown category given: {args}')
                                case sre.IN:
                                    # If this is a pattern like [^abc]
                                    if args[0][0] is sre.NEGATE:
                                        # Handle all the args except the negate flag and remove it from the options
                                        otherthan = handle(args[1:])
                                        almost_everything = list(_everything)
                                        for i in otherthan:
                                            if i in almost_everything:
                                                almost_everything.remove(i)
                                        s += choice(almost_everything)
                                    else:
                                        s += handle([choice(args)], amt)
                                case sre.SUBPATTERN: # This handles groups
                                    group, num, num2, sub = args
                                    sub_pattern = handle(sub) * amt
                                    groups[group] = sub_pattern
                                    s += sub_pattern
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
                                    elif args is sre.AT_BOUNDARY:
                                        if len(s) and s[-1] in string.digits + string.ascii_letters + '_':
                                            s += choice(string.punctuation + _whitespace)
                                        else:
                                            s += choice(string.digits + string.ascii_letters + '_')
                                    else:
                                        raise NotImplementedError(f'Unknown parameter[s] given for AT op: {args}')
                                case sre.BRANCH:
                                    something, branches = args
                                    s += handle(choice(branches), amt)
                                case sre.NEGATE:
                                    s += handle(args, amt, opposite=True)
                                case sre.GROUPREF:
                                    s += groups[args]
                                case sre.GROUPREF_EXISTS:
                                    # TODO: This often requires multiple tries to get right
                                    group, trueSub, falseSub = args
                                    s += handle(trueSub if group in groups else falseSub, amt)
                                case _:
                                    raise NotImplementedError(f'Unknown op {op} given with args {args}')
                        else:
                            match op:
                                case sre.LITERAL:
                                    almost_everything = list(_everything)
                                    if chr(args) in almost_everything:
                                        almost_everything.remove(chr(args))
                                    # If it's not in there, great!
                                    s += choice(almost_everything) * amt
                                case sre.NOT_LITERAL:
                                    s += chr(args) * amt
                                case sre.RANGE:
                                    start, end = args
                                    almost_everything = set(_everything)
                                    almost_everything.difference(map(chr, range(start, end)))
                                    s += choice(list(almost_everything))
                                case sre.MAX_REPEAT | sre.MIN_REPEAT:
                                    min, max, sub = args
                                    # Adding something that wouldn't match at all is always an option
                                    options = [handle(sub, amt, opposite=True)]
                                    # If a max is specified, then it can't match more than that many
                                    if max is not None and max is not sre.MAXREPEAT:
                                        options.append(handle(sub, amt * (max + randint(1, alot))))
                                    # If there's a min (meaning its more than 0), then it can't match
                                    # less than that many
                                    if min >= 1:
                                        # TODO: Potential Error: This doesn't take into account the current amt.
                                        options.append(handle(sub, randint(0, min-1)))
                                    s += choice(options)
                                case sre.ANY:
                                    # TODO: I think this will fail if given [^.\\n] (or anyExcept(literallyAnything)),
                                    # but also, how DO you handle that?
                                    for _ in range(amt):
                                        # I guess?
                                        s += '\n'
                                case sre.ASSERT:
                                    # I don't think conditionals are allowed inside a not assert (I think)
                                    type_, sub = args
                                    s += handle(sub, amt, opposite=True)
                                case sre.ASSERT_NOT:
                                    type_, sub = args
                                    # I *think* this will work?...
                                    s += handle(sub)
                                case sre.CATEGORY:
                                    for _ in range(amt):
                                        match args:
                                            case sre.CATEGORY_DIGIT | sre.CATEGORY_UNI_DIGIT:
                                                s += choice(string.ascii_letters + string.punctuation + _whitespace)
                                            case sre.CATEGORY_LINEBREAK | sre.CATEGORY_UNI_LINEBREAK:
                                                s += choice(_everything)
                                            case sre.CATEGORY_NOT_DIGIT | sre.CATEGORY_UNI_NOT_DIGIT:
                                                s += choice(string.digits)
                                            case sre.CATEGORY_NOT_LINEBREAK | sre.CATEGORY_UNI_NOT_LINEBREAK:
                                                s += '\n'
                                            case sre.CATEGORY_NOT_SPACE | sre.CATEGORY_UNI_NOT_SPACE:
                                                s += ' '
                                            case sre.CATEGORY_NOT_WORD | sre.CATEGORY_UNI_NOT_WORD | sre.CATEGORY_LOC_NOT_WORD:
                                                s += choice(string.ascii_letters + '_')
                                            case sre.CATEGORY_SPACE | sre.CATEGORY_UNI_SPACE:
                                                s += choice(string.punctuation + string.ascii_letters + string.digits)
                                            case sre.CATEGORY_WORD | sre.CATEGORY_UNI_WORD | sre.CATEGORY_LOC_WORD:
                                                s += choice(string.punctuation + _whitespace)
                                            case _:
                                                raise NotImplementedError(f'Unknown category given: {args}')
                                case sre.IN:
                                    # If this is a pattern like [^abc]
                                    if args[0][0] is not sre.NEGATE:
                                        # Handle all the args except the negate flag and remove it from the options
                                        otherthan = handle(args[1:])
                                        almost_everything = list(_everything)
                                        for i in otherthan:
                                            if i in almost_everything:
                                                almost_everything.remove(i)
                                        s += choice(almost_everything)
                                    else:
                                        s += handle([choice(args)], amt)
                                case sre.SUBPATTERN:
                                    idk, num, num2, sub = args
                                    s += handle(sub, opposite=True) * randint(0, amt)
                                case None: #sre.AT: # I don't know how to handle this
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
                                    elif args is sre.AT_BOUNDARY:
                                        if len(s) and s[-1] in string.digits + string.ascii_letters + '_':
                                            s += choice(string.punctuation + _whitespace)
                                        else:
                                            s += choice(string.digits + string.ascii_letters + '_')
                                    else:
                                        raise NotImplementedError(f'Unknown parameter[s] given for AT op: {args}')
                                case sre.BRANCH:
                                    something, branches = args
                                    s += handle(choice(branches), amt, opposite=True)
                                case sre.NEGATE:
                                    s += handle(args, amt)
                                case sre.GROUPREF:
                                    add = groups[args]
                                    while add == groups[args]:
                                        add = _randWord(word=words)
                                    s += add
                                case sre.GROUPREF_EXISTS:
                                    group, trueSub, falseSub = args
                                    s += handle(trueSub if group in groups else falseSub, amt, opposite=True)
                                case _:
                                    raise NotImplementedError(f'Unknown opposite op {op} given with args {args}')
                    return s

                rtn = handle(sre.parse(expr))
    except:
        rtn = None
    # I don't know why copying here is necissary. Do parameters act like globals?
    _untried = _untried.copy()
    try:
        _untried.remove(backend)
    # If we get a ValueError here, it just means that we're retrying the current backend
    # We can't just remove the _untried parameter in the recuse call in the else
    # statement below, because then it causes an infinite loop, instead of trying all
    # the options. This is better.
    except ValueError: pass

    # Try the current backend `tries` times
    if rtn is not None and search(expr, rtn):
        return rtn
    # If we're out of tries, switch backends
    elif tries < 0:
        # If we have options we haven't tried yet
        if len(_untried):
            # # tryNext = _untried.pop(0)
            # The next recursion will remove it for us
            tryNext = _untried[0]
            if _verbose:
                print(f'Not found using {backend}, trying {tryNext}')
            return invert(expr, words, randomNumbers, alot, _tried, tryNext, _verbose, _untried) # type: ignore
        # If we've tried everything, go to the error outside the if statement
    # If we're here, we generated a bad string, but we have more tries
    else:
        if _verbose:
            print(f'Not found using {backend}, retrying')

        return invert(expr, words, randomNumbers, alot, tries, backend, _verbose, _untried, _tried-1) # type: ignore

    raise NotImplementedError(f"Failed to invert pattern `{expr}`. Likely, bad regex was given. "
        "Otherwise, there\'s a bug in the invert function. You can submit a bug report to "
        "smartycope@gmail.com, and include the regex you used to get this error. (Failed expr: "
        f"was `{rtn}`)")
    return rtn


if __name__ == '__main__':
    pass
    # print(invert(r'D(?=AB)C'))  # ASSERT,      1, ifProcededBy
    # print(invert(r'D(?!AB)C'))  # ASSERT_NOT,  1, ifNotProcededBy
    # print(invert(r'C(?<=AB)D', _verbose=True)) # ASSERT,     -1, ifPrecededBy
    # print(invert(r'C(?<!AB)D'))   # ASSERT_NOT, -1, ifNotPrecededBy

    # print(invert(r'C(?=AB)'))  # ASSERT,      1, ifProcededBy
    # print(invert(r'C(?!AB)'))  # ASSERT_NOT,  1, ifNotProcededBy
    # print(invert(r'(?<=AB)C')) # ASSERT,     -1, ifPrecededBye
    # print(invert(r'(?<!AB)C'))   # ASSERT_NOT, -1, ifNotPrecededBy

    # print(invert(r'(?=AB)(?!CD)DC AB(?<=CD) AB(?<!CD)'))

    # print(invert(r'[ABC]+(?=D).*$ <.*?>'))

    # print(invert(r'\w+test\d+', _verbose=True))
