import re
from copy import deepcopy
from re import RegexFlag
from typing import List
from warnings import warn

from rich import print as rprint
from rich.panel import Panel
from rich.text import Text

from .invert import invertRegex
from functools import partial
from random import shuffle

# These are mutable parts of the Regex statement, produced by EasyRegexElements.
# Should not be instantiated by the user directly.
class EZRegexMember:
    def __init__(self, funcs:List[partial], sanatize=True, init=True, replacement=False, flags=0):
        """ The workhorse of the EZRegex library. This represents a regex pattern
        that can be combined with other EZRegexMembers and strings.
        Ideally, this should only be called internally, but it should still
        work from the user's end
        """
        self.flags = flags

        # Parse params
        # Add flags if it's another EZRegexMember
        if isinstance(funcs, EZRegexMember):
            self.flags = funcs.flags

        if isinstance(funcs, (str, EZRegexMember)):
            funcs = [str(funcs)]
        elif not isinstance(funcs, (list, tuple)):
            funcs = [funcs]

        self.sanatize = sanatize
        self.replacement = replacement
        self.funcList = list(funcs)
        self.example = self.invert = self.inverse

        # The init parameter is not actually required, but it will make it more
        # efficient, so we don't have to check that the whole chain is callable
        if init:
            # Go through the chain (most likely of length 1) and parse any strings
            # This is for simplicity when defining all the members
            for i in range(len(self.funcList)):
                if isinstance(self.funcList[i], str):
                    # I *hate* how Python handles lambdas
                    stringBecauseHatred = deepcopy(self.funcList[i])
                    self.funcList[i] = lambda cur=...: cur + stringBecauseHatred
                elif not callable(self.funcList[i]) and self.funcList[i] is not None:
                    raise TypeError(f"Invalid type {type(self.funcList[i])} passed to EZRegexMember constructor")

    def _sanitizeInput(self, i, addFlags=False):
        """ Instead of rasising an error if passed a strange datatype, it now
            trys to cast it to a string """
        i = deepcopy(i)

        # Don't sanatize anything if this is a replacement string
        if self.replacement:
            return str(i)

        # If it's another chain, compile it
        if isinstance(i, EZRegexMember):
            # This causes *weird* errors... that make sense in hindsight
            # self.flags |= i.flags
            # This works
            # i.flags |= self.flags
            # ...but I don't think is necissary, cause we're compiling without flags anyway?
            # return i._compile(addFlags=False)
            return i._compile(addFlags=addFlags)
        # It's a string (so we need to escape it)
        elif isinstance(i, str):
            i = re.escape(i)
            return i
        # A couple of singletons use bools and None as kwargs, just ignore them and move on
        elif i is None or isinstance(i, bool):
            return i
        # A couple singletons use ints as input, just cast it to a string and don't throw a warning
        elif isinstance(i, int):
            return str(i)
        # It's something we don't know, but try to cast it to a string anyway
        else:
            try:
                s = str(i)
                msg = f"Type {type(i)} passed to EZRegexMember, auto-casting to a string. Special characters will will not be escaped."
                try:
                    from Cope import debug
                except:
                    warn(msg)
                else:
                    debug(msg, color=-1, calls=3)
                return s
            except:
                raise TypeError(f'Incorrect type {type(i)} given to EZRegexMember parameter: Must be string or another EZRegexMember chain.')

    def __call__(self, *args, **kwargs):
        """ This should be called by the user to specify the specific parameters
            of this instance
            i.e. anyof('a', 'b')
        """
        # If this is being called without parameters, just compile the chain.
        # If it's being called *with* parameters, then it better be a fundemental
        # member, otherwise that doesn't make any sense.
        if len(self.funcList) > 1:
            if not len(args) and not len(kwargs):
                return self._compile()
            else:
                raise TypeError("You're trying to pass parameters to a chain of expressions. That doesn't make any sense. Stop that.")

        # Sanatize the arguments
        args = list(map(self._sanitizeInput if self.sanatize else deepcopy, args))
        # args = list(args)
        # for cnt, i in enumerate(args):
        #     args[cnt] = self._sanitizeInput(i) if self.sanatize else deepcopy(i)
        _kwargs = {}
        for key, val in kwargs.items():
            _kwargs[key] = self._sanitizeInput(val) if self.sanatize else deepcopy(val)
        # _kwargs['cur'] = args[0]
        # del args[0]

        return EZRegexMember([partial(self.funcList[0], *args, **_kwargs)], init=False, sanatize=self.sanatize, replacement=self.replacement, flags=self.flags)

    # Magic Functions
    def __str__(self, addFlags=True):
        return self._compile(addFlags)

    def __repr__(self):
        return 'ezregex("' + self._compile() + '")'

    def __eq__(self, thing):
        return self._sanitizeInput(thing, addFlags=True) == self._compile()

    def __mul__(self, amt):
        rtn = self
        # This isn't optimal, but it's unlikely anyone will use this with large numbers
        for i in range(amt-1):
            # This doesn't work
            # rtn += self
            # But this does??
            rtn = rtn + self
        return rtn

    def __rmul__(self, amt):
        return self * amt

    def __imul__(self, amt):
        return self * amt

    def __add__(self, thing):
        return EZRegexMember(self.funcList + [partial(lambda cur=...: cur + self._sanitizeInput(thing))],
            init=False,
            sanatize=self.sanatize or thing.sanatize if isinstance(thing, EZRegexMember) else self.sanatize,
            replacement=self.replacement or thing.replacement if isinstance(thing, EZRegexMember) else self.replacement,
            flags=self.flags | thing.flags if isinstance(thing, EZRegexMember) else self.flags
        )

    def __radd__(self, thing):
        return EZRegexMember([partial(lambda cur=...: self._sanitizeInput(thing) + cur)] + self.funcList,
            init=False,
            sanatize=self.sanatize or thing.sanatize if isinstance(thing, EZRegexMember) else self.sanatize,
            replacement=self.replacement or thing.replacement if isinstance(thing, EZRegexMember) else self.replacement,
            flags=self.flags | thing.flags if isinstance(thing, EZRegexMember) else self.flags
        )

    def __iadd__(self, thing):
        # return self + self._sanitizeInput(thing)
        return self + thing

    # def __and__(self, thing):
        # return self.__add__(self, thing)

    # The shift operators just shadow the add operators
    def __lshift__(self, thing):
        return self.__add__(thing)

    def __rlshift__(self, thing):
        return self.__radd__(thing)

    def __ilshift__(self, thing):
        return self.__iadd__(thing)

    # I don't think right and left shifts should be any different, right?
    def __rshift__(self, thing):
        return self.__add__(thing)

    def __rrshift__(self, thing):
        return self.__radd__(thing)

    def __irshift__(self, thing):
        return self.__iadd__(thing)

    def __invert__(self):
        return self.invert()

    def __not__(self):
        raise NotImplementedError('The not operator is not implemented. What you probably want is one of anyExcept(), anyCharExcept(), ifNotProceededBy(), or ifNotPreceededBy()')

    def __pos__(self):
        comp = self._compile()
        return EZRegexMember(('' if not len(comp) else r'(?:' + comp + r')') + r'+', sanatize=False)

    def __or__(self, other):
        return

    def __hash__(self):
        return hash(self._compile())

    def __contains__(self, thing):
        assert isinstance(thing, str), "`in` statement can only be used with a string"
        return re.search(self._compile(), thing) is not None

    # I guess this isn't a thing? But it really should be.
    def __rcontains__(self, thing):
        assert isinstance(thing, str), "`in` statement can only be used with a string"
        return re.search(self._compile(), thing) is not None

    def __reversed__(self):
        return self.inverse()

    def __rich__(self):
        return self._compile()

    def __pretty__(self):
        return self._compile()

    # Regular functions
    def _compile(self, addFlags=True):
        regex = ''
        for func in self.funcList:
            regex = func(cur=regex)
            # regex = func(regex)

        # Add the flags
        _flags = ''
        if addFlags:
            if self.flags & RegexFlag.ASCII:
                _flags += 'a'
            if self.flags & RegexFlag.DEBUG:
                pass
            if self.flags & RegexFlag.DOTALL:
                _flags += 's'
            if self.flags & RegexFlag.IGNORECASE:
                _flags += 'i'
            if self.flags & RegexFlag.LOCALE:
                _flags += 'L'
            if self.flags & RegexFlag.MULTILINE:
                _flags += 'm'
            if self.flags & RegexFlag.TEMPLATE:
                pass
            if self.flags & RegexFlag.UNICODE:
                _flags += 'u'
            if self.flags & RegexFlag.VERBOSE:
                _flags += 'x'
            if len(_flags):
                regex = fr'(?{_flags})' + regex
        return regex

    def compile(self, addFlags=True):
        return re.compile(self._compile(addFlags))

    def str(self):
        return self.__str__()

    def debug(self):
        try:
            from Cope import debug
        except ModuleNotFoundError:
            print(f"Compiled ezregex string = {self}")
        else:
            debug(self, name='Compiled ezregex string', calls=2)
        return self

    def debugStr(self):
        return self.debug().str()

    def copy(self):
        try:
            from clipboard import copy
        except ImportError:
            print('Please install the clipboard module in order to auto copy ezregex expressions (i.e. pip install clipboard)')
        else:
            copy(self._compile())

    def test(self, testString=None, show=True, context=True) -> bool:
        """ Tests the current regex expression to see if it's in @param testString.
            Returns the match objects (None if there was no match)
        """

        json = self._matchJSON(testString=testString)
        if not show:
            return bool(len(json['matches']))

        _cope = False
        if context:
            # Use the nice context function in the Cope library
            try:   from Cope import get_context, get_metadata
            except ImportError: pass
            else:  _cope = True

        st = Text()  # String
        gt = Text()  # Groups (all the group-related text)
        defaultColor = 'bold'
        textColor = ''

        st.append("Testing expression", style=defaultColor)
        # Add the context line
        if _cope:
            st.append(f' (from {get_context(get_metadata(2), False, True, True).strip()})', style=defaultColor)
        st.append(':\n', style=defaultColor)

        # The expression we're testing
        st.append(f'\t{json["regex"]}\n', style=textColor)
        st.append("for matches in:\n\t", style=defaultColor)

        # Add the main string
        for color, background, part in json['parts']:
            st.append(part, style=color if background is None else f'{color} on {background}')
        st.append('\n')

        # Add all the matches and groups
        for m in json['matches']:
            gt.append('Match = "')
            for color, background, part in m['match']['parts']:
                gt.append(part, style=color if background is None else f'{color} on {background}')
            gt.append('" ')
            gt.append(f"({m['match']['start']}:{m['match']['end']})", style=f'italic bright_black')
            gt.append('\n')
            if len(m['unnamedGroups']):
                gt.append('Unnamed Groups:\n')
            for cnt, group in enumerate(m['unnamedGroups']):
                gt.append(f'\t{cnt+1}: "')
                gt.append(group['string'], style=group['color'])
                gt.append('" ')
                gt.append(f"({group['start']}:{group['end']})", style=f'italic bright_black')
                gt.append('\n')
            if len(m['namedGroups']):
                gt.append('Named Groups:\n')
            for name, group in m['namedGroups'].items():
                gt.append(f'\t{name}: "')
                gt.append(group['string'], style=group['color'])
                gt.append('" ')
                gt.append(f"({group['start']}:{group['end']})", style=f'italic bright_black')
                gt.append('\n')
            gt.append('\n')

        # Assemble everything into a panel
        rprint(Panel(Text.assemble(*st, '\n', *gt),
            title='Testing Regex',
            subtitle=Text('Found\n', style='blue') if len(json['matches'])
                else Text('Not Found\n', style='red')))  #, border_style='dim green')

        return bool(len(json['matches']))

    def _matchJSON(self, testString=None):
        #           red         green       yellow    blue       orange     purple      teal  greenish teal skin color dark green dark teal pale pink   brown    pale yellow  maroon
        # _colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#d16d2a', '#651fb6', '#39c5c5', '#a8f678', '#fabebe', '#808000', '#008080', '#e6beff', '#9a6324', '#c5c19b', '#800000']
        # _colors = ['#800000', '#9a6324', '#808000', '#d16d2a', '#e6194b', '#fabebe', '#ffe119', '#c5c19b', '#a8f678', '#3cb44b', '#39c5c5', '#008080', '#4363d8', '#e6beff', '#651fb6']
        # Lighter ones, so they show up better on a dark background
        _matchColors = ["#ffe119", "#a8f678", "#fabebe", "#39c5c5", "#c5c19b", '#44ff00', "#8da0cb", "#df5e3e", "#f08a5d", '#00ffe1', '#ff0000']
        shuffle(_matchColors)
        # darker ones, so they show up better on _matchColors
        _groupColors = ["#800000", "#d1750b", "#005f00", "#3cb44b", '#6c6c6c', "#4363d8", "#651fb6", '#95624e', '#870000', '#086f95', '#829569']
        shuffle(_groupColors)
        _colors = _groupColors + _matchColors

        # Get an inverse, if nessicary
        if testString is None or not len(testString):
            testString = self.inverse()
        matches = list(re.finditer(self._compile(), testString))
        found = bool(len(matches))

        json = {
            'regex': self._compile(),
            'string': testString,
            'stringHTML': ...,
            'parts': [],
            'matches': []
        }

        html_string = '<p><span style="color: white;">'
        parts = []
        globalCursor = 0
        allMatches = [m.span() for m in matches]
        # Map match spans to unique colors
        # matchColors = dict(zip(allMatches, reversed(_matchColors)))
        while len(allMatches) > len(_colors):
            _colors += _colors
        matchColors = dict(zip(allMatches, reversed(_colors)))

        for match in matches:
            allGroups = {match.span(i+1) for i in range(len(match.groups()))}
            namedGroups = dict({(i, match.span(i)) for i in match.groupdict().keys()})
            unnamedGroups = allGroups - set(namedGroups.values())
            # Map group spans to unique colors
            # colors = dict(zip(allGroups, _groupColors))
            colors = dict(zip(allGroups, _colors))
            # So different matches have different groups of colors
            # _groupColors = _groupColors[len(allGroups):]
            _colors = _colors[len(allGroups):]
            cursor = match.span()[0]

            # First, get up until the match
            html_string += f'{testString[globalCursor:cursor]}</span>'
            parts.append([None, None, testString[globalCursor:cursor]])
            match_html = ''
            match_parts = []
            for g in sorted(allGroups, key=lambda x: x[0]):
                # Print the match up until the group
                match_html += f'<span style="color: {matchColors[match.span()]};">{testString[cursor:g[0]]}</span>'
                match_parts.append([matchColors[match.span()], None, testString[cursor:g[0]]])

                # Print the group
                match_html += f'<span style="background-color: {colors[g]}; color: {matchColors[match.span()]};">{testString[g[0]:g[1]]}</span>'
                match_parts.append([matchColors[match.span()], colors[g], testString[g[0]:g[1]]])
                cursor = g[1]
            match_html += f'<span style="color: {matchColors[match.span()]};">{testString[cursor:match.span()[1]]}</span>'
            match_parts.append([matchColors[match.span()], None, testString[cursor:match.span()[1]]])
            globalCursor = match.span()[1]
            # Don't print after the group, cause there might be another match that covers it
            html_string += match_html
            parts += match_parts
            toSlice = lambda t: f'({t[0]}:{t[1]})'
            match_json = {
                'match': {
                    'string': match.group(),
                    'stringHTML': match_html,
                    'parts': match_parts,
                    'end': match.end(),
                    'start': match.start(),
                    "color": matchColors[match.span()],
                },
                "unnamedGroups":[],
                "namedGroups":{},
            }

            for i in range(len(unnamedGroups)):
                match_json['unnamedGroups'].append({
                    'string': match.group(i+1),
                    'end': match.end(i+1),
                    'start': match.start(i+1),
                    "color": colors[match.span(i+1)],
                })

            for name, span in namedGroups.items():
                match_json['namedGroups'][name] = {
                    'string': match.group(name),
                    'end': span[1],
                    'start': span[0],
                    "color": colors[span],
                }
            json['matches'].append(match_json)


        # Don't forget to add any bit at the end that's not part of a match
        html_string += testString[globalCursor:]
        parts.append([None, None, testString[globalCursor:]])
        html_string += '</span></p>'
        json['stringHTML'] = html_string
        json['parts'] = parts
        return json

    def inverse(self, amt=1, **kwargs):
        """ "Inverts" the current Regex expression to give an example of a string
            it would match.
            Useful for debugging purposes.
        """
        return '\n'.join([invertRegex(self._compile(), **kwargs) for _ in range(amt)])





"""
    def test(self, testString=None, show=True, context=True) -> bool:
        Tests the current regex expression to see if it's in @param testString.
            Returns the match objects (None if there was no match)

        # Get an inverse, if nessicary
        _assert = testString is None
        if testString is None:
            testString = self.inverse()
        matches = list(re.finditer(self._compile(), testString))
        found = bool(len(matches))

        if not show:
            return found

        _cope = False
        if context:
            # Use the nice context function in the Cope library
            try:
                from Cope import get_context, get_metadata
            except ImportError:
                pass
            else:
                _cope = True

        st = Text()  # String
        gt = Text()  # Groups (all the group-related text)
        defaultColor = 'bold'
        textColor = ''

        st.append("Testing expression", style=defaultColor)
        # Add the context line
        if _cope:
            st.append(f' (from {get_context(get_metadata(2), False, True, True).strip()})', style=defaultColor)
        st.append(':\n', style=defaultColor)
        # The expression we're testing
        st.append(f'\t{self._compile()}\n', style=textColor)
        st.append("for matches in:\n\t", style=defaultColor)

        globalCursor = 0
        allMatches = [m.span() for m in matches]
        # 14-a, to differentiate from the group colors
        # Map match spans to unique colors
        # TODO: This will fail if testString has more than 14 matches (I think? Not sure how rich will handle negative colors)
        matchColors = dict(zip(allMatches, map(lambda a: 14-a, range(len(allMatches)))))
        startColors = 1

        for match in matches:
            allGroups = {match.span(i+1) for i in range(len(match.groups()))}
            namedGroups = dict({(i, match.span(i)) for i in match.groupdict().keys()})
            unnamedGroups = allGroups - set(namedGroups.values())
            # +1, just so we can get different starting color other than black
            # Map group spans to unique colors
            colors = dict(zip(allGroups, map(lambda a: a+startColors, range(len(allGroups)))))
            # So different matches have different groups of colors
            startColors += len(allGroups)
            cursor = match.span()[0]

            # First, print up until the match
            st.append(testString[globalCursor:cursor], style=textColor)
            for g in sorted(allGroups, key=lambda x: x[0]):
                # Print the match up until the group
                st.append(testString[cursor:g[0]], style=f'color({matchColors[match.span()]})')
                # Print the group
                st.append(testString[g[0]:g[1]], style=f'color({matchColors[match.span()]}) on color({colors[g]})')
                cursor = g[1]
            st.append(testString[cursor:match.span()[1]], style=f'color({matchColors[match.span()]})')
            globalCursor = match.span()[1]
            # Don't print after the group, cause there might be another match that covers it

            toSlice = lambda t: f'({t[0]}:{t[1]})'
            gt.append('\nMatch = ', style=f'italic color({matchColors[match.span()]})')
            gt.append(f'"{match.group()}"', style=f'color({matchColors[match.span()]})')
            gt.append(f' {toSlice(match.span())}\n', style=f'italic color({matchColors[match.span()]})')

            if len(unnamedGroups):
                gt.append('Unnamed Groups:\n', style=f'italic color({matchColors[match.span()]})')
            for i in range(len(unnamedGroups)):
                clr = f'color({colors[match.span(i+1)]})'
                gt.append(f'\t{i+1}: ', style=f'color({matchColors[match.span()]})')
                gt.append(f'"{match.group(i+1)}"', style=f'color({matchColors[match.span()]}) on {clr}')
                gt.append(f' {toSlice(match.span(i+1))}\n', style=f'italic color({matchColors[match.span()]})')

            if len(namedGroups):
                gt.append('Named Groups:\n', style=f'italic color({matchColors[match.span()]})')
            for name, span in namedGroups.items():
                clr = f'color({colors[span]})'
                gt.append(f'\t{name}: ', style=f'color({matchColors[match.span()]})')
                gt.append(f'"{match.group(name)}"', style=f'color({matchColors[match.span()]}) on {clr}')
                gt.append(f' {toSlice(span)}\n', style=f'italic color({matchColors[match.span()]})')

        # Don't forget to add any bit at the end that's not part of a match
        st.append(testString[globalCursor:], style=textColor)

        # if _internal:
        #     print(st.markup + '\n' + gt.markup)
        #     return found

        # if rtn is str:
            # return '\n'.join([t._text for t in st])
            # return '\n'.join(st._text)
            # return str(st) + '\n' + str(gt)

        rprint(Panel(Text.assemble(*st, '\n', *gt),
            title='Testing Regex',
            subtitle=Text('Found\n', style='blue') if found
                else Text('Not Found\n', style='red')))  #, border_style='dim green')

        # if rtn is bool:
        return found
"""
