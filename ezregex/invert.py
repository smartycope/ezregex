__version__ = '2.2.0'

import json
import string
from pathlib import Path
from random import choice, choices, randint, random, seed as set_seed
from re import search
from sys import version_info
from typing import Literal, Union
import logging


if version_info.minor <= 10:
    from re import sre_parse as sre  # type: ignore
else:
    from re import _parser as sre  # type: ignore

# So I can debug this file directly
if __name__ == '__main__':
    from ezregex.invert_old import invertRegex
    from ezregex import *
else:
    from . import *
    from .invert_old import invertRegex


with open(Path(__file__).parent / 'assets' / 'common_sorted_words.json') as f:
    words = json.load(f)


def invert(
    expr:Union[str, 'EZRegex'],
    tries:int=10,
    backend:Literal['re_parser', 'regex', 'xeger', 'sre_yield']=...,
    words:Literal['lookup', 'random']|None='lookup',
    random_numbers=False,
    alot=8,
) -> str:
    """ "Inverts" a regular expression by returning an example of something which is guaruanteed to
        match the passed expression.
        NOTE: This only works on valid Python regular expressions.

        Args:
            expr: The regular expression to invert. Can be a string, or a EZRegex expression
            words: Controls how works are handled. If `random`, words are made of random letters. If `lookup`,
                it looks up valid english words and inserts them to make it more readable.
            random_numbers: controls whether all numbers are 12345... to a desired length, or if they're
                just random numbers (again, for readability)
            self.alot: When given a choice of how many characters to put someone, it inserts a random integer
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
    return Inverter(expr,tries, backend, words, random_numbers, alot).invert()


class Inverter:
    def __init__(self,
        expr:Union[str, 'EZRegex'],
        tries:int=10,
        backend:Literal['re_parser', 'regex', 'xeger', 'sre_yield']=...,
        words:Literal['lookup', 'random']|None='lookup',
        random_numbers=False,
        alot=8,
    ):
        self.expr = str(expr)
        self.words = words
        self.random_numbers = random_numbers
        self.alot = alot
        self.tries = tries
        self.backend = backend
        self._attempts = {
            're_parser': 0,
            'regex': 0,
            'xeger': 0,
            'sre_yield': 0,
        }
        # Don't use string.whitespace, because we don't want to use weird difficult to print characters.
        # We want the replacement to be readable.
        self._whitespace = ' '
        self._everything = string.digits + string.ascii_letters + string.punctuation + self._whitespace + '_'
        self._seed = random()

        try: from xeger import Xeger  # type: ignore
        except ImportError: self._xeger = False
        else: self._xeger = True

        try: import sre_yield  # type: ignore
        except ImportError: self._sre_yield = False
        else: self._sre_yield = True

        if backend == 'xeger' and not self._xeger:
            raise ImportError(f'Requested backend `xeger` not available. Try installing it by running `pip install xeger`')

        if backend == 'sre_yield' and not self._sre_yield:
            raise ImportError(f'Requested backend `sre_yield` not available. Try installing it by running `pip install sre_yield`')

    def _randWord(self, length=..., word=...) -> str:
        self.seed += 1

        if word is Ellipsis:
            word = self.words
        if length is Ellipsis:
            length = randint(3, self.alot)

        if word == 'random':
            return ''.join(choices(string.ascii_letters, k=length))

        elif word == 'lookup':
            try:
                # The keys are strings, not ints, and I don't feel like fixing it
                return choice(words[str(length)])
            except KeyError:
                return self._randWord(length, word='random')

        elif word is None:
            return 'word'

        else:
            raise ValueError(f"invalid parameter given for word {word}. Accepted values are either random, lookup, or None")

    def _randNumber(self, length=...) -> str:
        self.seed += 1

        if length is Ellipsis:
            length = randint(2, self.alot)

        if self.random_numbers:
            return str(randint(0, 10**length))
        else:
            return ''.join(map(lambda i: str(i)[-1], range(1, length+1)))

    def _handle(self, pattern, amt=1, opposite=False):
        # I don't thiiiink anything uses multiple random calls, for now anyway
        if amt == 0:
            return ''

        # To make it deterministic, but still random
        self.seed += 1
        s = ''
        for op, args in pattern:
            if not opposite:
                match op:
                    case sre.LITERAL:
                        logging.debug(f'Literal: {chr(args)} * {amt}')
                        s += chr(args) * amt
                    case sre.NOT_LITERAL:
                        almost_everything = list(self._everything)
                        if chr(args) in almost_everything:
                            almost_everything.remove(chr(args))
                        # If it's not in there, great!
                        s += choice(almost_everything) * amt
                    case sre.RANGE:
                        start, end = args
                        s += chr(randint(start, end))
                    case sre.MIN_REPEAT: # optional, I believe
                        min, max, sub = args
                        if max is None or max is sre.MAXREPEAT:
                            max = randint(min, self.alot)
                        s += self._handle(sub, randint(min, max))
                    case sre.MAX_REPEAT:
                        min, max, sub = args
                        if max is None or max is sre.MAXREPEAT:
                            max = randint(min, self.alot)

                        _amt = (randint(min, max) * amt)
                        # Words and numbers look like this:
                        # [(IN, [(CATEGORY, CATEGORY_DIGIT)])]
                        if sub[0][0] == sre.IN:
                            # If we know we're getting word chars, make a word of it
                            if sub[0][1][0][1] in (sre.CATEGORY_WORD, sre.CATEGORY_UNI_WORD, sre.CATEGORY_LOC_WORD):
                                logging.debug('Getting a random word')
                                s += self._randWord(_amt)
                            # If we know we're getting digit chars, make a number of it
                            elif sub[0][1][0][1] in (sre.CATEGORY_DIGIT, sre.CATEGORY_UNI_DIGIT):
                                logging.debug('Getting whole number' )
                                s += self._randNumber(_amt)
                            else:
                                s += self._handle(sub) * _amt
                        else:
                            s += self._handle(sub) * _amt
                    case sre.ANY:
                        for _ in range(amt):
                            s += choice(self._everything)
                    case sre.ASSERT:
                        type_, sub = args
                        if type_ == 1: # ifProcededBy
                            s = s + self._handle(sub, amt)
                        elif type_ == -1: # ifPrecededBy
                            s += self._handle(sub, amt)
                        else:
                            s += self._handle(sub, amt)
                    case sre.ASSERT_NOT:
                        type_, sub = args
                        if type_ == 1: # ifNotProcededBy
                            # almost_everything = list(self._everything)
                            # if chr(args) in almost_everything:
                            #     almost_everything.remove(chr(args))
                            # # If it's not in there, great!
                            # s += choice(almost_everything) * amt
                            s += self._handle(sub, amt, opposite=True)
                        if type_ == -1: # ifNotPrecededBy
                            s = s + self._handle(sub, amt, opposite=True)
                        # If it needs to be followed by that sequence, simply add that sequence
                        else:
                            s += self._handle(sub, amt, opposite=True)
                            # s += self._handle(sub, amt)
                    case sre.CATEGORY:
                        for _ in range(amt):
                            match args:
                                case sre.CATEGORY_DIGIT | sre.CATEGORY_UNI_DIGIT:
                                    s += str(randint(0, 10))
                                case sre.CATEGORY_LINEBREAK | sre.CATEGORY_UNI_LINEBREAK:
                                    s += '\n'
                                case sre.CATEGORY_NOT_DIGIT | sre.CATEGORY_UNI_NOT_DIGIT:
                                    s += choice(string.ascii_letters + string.punctuation + self._whitespace)
                                case sre.CATEGORY_NOT_LINEBREAK | sre.CATEGORY_UNI_NOT_LINEBREAK:
                                    s += choice(self._everything)
                                case sre.CATEGORY_NOT_SPACE | sre.CATEGORY_UNI_NOT_SPACE:
                                    s += choice(string.punctuation + string.ascii_letters + string.digits)
                                case sre.CATEGORY_NOT_WORD | sre.CATEGORY_UNI_NOT_WORD | sre.CATEGORY_LOC_NOT_WORD:
                                    s += choice(string.punctuation + self._whitespace)
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
                            otherthan = self._handle(args[1:])
                            almost_everything = list(self._everything)
                            for i in otherthan:
                                if i in almost_everything:
                                    almost_everything.remove(i)
                            s += choice(almost_everything)
                        else:
                            s += self._handle([choice(args)], amt)
                    case sre.SUBPATTERN: # This handles groups
                        group, num, num2, sub = args
                        sub_pattern = self._handle(sub) * amt
                        self.groups[group] = sub_pattern
                        s += sub_pattern
                        logging.debug(f'group: {group}, num: {num}, num2: {num2} -> s: {s} -- sub: {sub}')
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
                                s += choice(string.punctuation + self._whitespace)
                            else:
                                s += choice(string.digits + string.ascii_letters + '_')
                        # \B, I believe
                        elif args is sre.AT_NON_BOUNDARY:
                            # This works... I'm not entirely sure why... I'm not gonna touch it.
                            if len(s) and s[-1] not in string.digits + string.ascii_letters + '_':
                                s += choice(string.digits + string.ascii_letters + '_')
                            else:
                                s += choice(string.punctuation + self._whitespace)
                        else:
                            raise NotImplementedError(f'Unknown parameter[s] given for AT op: {args}')
                    case sre.BRANCH:
                        something, branches = args
                        s += self._handle(choice(branches), amt)
                    case sre.NEGATE:
                        s += self._handle(args, amt, opposite=True)
                    case sre.GROUPREF:
                        s += self.groups[args]
                    case sre.GROUPREF_EXISTS:
                        # TODO: This often requires multiple tries to get right
                        group, trueSub, falseSub = args
                        s += self._handle(trueSub if group in self.groups else falseSub, amt)
                    case _:
                        raise NotImplementedError(f'Unknown op {op} given with args {args}')
            else:
                match op:
                    case sre.LITERAL:
                        almost_everything = list(self._everything)
                        if chr(args) in almost_everything:
                            almost_everything.remove(chr(args))
                        # If it's not in there, great!
                        s += choice(almost_everything) * amt
                    case sre.NOT_LITERAL:
                        s += chr(args) * amt
                    case sre.RANGE:
                        start, end = args
                        almost_everything = set(self._everything)
                        almost_everything.difference(map(chr, range(start, end)))
                        s += choice(list(almost_everything))
                    case sre.MAX_REPEAT | sre.MIN_REPEAT:
                        min, max, sub = args
                        # Adding something that wouldn't match at all is always an option
                        options = [self._handle(sub, amt, opposite=True)]
                        # If a max is specified, then it can't match more than that many
                        if max is not None and max is not sre.MAXREPEAT:
                            options.append(self._handle(sub, amt * (max + randint(1, self.alot))))
                        # If there's a min (meaning its more than 0), then it can't match
                        # less than that many
                        if min >= 1:
                            # TODO: Potential Error: This doesn't take into account the current amt.
                            options.append(self._handle(sub, randint(0, min-1)))
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
                        s += self._handle(sub, amt, opposite=True)
                    case sre.ASSERT_NOT:
                        type_, sub = args
                        # I *think* this will work?...
                        s += self._handle(sub)
                    case sre.CATEGORY:
                        for _ in range(amt):
                            match args:
                                case sre.CATEGORY_DIGIT | sre.CATEGORY_UNI_DIGIT:
                                    s += choice(string.ascii_letters + string.punctuation + self._whitespace)
                                case sre.CATEGORY_LINEBREAK | sre.CATEGORY_UNI_LINEBREAK:
                                    s += choice(self._everything)
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
                                    s += choice(string.punctuation + self._whitespace)
                                case _:
                                    raise NotImplementedError(f'Unknown category given: {args}')
                    case sre.IN:
                        # If this is a pattern like [^abc]
                        if args[0][0] is not sre.NEGATE:
                            # Handle all the args except the negate flag and remove it from the options
                            otherthan = self._handle(args[1:])
                            almost_everything = list(self._everything)
                            for i in otherthan:
                                if i in almost_everything:
                                    almost_everything.remove(i)
                            s += choice(almost_everything)
                        else:
                            s += self._handle([choice(args)], amt)
                    case sre.SUBPATTERN:
                        idk, num, num2, sub = args
                        s += self._handle(sub, opposite=True) * randint(0, amt)
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
                                s += choice(string.punctuation + self._whitespace)
                            else:
                                s += choice(string.digits + string.ascii_letters + '_')
                        else:
                            raise NotImplementedError(f'Unknown parameter[s] given for AT op: {args}')
                    case sre.BRANCH:
                        something, branches = args
                        s += self._handle(choice(branches), amt, opposite=True)
                    case sre.NEGATE:
                        s += self._handle(args, amt)
                    case sre.GROUPREF:
                        add = self.groups[args]
                        while add == self.groups[args]:
                            add = self._randWord()
                        s += add
                    case sre.GROUPREF_EXISTS:
                        group, trueSub, falseSub = args
                        s += self._handle(trueSub if group in self.groups else falseSub, amt, opposite=True)
                    case _:
                        raise NotImplementedError(f'Unknown opposite op {op} given with args {args}')
        return s


    def invert_re_parser(self) -> str | None:
        self._attempts['re_parser'] += 1
        self.seed = random()
        logging.debug(f're_parser attempt #{self._attempts["re_parser"]} with seed {self._seed}...')
        self.groups = {}
        return self._handle(sre.parse(self.expr))

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        self._seed = value
        set_seed(self._seed)

    def invert_regex(self) -> str | None:
        self._attempts['regex'] += 1
        logging.debug(f'regex attempt #{self._attempts["regex"]}...')
        try:
            rtn = invertRegex(self.expr, 1)
        except NotImplementedError:
            pass

    def invert_xeger(self) -> str | None:
        self._attempts['xeger'] += 1
        logging.debug(f'xeger attempt #{self._attempts["xeger"]}...')
        if self._xeger:
            from xeger import Xeger  # type: ignore
            return Xeger().xeger(self.expr)

    def invert_sre_yield(self) -> str | None:
        self._attempts['sre_yield'] += 1
        logging.debug(f'sre_yield attempt #{self._attempts["sre_yield"]}...')
        if self._sre_yield:
            import sre_yield  # type: ignore
            for i in sre_yield.AllStrings(self.expr):
                return i

    def invert(self) -> str:
        if self.backend is Ellipsis:
            # The old backend occasionally enters an infinite loop, and I don't care to fix it
            order = ('re_parser', 'sre_yield', 'xeger') # 'regex',
        else:
            order = [self.backend]
        for backend in order:
            while self._attempts[backend] <= self.tries:
                if (inverter := getattr(self, 'invert_' + backend)) is not None:
                    matching_pattern = inverter()
                    if search(self.expr, matching_pattern):
                        logging.info(f'Found using {backend}')
                        return matching_pattern
                    else:
                        if matching_pattern is not None:
                            logging.info(f'Successfully inverted pattern, but it was invalid: `{matching_pattern}`')
                        else:
                            logging.info('Failed to invert pattern')
                else:
                    logging.info(f'Invalid backend: {backend}')

        logging.info(f'Not found using {backend}')
        msg = (
            f"Failed to invert pattern `{self.expr}`. Likely, bad regex was given. "
            "If you think that's not the case, please submit a bug report to "
            "https://github.com/smartycope/ezregex/issues, and include the regex you used to get "
            f"this error, and this seed: {self._seed}. "
        )
        if not self._xeger or not self._sre_yield:
            msg += "You can also try installing the extra backends to see if those work:\n"
        if not self._xeger:
            msg += "\txeger (`pip install xeger`)\n"
        if not self._sre_yield:
            msg += "\tsre_yield (`pip install sre-yield`)"

        raise NotImplementedError(msg)


if __name__ == '__main__':
    # NOTE: this can be helpful for quick tests, but for serious bugfixes, there's a debugging_invert.ipynb in the tests/ folder
    logging.basicConfig(level=logging.DEBUG)
    # inv = Inverter(r'\w+\d+', verbose=False)
    # print(inv.invert())
    # print(invert(r'D(?=AB)C', verbose=True))  # ASSERT,      1, ifProcededBy
    # print(invert(r'D(?!AB)C'))  # ASSERT_NOT,  1, ifNotProcededBy
    # print(invert(r'C(?<=AB)D', _verbose=True)) # ASSERT,     -1, ifPrecededBy
    # print(invert(r'C(?<!AB)D'))   # ASSERT_NOT, -1, ifNotPrecededBy

    # print(invert(r'C(?=AB)'))  # ASSERT,      1, ifProcededBy
    # print(invert(r'C(?!AB)'))  # ASSERT_NOT,  1, ifNotProcededBy
    # print(invert(r'(?<=AB)C')) # ASSERT,     -1, ifPrecededBy
    # print(invert(r'(?<!AB)C'))   # ASSERT_NOT, -1, ifNotPrecededBy

    # print(invert(r'(?=AB)(?!CD)DC AB(?<=CD) AB(?<!CD)'))

    # print(invert(r'[ABC]+(?=D).*$ <.*?>'))
    # print(invert(r'(<)?(\w+@\w+(?:\.\w+)+)(?(1)>|$)'))
    # print(invert(r'(?:(<))?(\w+@\w+(?:\.\w+)+)(?(1)>|\Z)'))

    wc = whitechunk; nl = newline; place = lambda which: chunk.group(name=which+"City") + " " + uppercase.amt(2).group(name=which+"State"); supplier = chunk.group(name="Supplier"); SCAC = letter.amt(4).group(name="SCAC"); money = lambda col: "$" + nl + fullFloat.group(name=col); transit = digit.group(name="TransitTime"); regex = place("O") + wc + place("D") + wc + supplier + wc + SCAC + wc + money("RPM") + wc + money("MinCharge") + wc + transit

    these = (
    # r"[a-z0-9!\#\$%\&'\*\+/=\?\^_`\{\|\}\~\-]+",
    # r"[a-z0-9!\#\$%\&'\*\+/=\?\^_`\{\|\}\~\-]+",
    # r"\w+\d+",
    # r"(<)?(\w+@\w+(?:\.\w+)+)(?(1)>|$)",
    # r"(?P(?:(?:\w|-))+) (?:(?P[A-Za-z])(?:.|\w+) )?(?P\w+),.+",
    regex,
    # r"(?:df){3}",
    # r"(test)+",
    # r"(test){3}",
    # r'(?:(?:\'|\")){3}',
    # r'\w{3,5}',
    # r'(a??) a*? a{3,}? ab{4,7}? ',
    # r"(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*",
    # r"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*",
    # r"(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")",
    # r"(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])",
    )
    for i in these:
        print(invert(i, backend='re_parser'))
