# Developer Documentation
## The EZRegex class
Everything relies on the EZRegex class. The EZRegex class is an abstract class, and each dialect subclasses the EZRegex class to define their own elements specific to that dialect (more on that later). The EZRegex class is not technically a metaclass, but functions similarly: at define time (not at instantiation time), it does a number of things:
1. Add variables to the class (more on that later)
2. Take members & methods of the subclass (including from mixins), and instantiate them into instances of the subclass (I'm calling these `singleton members`)
3. Generate the options function from the flags parameter
4. Make the subclass immutable
5. Add psuedonyms

Step 2 is probably the most confusing part. There are 2 reasons for doing it this way, generally. Firstly, I wanted to support chain-like syntax, like `word.anyof('123').digit`. But mainly, I wanted a more object-oriented way of defining dialects, instead of the hodge-podge pile of global functions I had before. The original operator syntax, `word + anyof('123') + digit`, still functions, because at the end of each dialect I simply have a function that puts all the singleton members into the global scope. This is much cleaner than the other way around.

The psuedonyms are simply alternate names for most of the functions. Internally, each singleton member has 1 name (lowercase, snake_case), but because this library is intended to be used by people writing in other languages, there's also snakeCase versions of each of them. Also, for many of the concepts, either there's multiple sensible names for them, or different dialects tend to call them different things (`letter` vs `alpha`, `at_least_none` vs `any_amt` vs `zero_or_more`, etc). Note that camelCase versions are auto-generated from both the cannonical names and psuedonyms at define time as well.

Each `singleton member` (and their associated global version) represents a fundamental part of the Regular Expression syntax for that language, as well as less-fundemental common combinations for convenience (like email and float).

## Creating a New Dialect
New dialects are implemented in their own submodule, and are imported into the main module. They should have a single class that inherits from EZRegex. The submodule naming convention is all lowercase, using non-acronyms where it makes sense to (e.g. `javascript` instead of `js`, but `pcre2` is still `pcre2`).

An example is worth a thousand explanations, so here's an example dialect:

```python
from .. import EZRegex
from ..mixins import (BaseMixin, AssertionsMixin, GroupsMixin, AnchorsMixin, ReplacementsMixin, AdvancedGroupsMixin, AdvancedReplacementsMixin, imply_pattern_is_cur, raise_if_empty)
from ..flag_docs import common_flag_docs

# This is the naming convention
class PythonEZRegex(
    # Note that for clarity, all mixins only take named parameters
    # This is the base syntax, shared by most of the dialects. Single elements which don't fit can be removed
    # or overriden as needed
    # Auto-generates greedy and possessive variants where applicable
    BaseMixin(allow_greedy=True, allow_possessive=True),
    # Adds things like lookahead assertions
    AssertionsMixin(),
    # Adds groups, used for replacement regexs.
    GroupsMixin(
        # Some of these are specified as parameters, instead of later in the class body
        # because it integrates it into more advanced logic internally, or it's used in multiple parts
        named_group=lambda pattern, name, cur=...: f'{cur}(?P<{name}>{pattern})',
    ),
    # This adds some more advanced group syntax, like referencing earlier groups. Later, even more advanced
    # parts will get added to this, such as branching logic
    AdvancedGroupsMixin(
        earlier_numbered_group=lambda num, cur=...: f'{cur}\\{num}',
        earlier_named_group=lambda name, cur=...: f'{cur}(?P={name})'
    ),
    # Adds regex anchors
    AnchorsMixin(
        # adds start/end of string and is_exactly
        string=True,
        # adds start/end of line
        line=True,
        # adds word/not word boundary
        word_boundaries=True,
        # adds word starts/ends with
        word=True,
        # The default is \z, but some dialects use \Z instead
        string_end=r'\Z'
    ),
    # Adds replacement syntax. These are distinct and not interoperable with regular regexs
    ReplacementsMixin(
        named_group=lambda name, cur=...: fr'{cur}\g<{name}>',
        numbered_group=lambda num, cur=...: fr'{cur}\g<{num}>'
    ),
    # Includes defaults for entire_string, string_before_match, and string_after_match
    AdvancedReplacementsMixin(),
    # This needs to be last, because Python evaluates multiple inheritence from left to right,
    # and all the mixins need to be transformed
    EZRegex,

    # These are now not inherited classes, but parameters that get passed to EZRegex.__init_subclass__
    # These are the characters in this dialect that we want to auto-escape
    escape_chars=b'()[]{}?*+-|^$\\.&~# \t\n\r\v\f',
    # These are the flags in this dialect. The names should be lower, snake_case, like so, and the
    # values should be the single character flag associated with it
    flags={
        'ascii': 'a',
        'ignore_case': 'i',
        'single_line': 's',
        'locale': 'L',
        'multiline': 'm',
        'unicode': 'u'
    },
    # A lot of the dialects share flags, so I've provided a common set of flag docs
    flags_docs_map={**common_flag_docs, 'locale': '''Try not to use this, and rely on unicode matching instead'''},
    # A link to the official docs for the flags. This is purely optional, and used to
    # dynamically generate the options() docstring
    flags_docs_link='https://docs.python.org/3/library/re.html#flags',

    # This is also optional. This is a dict of variables that get added to the class.
    # The keys are the names of the variables, and the values are (default_value, combine_function)
    # The default_value can be a callable, which will be called with the object in question
    # (which may or may not be an EZRegex instance). If it's not callable, it uses that as the default value
    # The combine_function takes 2 arguments, l and r, for left and right, and returns the combined value
    # In this case, we have a function below which caches the compiled regex. If we add anything to the
    # EZRegex chain, we need to invalidate the cache, so the default value is `None` (uncompiled), and
    # the combine function always returns None
    variables={
        '_compiled': (None, lambda l, r: None),
    }
):
    # It's polite to link to the official docs
    """
    Official docs:
    https://docs.python.org/3/library/re.html
    """

    # If you want to add methods specific to this dialect, you can by decorating them with
    # EZRegex.exclude. This prevents them from being transformed into EZRegex objects.
    @EZRegex.exclude
    def compile(self, add_flags=True):
        return re.compile(self._compile(add_flags=add_flags))

    # There are 5 ways to define parts of the dialect:
    # 1. As a string. This just adds the string to the end of the current complied regex
    white_char = r'\s'

    # 2. A lambda. It can take any parameters, but must take cur=... as a keyword parameter,
    # and it must have ... as the default value. cur gets passed as the current complied regex string,
    # and what the lambda returns becomes the new complied regex string. Note that cur is guranteed to
    # be a string. Other parameters are sanatized: None and bools are passed as-is, ints are cast to strings,
    # and strings are escaped based on the dialect's escape_chars. Any other types are auto-cast to strings,
    # special characters are not escaped, and a warning is thrown. See EZRegex._sanitize_param for more info
    literal = lambda pattern, cur=...: cur + pattern

    # 3. A callable. It functions exactly the same as the lambda
    def any_between(char:str, and_char:str, cur=...):
        """Match any char between `char` and `and_char`, using the ASCII table for reference"""
        # You can use raise_if_empty() to raise a ValueError if a parameter is and empty string
        raise_if_empty(char, 'any_between', 'char')
        raise_if_empty(and_char, 'any_between', 'and_char')
        return cur + r'[' + char + r'-' + and_char + r']'

    # 4. A tuple of (lambda, dict). The lambda functions as above, and the dict is a dictionary of variables
    # to add to the class. This sets the default value for this instance, and then they propagate as
    # defined in the variables parameter to the class
    line_starts_with = lambda pattern='', cur=...: r'^' + pattern + cur, {'flags':'m'}

    # 5. A function decorated with add_vars. This does the same as #4, but in case you need
    # more complex logic, you can use this
    @add_vars(replacement=True)
    def rliteral(pattern, cur=...):
        return cur + pattern

    # There's also another helpful decorator, imply_pattern_is_cur
    # If `pattern` is Ellipsis, it will use `cur` instead, and `cur` will be set to an empty string.
    # This is useful for functions that want to allow both inline and operator style chaining
    # i.e. digit.amt(2) and amt(2, digit)
    # NOTE: `pattern` must be a keyword parameter, and it must be the last parameter able to be
    # provided as a positional argument. Don't use *args.
    @imply_pattern_is_cur
    def match_max(pattern=..., *, cur=...):
        """ Match as many of `pattern` in the string as you can. This is equivelent to using the unary + operator. """
        return cur + r'(?:' + pattern + r')' + r'+'

    # Feel free to add raw regexs for this dialect here.
    version = r"(?P<major>0|[1-9]\d*) ..."
    """The *official* regex for matching version numbers from https://semver.org/."""
    # Docstrings immediately after members are used as the docstring. This will be added in a later version
```

The __init__ file in the submodule must look like this:
```python
from .DialectEZRegex import DialectEZRegex
from ..inject_parts import inject_parts

globals().update(inject_parts(DialectEZRegex))
```
This will inject all the members into the module, and make them available as attributes of the module.

When adding a new dialect, you can do it incrementally, adding parts at a time, but try to keep all the tests passing.

## Inverting
There's actually 2 algorithms implemented for "inverting" regexs. The old algorithm regexs the regexs in a specific order to replace parts one at a time. This is just as nasty and horrifying as it sounds. Dispite it being a terrible, *terrible* solution, I actually got it to work decently well.

Later, when I was reading up on abstract syntax trees, and scrolling around on PyPi, I realized that Python has one built in, and that it's available to use. I reimplemented the whole algorithm to instead parse the AST given by the built-in re lexer, and wrote my own parser on top of it, which works *much* better.

Along the way, I also discovered, deep in the corners of the internet, 2 other Python libraries which do almost the same thing: `xeger` (regex backwards), and `sre_yield`. `xeger` technically works, however it tends to include unprintable characters, so it's output isn't very readable. `sre_yeild` is better, but it can be very slow, and is not quite the use case I'm going for. My invert algorithm is meant to be a debugging tool (though it doubles well for a testing tool), so it does things like detecting words (as opposed to seperate word characters) and inserts actual words, and doing the same for numbers and inserting `12345...`, as well as a couple other enhancements.

## Documentation
Docs are hosted on readthedocs, built by mkdocs, and the dialect docs are assisted by pdoc.
<!-- TODO: more details here -->

## Tests
Tests are run using GitHub Actions, and are run in a Docker container. The Dockerfile is in the `tests` directory, and the manager script is in the same directory. The manager script is run using `bash manager.sh`

How it works:
1. The docker container is built, either locally, or by GitHub Actions
2. The manager script is run inside the docker container, given the arguments passed to the docker run command
3. The manager script runs the appropriate tests
    * For dialect tests, because the regexs in regexs.jsonc are EZRegexs, not regular expression strings, the file needs to be "compiled" by python in order to be used by other languages, before running individual test runner scripts. This is handled by the `compile_regexs.py` script, which is called by the manager script when appropriate.
    * Each dialect has its own test runner script, which is run by the manager script. These are written in their appropriate language.

Commands:
(All commands should be run from the project root directory)
* To build locally:
    * `docker build -f ./tests/Dockerfile -t ezregex-test .`
    * Note: the first time building takes a while
* To force rebuild locally:
    * `docker build -f ./tests/Dockerfile -t ezregex-test --no-cache .`
* To run tests locally (syncs the project directory and the terminal with the container):
    * `docker run -it -v "$(pwd)":/app ezregex-test <args>`
    * Args:
        * `invert [args] | generate | all | most | dialect <dialect> | pytests`
        * dialect accepts `py | js | r | pcre2 | all | misc`
            * misc runs additional dialect tests that can't be covered by the standard suite of regexs.jsonc/replacements.jsonc tests, like when things should throw errors. They're not specific to any given dialect
        * invert accepts
            * `--strictness <int>`
                * How many times we try inverting a regex, to ensure they all work
            * `--tries <int>`
                * How many times we try inverting before giving up (-1 means just return a bad inversion)
            * `--timeout <int>`
                * How many seconds we allow inverting to take before calling it an infinite loop
            * `--passed`
                * Include passed inversions in the summary
            * `--backend <backend>`
                * The backend to use for inverting. Defaults to "whatever works, in order". For testing the custom backend, it's recommended to use `re_parser`
        * generate takes a long time, and is not run by default
        * pytests runs all the pytests (other than invert and generate)
        * most runs all the tests other than generate
        * all runs all the tests

### Some helpful hints
* If one of the dialect runners *fails*, it could be just a problem with the regexs.jsonc file.
* If one of the dialect runners *errors*, you're probably allowing compilation of a regex that the dialect doesn't support. That means it's a problem with the code itself, and the regexs.jsonc file has innaccurate dialects specified.
* If the compile_regexs.py script fails, it's probably a problem with the regexs.jsonc file trying to use a feature of a dialect that it doesn't support (innaccurate dialects).
