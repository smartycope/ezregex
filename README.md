# ezregex

An readable and intuitive way to generate Regular Expressions

TL;DR: This is to regular expressions what CMake is to makefiles

**Table of Contents**

* [Installation](#installation)
* [License](#license)

## Usage:
```
    import ezregex as er
    optW = er.optional(er.whitechunk)
    optionalParams = er.multiOptional(optW + er.group(er.optional(er.chunk)) + optW + er.match(','))
    function = er.stuff + 'func(' + er.ifFollowedBy(optionalParams) + ')'
    function.test('this should match only the func(param1, param2 ) part of this string')
```

## Current limitations
- inverse() doesn't work well with broken up chains. A large code refactoring would be required. So to get proper
    inverting on broken up functions, you have to put .inverse() at the end of every chain, before it enters the main chain.
    This will mess up your end result however, so use only for debugging purposes.
- inverse() is also not totally function yet? It's closish, but currently only works on simple regex expressions
- The "not" operator doesn't currently work. Another large code refactoring would be required.
- Everything is kinda just mushed together as generic dialect. Separating of python and generic dialects would be helpful.
- The Perl dialect isn't implemented at all. I don't know any perl, but this is meant to be a cross-platform solution.

## Explination of How it Works
This is version 2. The original version just had an EasyRegex class with a bunch of members that returned self, then you chained together member function calls.

**NOTE** this is no longer accurate in version >1.1.0. EZRegexSingleton is no longer a thing, and they're all EZRegexMembers
This version uses a bunch of constant singletons (of type EasyRegexSingleton) that have the __call__() dunder function overridden to return a separate class (EasyRegexMember) which override the __add__() and __str__() dunder functions. What happens is you have all the singletons created in __init__.py, specifying lambdas (or strings, for convenience) describing how they interact with the current regex expression, and then optional inverted lambdas (get to that in a moment) and separate dialect lambdas. When those are called later on by the user, (they can be treated like regular functions) they initialize a EasyRegexMember, and give it the function they hold. Then, EasyRegexMembers are chained together with +'s (or <<'s). EasyRegexMembers all have internal ordered lists of functions that get added to when +'ed. If you assign the chain (or chains!) to a varaible or put in ()'s, what you end up with is one EasyRegexMember that has an ordered list of all the functions from all the EasyRegexMembers in that chain. When you then cast that to a string (or call .str() or .compile()), it finally goes through and calls all those functions, which results in the final regex string.


## Installation

ezregex is distributed on [PyPI](https://pypi.org) as a universal
wheel and is available on Linux/macOS and Windows and supports
Python 3.10+ and PyPy.

```bash
$ pip install ezregex
```

## License

ezregex is distributed under the terms of both

- [MIT License](https://choosealicense.com/licenses/mit)
- [Apache License, Version 2.0](https://choosealicense.com/licenses/apache-2.0)

at your option.
