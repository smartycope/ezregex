import re
from copy import copy
from dataclasses import dataclass
from random import choice, choices, randint
from warnings import warn


def unsanitize(string):
    return re.sub(r'\\([' + re.escape(')([]{}+*$^-\\?| ,') + r'])', '\g<1>', string)

def randbool():
    return bool(randint(0, 1))

def _randWord(randomlyGenerate=False):
    if randomlyGenerate:
        return ''.join(choices(_letters + '_', k=randint(1, _alot)))
    else:
        return 'word'

# Inverting helpers
_alot         = 6
_digits       = '0123456789'
_letters      = 'abcdefghijklmnopqrstuvwxyz'
_letters     += _letters.upper()
_punctuation  = "./;=-&%$#@~"
_whitespace   = '  '
_everything   = _digits + _letters + _punctuation + _whitespace + '_'

# notParens = matchMax(anyCharExcept('(', ')'))  # + ifNotPreceededBy(r'\\'))
# inner = atLeastNone(either('(' + optional('?:') + notParens + ')', notParens))
# prevThing = namedGroup('prev', anyof('(?:' + inner + ')', '(' + inner + ')', ifNotPreceededBy(r'\\') + anything))
prevThing = r'(?P<prev>(?:\(\?\:(?:(?:\((?:\?\:)?(?:[^\(\)])+\)|(?:[^\(\)])+))*\)|\((?:(?:\((?:\?\:)?(?:[^\(\)])+\)|(?:[^\(\)])+))*\)|(?<!\\).))'

tillCloseParen = r'(?P<stuff>.+)\)'

@dataclass
class _invertRegexes:
    flags        = re.compile(r"\A\(\?[aiLmsux]\)")
    word         = re.compile(r'\\w\+')
    s            = re.compile(r'\\s')
    digit        = re.compile(r'\\d')
    char         = re.compile(r'\\w')
    any          = re.compile(r'(?<!\\)\.')
    newline      = re.compile(r'\\n')
    carriage     = re.compile(r'\\r')
    tab          = re.compile(r'\\t')
    vert         = re.compile(r'\\v')
    f            = re.compile(r'\\f')
    stringStart  = re.compile(r'\\A')
    lineStart    = re.compile(r'\^')
    stringEnd    = re.compile(r'\\Z')
    lineEnd      = re.compile(r'\$')
    matchExactly = re.compile(r'\^(.+)\$')  # \^stuff\$
    # '[' + atLeastOne(namedGroup('start', char) + '-' + namedGroup('end', char)) + ']'
    anyBetween   = re.compile(r'\[(?:(?P<start>.)\-(?P<end>.))+\]')
    # '(' + namedGroup('stuff', chunk()) + '){' + namedGroup('amt', number()) + '}'
    matchExactAmt = re.compile(prevThing + r'\{(?P<amt>\d+)\}')  # (stuff){3}
    # '(' + namedGroup('stuff', chunk()) + '){' + namedGroup('min', number()) + ',' + optional(space()) + '}'
    matchMore = re.compile(prevThing + r'\{(?P<min>\d+),( )?\}')  # (stuff){3,}
    # optional  = re.compile(prevThing + r'\?(?![\:P\<\!])')  # (stuff)?
    optionalGreedy  = re.compile(prevThing + r'\?(?![\:P\<\!])')  # (stuff)?
    optionalNonGreedy  = re.compile(prevThing + r'\?\?(?![\:P\<\!])')  # (stuff)??
    atLeastNoneGreedy       = re.compile(prevThing + r'\*')  # (stuff)*
    atLeastNoneNonGreedy       = re.compile(prevThing + r'\*\?')  # (stuff)*?
    atLeastOneGreedy     = re.compile(fr'{prevThing}\+')  # (stuff)+
    atLeastOneNonGreedy     = re.compile(fr'{prevThing}\+\?')  # (stuff)+?
    # '(' + namedGroup('stuff', chunk()) + '){' + namedGroup('min', number()) + ',' + optional(space()) + namedGroup('max', number()) + '}'
    matchRangeGreedy = re.compile(prevThing + r'\{(?P<min>\d+),( )?(?P<max>\d+)\}')  # (stuff){3,4}
    matchRangeNonGreedy = re.compile(prevThing + r'\{(?P<min>\d+),( )?(?P<max>\d+)\}\?')  # (stuff){3,4}?
    # either('(?:', '(') + group(atLeast1(notParens, greedy=False)) + '|' + group(atLeast1(char, greedy=False)) + ')'
    either    = re.compile(r'(?:\(\?\:|\()((?:(?:[^\(\)](?<!\\))+)+?)\|(.+?)\)')  # (stuff|things)
    notWhitespace = re.compile(r'\\S')
    notDigit      = re.compile(r'\\D')
    notWord       = re.compile(r'\\W')
    # '[' + ifNotFollowedBy('^') + group(atLeastOne(anyCharExcept(','))) + ']'
    anyChars    = re.compile(r'\[(?!\^)((?:[^\,])+)\]')  # [st]
    anyChars2    = re.compile(r'\[(?!\^)((?:.(?:\,)?)+)\]')  # [s,t]
    # '[' + ifFollowedBy('^') + group(atLeastOne(char)) + ']'
    notAnyChars = re.compile(r'\[(?=\^)(.+)\]')  # [^s,t]
    # group(either(ifPrecededBy('(?:'), ifPrecededBy('(')) + matchMax(anyCharExcept(r'|\)')) + '|' + matchMax(anyCharExcept(r'|\)')) + optional('|') + ifFollowedBy(')'))
    anyOf = re.compile(r'((?:(?<=\(\?\:)|(?<=\())(?:.\|)+.(?=\)))')  # (stuff|things|otherThings)
    ifThing = re.compile(r'\(\?\=' + tillCloseParen)  # (?=stuff)
    ifNotThing       = re.compile(r'\(\?!' + tillCloseParen)  # (?!stuff)
    ifPrecededBy     = re.compile(r'\(\?\<\=' + tillCloseParen)
    ifNotPrecededBy  = re.compile(r'\(\?\<\!' + tillCloseParen)
    ifNotPrecededBy2 = re.compile(r'\(\?\!\=' + tillCloseParen)
    # '(?:' + group(matchMax(notAnyChars(')', '(', '?'))) + ')'
    passiveGroup     = re.compile(r'\(\?\:((?:[^\(\?])+)\)')  # (?:stuff)
    group = re.compile(r'\((?!\?)([^\)\(\?]+)\)')  # (stuff)
    namedGroup = re.compile(r'\(\?P\<(?P<name>\w+)\>(?P<stuff>.+)\)')  # (P?<name>stuff)


def invertRegex(regex:str, tries=10) -> str:
    """ 'Inverts' a regex expression.
        Gives an example of something that would match the given regex
        If tries is positive, it's guarenteed to return an expression that
        correctly matches the given expression, or raise an Error
    """
    warn('This backend only works most of the time. The default backend is prefered.')
    # So we can compare later and make sure it works
    original = copy(regex)

    # So you can pass in an EasyRegex chain
    regex = str(regex)

    # Because I hate everyone and this is a stupid bug and it makes NO sense
    regex = re.sub(r'\\(?![AZbBcsSdDwWx0\|QEnrtvfox])', r'\\\\', regex)

    #* The order of these matter

    # Very first thing, remove any flags at the beginning
    # TODO: keep track of what flags are asserted. It's probably important?
    regex = _invertRegexes.flags.sub('', regex)

    regex = _invertRegexes.stringStart.sub('', regex)  # TODO
    regex = _invertRegexes.stringEnd.sub('', regex)  # TODO
    regex = _invertRegexes.lineEnd.sub('', regex)  # TODO

    # Single Characters
    regex = _invertRegexes.word.sub(_randWord(), regex)
    regex = _invertRegexes.s.sub(_whitespace, regex)
    regex = _invertRegexes.digit.sub(choice(_digits), regex)
    regex = _invertRegexes.char.sub(choice(_letters + '_'), regex)
    regex = _invertRegexes.any.sub(choice(_everything), regex)

    # Explicit Characters
    regex = _invertRegexes.newline.sub('\n', regex)
    regex = _invertRegexes.carriage.sub('\r', regex)
    regex = _invertRegexes.tab.sub('\t', regex)
    regex = _invertRegexes.vert.sub('\v', regex)
    regex = _invertRegexes.f.sub('\f', regex)

    # Matching
    regex = _invertRegexes.matchExactly.sub(r'\1', regex)

    # Amounts
    regex = _invertRegexes.matchRangeNonGreedy.sub(lambda m: m.group('prev') * randint(int(m.group('min')), int(m.group('max'))), regex)
    regex = _invertRegexes.matchRangeGreedy.sub(lambda m: m.group('prev') * randint(int(m.group('min')), int(m.group('max'))), regex)

    regex = _invertRegexes.atLeastOneNonGreedy.sub(r"\g<prev>" * randint(1, _alot), regex)
    regex = _invertRegexes.atLeastOneGreedy.sub(r"\g<prev>" * randint(1, _alot), regex)
    regex = _invertRegexes.matchExactAmt.sub(lambda m: m.group('prev') * randint(int(m.group('amt')), int(m.group('amt'))), regex)
    regex = _invertRegexes.matchMore.sub(lambda m: m.group('prev') * randint(int(m.group('min')), int(m.group('min')) + _alot), regex)

    # Not Chuncks
    regex = _invertRegexes.notWhitespace.sub(choice(_digits  + _letters + _punctuation + '_'), regex)
    regex = _invertRegexes.notDigit.sub(choice(_letters + _whitespace  + _punctuation + '_'), regex)
    regex = _invertRegexes.notWord.sub(choice(_punctuation + _whitespace), regex)

    # Conditionals
    regex = _invertRegexes.ifThing.sub(r'\g<stuff>', regex)
    regex = _invertRegexes.ifNotThing.sub(r'\g<stuff>', regex)
    regex = _invertRegexes.ifPrecededBy.sub(r'\g<stuff>', regex)
    regex = _invertRegexes.ifNotPrecededBy.sub(r'\g<stuff>', regex)
    regex = _invertRegexes.ifNotPrecededBy2.sub(r'\g<stuff>', regex)

    # Optionals
    regex = _invertRegexes.atLeastNoneNonGreedy.sub(r'\g<prev>' * randint(0, _alot), regex)
    regex = _invertRegexes.atLeastNoneGreedy.sub(r'\g<prev>' * randint(0, _alot), regex)
    regex = _invertRegexes.either.sub(r'\g<1>' if randint(0,1) else r'\g<2>', regex)
    # TODO: This isn't wrong, but it also isn't right. It only uses the start or the end, instead of the range
    regex = _invertRegexes.anyBetween.sub(r'\g<start>' if randint(0,1) else r'\g<end>', regex)
    regex = _invertRegexes.notAnyChars.sub(lambda m: choice(list(set(_everything).difference(list(m.group(1))))), regex)
    regex = _invertRegexes.anyChars.sub(lambda m: choice(list(m.group(1))), regex)
    regex = _invertRegexes.anyChars2.sub(lambda m: choice(m.groups()).replace(',', ''), regex)

    regex = _invertRegexes.lineStart.sub('', regex)  # TODO

    def tmp(m):
        options = m.groups()[0].split('|')
        return choice(options)
    regex = _invertRegexes.anyOf.sub(tmp, regex)

    # Groups
    def denest(regex, replace, current):
        new = regex.sub(replace, current)
        if current != new:
            new = denest(regex, replace, new)
        return new

    regex = denest(_invertRegexes.optionalNonGreedy, r'\g<prev>' if randint(0,1) else '', regex)
    regex = denest(_invertRegexes.optionalGreedy, r'\g<prev>' if randint(0,1) else '', regex)
    regex = denest(_invertRegexes.namedGroup, r'\g<stuff>', regex)
    regex = denest(_invertRegexes.passiveGroup, r'\1', regex)
    regex = denest(_invertRegexes.group, r'\1', regex)

    # referenceGroup = EasyRegexSingleton(lambda cur, name:        f'{cur}(?P={name})') # TODO))

    # Undo what we did earlier
    regex = re.sub(r'\\\\', r'\\', regex)
    regex = unsanitize(regex)

    # If the regex passed in isn't in what we generated, try again
    if re.search(str(original), regex) is not None or tries < 0:
        return regex
    else:
        if not tries:
            raise NotImplementedError(f"Can't invert the given regex. You can try again, which may work, or submit a bug report by emailing smartycope@gmail.com and including your pattern")
        else:
            return invertRegex(original, tries=tries-1)
