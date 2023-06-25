# ezregex
An readable and intuitive way to generate Regular Expressions

TLDR: This is to regular expressions what CMake is to makefiles


**Table of Contents**
* [Usage](#usage)
* [Installation](#installation)
* [Explanation](#Explanation)
* [Limitations](#current_limitations)
* [License](#license)

## Usage:
Importing as a named package is recommended, as many of the functions have common names
```python
import ezregex as er
ow = er.optional(er.whitechunk)
optionalParams = er.anyof(ow + er.group(er.optional(er.chunk)) + ow + ',')
function = er.stuff + 'func(' + er.ifFollowedBy(optionalParams) + ')'
function.test('this should match only the func(param1, param2 ) part of this string')
# or
re.search('some string containing func( param1 , param2)', function.compile())
```

## Installation
ezregex is distributed on [PyPI](https://pypi.org) as a universal
wheel and is available on Linux/macOS and Windows and supports
Python 3.10+ and PyPy.

```bash
$ pip install ezregex
```

## Explanation of How it Works
Everything relies on the EZRegexMember class. In the __init__ file of the package, I have defined a ton of pre-made EZRegexMembers which mimic all (or at least as many as I can) fundamental parts of the regex syntax, plus a few others which are common combinations (like chunk or whitechunk). These have operators overloaded so you can combine them in intuitive ways and call them by intuitive names. All EZRegexMembers take a function parameter (or a string which gets converted to a function for convenience), which gets called with the current regex expression and any parameters passed along when the instance gets called with the () operator. That way you can add things to the front or back of an expression for example, and you can change what exactly gets added to the current expression based on other parameters. You can also chain strings together, and pass them as parameters to other EZRegexMembers, which auto-compiles them and adds them appropriately.

I also have everything which could capture a group capture it passively, except for actual group operators, and always have the (?m) (multiline) flag automatically asserted whenever lineStartsWith/lineEndsWith are used so as to differentiate between capturing at the beginning/end of a string and the beginning/end of a line.

## Current limitations
- inverse() is not totally functional yet. It's close, but has a couple bugs I haven't yet figured out.
- I had previously included seperate dialects of the regex syntax, but ultimately decided it was too much effort and complication to maintain, so I did away with it and it only produces Python-style regex now.
- Not quite all of the regex syntax is implemented yet, though it's close

## License
ezregex is distributed under the [MIT License](https://choosealicense.com/licenses/mit)
