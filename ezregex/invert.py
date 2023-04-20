from dataclasses import dataclass
from random import randint, choice, choices
import re
from .EasyRegexMember import escapeChars

# from Cope import debug, todo, percent; todo('remove this')

def unsanitize(string):
    for part in escapeChars:
        string = re.sub(r'\\' + part, part[1], string)
    return string

def randbool():
    return bool(randint(0, 1))

def _randWord(randomlyGenerate=False):
    if randomlyGenerate:
        return ''.join(choices(_letters + '_', k=randint(1, _alot)))
    else:
        return 'word'

_prevThingRegex = r'(\\?\w+)\Z'
def _prevThing(cur):
    try:
        return re.search(_prevThingRegex, cur).group()
    except AttributeError:
        return ''

# Inverting helpers
_alot         = 6
_digits       = '0123456789'
_letters      = 'abcdefghijklmnopqrstuvwxyz'
_letters     += _letters.upper()
_punctuation  = r''',./;'[] = -)(*&^%$#@!~`+{}|:"<>?'''
_whitespace   = '\t'
_everything   = _digits + _letters + _punctuation + _whitespace + '_'

# notEscaped = r'[^\\]'
notEscaped = r'(?<!\\)'

# namedGroup('prev', either('(' + word() + ')', '.'))
# prevThing = fr'(?P<prev>(\(\w+\)|{notEscaped}.))'
# namedGroup('prev', anyof('(?:' + chunk() + ')', '(' + word() + ')', raw(r'(?<!\\)') + anything()))
prevThing = r'(?P<prev>(?:\(\?\:.+\)|\(\w+\)|(?<!\\).))'

tillCloseParen = r'(?P<stuff>.+)\)'

@dataclass
class _invertRegexes:
    start        = re.compile(r'\\A')
    end          = re.compile(r'\\Z')
    word         = re.compile(r'\\w\+')
    s            = re.compile(r'\\s')
    digit        = re.compile(r'\\d')
    char         = re.compile(r'\\w')
    any          = re.compile(notEscaped + r'\.')
    newline      = re.compile(r'\\n')
    carriage     = re.compile(r'\\r')
    tab          = re.compile(r'\\t')
    vert         = re.compile(r'\\v')
    f            = re.compile(r'\\f')
    matchExactly = re.compile(r'\^(.+)\$')  # \^stuff\$
    matchMax     = re.compile(fr'{prevThing}\+')  # (stuff)+
    # '(' + namedGroup('stuff', chunk()) + '){' + namedGroup('amt', number()) + '}'
    matchExactAmt = re.compile(prevThing + r'\{(?P<amt>\d+)\}')  # (stuff){3}
    # '(' + namedGroup('stuff', chunk()) + '){' + namedGroup('min', number()) + ',' + optional(space()) + namedGroup('max', number()) + '}'
    matchRange = re.compile(prevThing + r'\{(?P<min>\d+),( )?(?P<max>\d+)\}')  # (stuff){3,4}
    # '(' + namedGroup('stuff', chunk()) + '){' + namedGroup('min', number()) + ',' + optional(space()) + '}'
    matchMore = re.compile(prevThing + r'\{(?P<min>\d+),( )?\}')  # (stuff){3,}
    optional  = re.compile(prevThing + r'\?(?![\:P\<\!])')  # (stuff)?
    max       = re.compile(prevThing + r'\*')  # (stuff)*
    either    = re.compile(r'\((\w+)\|(\w+)\)')  # (stuff|things)
    notWhitespace = re.compile(r'\\S')
    notDigit      = re.compile(r'\\D')
    notWord       = re.compile(r'\\W')
    # This matches basically anything in square brackets that's not ^
    anyChars    = re.compile(r'(\[([^\^]\,?)+\])')  # [s,t]
    notAnyChars = re.compile(r'\[\^(.\,?)+\]')  # [^s,t]
    #
    # anyOf = re.compile(r'\((((.+)\|){1,}(.+))+\)') # (stuff|things)
    #! NOTE: This matches passive groups: (?:sequence) but I don't think its a problem, so long as the sequence doesn't contain a |
    #  TODO: this probably needs to be fixed at some point
    # todo('debugging this regex is where I left off. it needs to require at least 1 | in order to work properly -- fixing the problem in the above line')
    # group(either(ifPrecededBy('(?:'), ifPrecededBy('(')) + matchMax(anyCharExcept(r'|\)')) + '|' + matchMax(anyCharExcept(r'|\)')) + optional('|') + ifFollowedBy(')'))
    anyOf = re.compile(r'((?:(?<=\(\?\:)|(?<=\())(?:[^\|\)])+\|(?:[^\|\)])+(?:\|)?(?=\)))')  # (stuff|things|otherThings)
    # hex     = re.compile(r'\\(\d+)') # \\67
    # oct     = re.compile(r'\\x(\d+)') # \x67
    ifThing = re.compile(r'\(\?\=' + tillCloseParen)  # (?=stuff)
    ifNotThing       = re.compile(r'\(\?!' + tillCloseParen)  # (?!stuff)
    ifPrecededBy     = re.compile(r'\(\?\<\=' + tillCloseParen)
    ifNotPrecededBy  = re.compile(r'\(\?\<\!' + tillCloseParen)
    ifNotPrecededBy2 = re.compile(r'\(\?\!\=' + tillCloseParen)
    passiveGroup     = re.compile(r'\(\?\:([^\)\(\?]+)\)')  # (?:stuff)
    group = re.compile(r'\((?!\?)([^\)\(\?]+)\)')  # (stuff)
    notGroup = re.compile(r'\(\?:(.+)\)')  # (?:stuff)
    namedGroup = re.compile(r'\(\?P\<(?P<name>\w+)\>(?P<stuff>.+)\)')  # (P?<name>stuff)

def invertRegex(regex:str, colors=True, groupNames=True, explicitConditionals=False) -> str:
    """ 'Inverts' a regex expression. Gives an example of something that would match the given regex """
    defaultColor   = (204, 204, 204)
    notGroupColor  = (220, 0, 0)
    groupNameColor = (34, 111, 157)

    if explicitConditionals:
        _proceedOpen = '   <if followed by> { '
        _notProceedOpen = '   <if not followed by> { '
        _preceedOpen = '   <if preceeded by> { '
        _notPreceedOpen = '    <if not preceeded by> { '
        _optionalClose = ' }   '
    else:
        _proceedOpen = _notProceedOpen = _preceedOpen = _notPreceedOpen = _optionalClose = ''

    # So you can pass in an EasyRegex chain
    regex = str(regex)
    # Because I hate everyone and this is a stupid bug and it makes NO sense
    regex = re.sub(r'\\(?![AZbBcsSdDwWx0QEnrtvfox])', r'\\\\', regex)

    def randColor():
        return (randint(0, 255) % 20, randint(0, 255) % 20, randint(0, 255) % 20)

    def color(s, c, fg=False):
        if colors:
            return f'\0{"3" if fg else "4"}3[48;2;{c[0]};{c[1]};{c[2]}m{s}\033[38;2;{defaultColor[0]};{defaultColor[1]};{defaultColor[2]}m'
        else:
            return s

    #* The order of these matter
    regex = _invertRegexes.start.sub('', regex)  # TODO
    regex = _invertRegexes.end.sub('', regex)  # TODO

    # Single Characters
    regex = _invertRegexes.word.sub(_randWord(), regex)
    regex = _invertRegexes.s.sub(_whitespace, regex)
    regex = _invertRegexes.digit.sub(choice(_digits), regex)
    regex = _invertRegexes.char.sub(choice(_letters + '_'), regex)
    # regex = re.sub(r'\x',  choice(_digits + 'ABCDEF'), regex)
    # regex = re.sub(r'\O',  choice(_digits[:8]), regex)
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
    regex = _invertRegexes.matchMax.sub(r"\g<prev>" * randint(1, _alot), regex)
    regex = _invertRegexes.matchExactAmt.sub(lambda m: m.group('prev') * int(m.group('amt')), regex)
    regex = _invertRegexes.matchRange.sub(lambda m: m.group('prev') * randint(int(m.group('min')), int(m.group('max'))), regex)
    regex = _invertRegexes.matchMore.sub(lambda m: m.group('prev') * randint(int(m.group('min')), int(m.group('min')) + _alot), regex)

    # Not Chuncks
    regex = _invertRegexes.notWhitespace.sub(choice(_digits  + _letters + _punctuation + '_'), regex)
    regex = _invertRegexes.notDigit.sub(choice(_letters + _whitespace  + _punctuation + '_'), regex)
    regex = _invertRegexes.notWord.sub(choice(_punctuation + _whitespace), regex)  # I guess digits are counted as word chars?

    # Conditionals
    regex = _invertRegexes.ifThing.sub(_proceedOpen + r'\g<stuff>' + _optionalClose, regex)
    regex = _invertRegexes.ifNotThing.sub(_notProceedOpen + r'\g<stuff>' + _optionalClose, regex)
    regex = _invertRegexes.ifPrecededBy.sub(_preceedOpen + r'\g<stuff>' + _optionalClose, regex)
    regex = _invertRegexes.ifNotPrecededBy.sub(_notPreceedOpen + r'\g<stuff>' + _optionalClose, regex)
    regex = _invertRegexes.ifNotPrecededBy2.sub(_notPreceedOpen + r'\g<stuff>' + _optionalClose, regex)

    # Optionals
    regex = _invertRegexes.max.sub(r'\g<prev>' * randint(0, _alot), regex)
    regex = _invertRegexes.either.sub(r'\g<1>' if randint(0,1) else r'\g<2>', regex)
    # anyBetween    = EasyRegexSingleton(lambda cur, input, and_input: cur + r'[' + input + r'-' + and_input + r']') # TODO
    # Alright, so the regex matches basically anything in square brackets that's not a ^, including the square brackets. This gets that,
    #   drops the square brackets (with [1:-1]), and splits them along commas and chooses a random one
    regex = _invertRegexes.notAnyChars.sub(lambda m: choice(list(set(_everything).difference(m.groups()[0][1:-1].split(',')))), regex)
    regex = _invertRegexes.anyChars.sub(lambda m: choice(m.groups()[0][1:-1].split(',')), regex)
    # regex = _invertRegexes.anyOf.sub(lambda m: choice(m.groups()[0].split('|')), regex)

    def tmp(m):
        # debug(m.groups())
        # debug(m.groups()[0])
        # debug(m.group())
        options = m.groups()[0].split('|')
        # debug(options)
        # return debug(choice(m.groups()[0].split('|')), clr=2)
        # return debug(choice(options), clr=2)
        return choice(options)
    regex = _invertRegexes.anyOf.sub(tmp, regex)

    # Sets
    # regex = _invertRegexes.sub(r' \[A-Z\]',      choice(_letters.upper()), regex)
    # regex = _invertRegexes.sub(r' \[a-z\]',      choice(_letters.lower()), regex)
    # regex = _invertRegexes.sub(r'\[A-Za-z\]',    choice(_letters), regex)
    # regex = _invertRegexes.sub(r'\[A-Za-z0-9\]', choice(_letters + _digits), regex)
    # regex = _invertRegexes.sub(r'\[0-9\]',       choice(_digits), regex)
    # regex = _invertRegexes.sub(r'\[0-9a-fA-F\]', choice(_digits + "ABCDEF"), regex)
    # regex = _invertRegexes.sub(r'\[0-7\]',       choice(_digits[:8]), regex)
    # regex = _invertRegexes.sub(r'\[:punct:\]',   choice(_punctuation), regex)
    # regex = _invertRegexes.sub(r'\[ \t\r\n\v\f\]', choice(_whitespace), regex)
    # # regex = _invertRegexes.sub(r'\[\x00-\x1F\x7F\]', regex)
    # regex = _invertRegexes.sub(r'\[\\x21-\\x7E\]', choice(_everything.replace(' ', '')), regex)
    # regex = _invertRegexes.sub(r'\[\x20-\x7E\]', choice(_everything), regex)
    # regex = _invertRegexes.sub(r'\[A-Za-z0-9_\]', choice(_letters + _digits + '_'), regex)

    # Numbers
    # regex = _invertRegexes.hex.sub(r'0x\1',regex)
    # regex = _invertRegexes.oct.sub(r'0o\1',regex)

    # Groups
    regex = _invertRegexes.optional.sub(r'\g<prev>' if randint(0,1) else '', regex)
    regex = _invertRegexes.notGroup.sub(color(r'\1', notGroupColor), regex)  # TODO
    regex = _invertRegexes.namedGroup.sub((color(r'\g<name>: ', groupNameColor) if groupNames else '') + color(r'\g<stuff>', groupNameColor, True), regex)
    regex = _invertRegexes.passiveGroup.sub(r'\1', regex)
    regex = _invertRegexes.group.sub(color(r'\1', randColor()), regex)

    # referenceGroup = EasyRegexSingleton(lambda cur, name:        f'{cur}(?P={name})') # TODO))

    # Undo what we did earlier
    regex = re.sub(r'\\\\', r'\\', regex)
    return unsanitize(regex)

def testInvertRegex(regex, count=10, colors=True, groupNames=True, explicitConditionals=False):
    for i in range(count):
        print(invertRegex(regex, colors, groupNames, explicitConditionals))
