<div align="center">
    <img src="https://ezregex.org/favicon.png">
    <br>
    <br>
    <a href="https://github.com/smartycope/ezregex/actions/workflows/tests.yml">
        <img src="https://github.com/smartycope/ezregex/actions/workflows/tests.yml/badge.svg" alt="Unit Tests">
    </a>
    <a href="https://pypi.org/project/ezregex/">
        <img src="https://img.shields.io/pypi/v/ezregex.svg" alt="PyPI Latest Release">
    </a>
    <a href="https://choosealicense.com/licenses/mit/">
        <img src="https://img.shields.io/github/license/smartycope/ezregex">
    </a>
    <!-- <a href="https://www.python.org/">
        <img src="https://img.shields.io/pypi/implementation/ezregex">
    </a> -->
    <!-- <a href="https://pypi.org/project/ezregex/#files">
        <img src="https://img.shields.io/pypi/format/ezregex">
    </a> -->
    <img src="https://img.shields.io/badge/dependencies-0-blue">
</div>
<div align="center">
    <img src="https://img.shields.io/badge/Supported%20Dialects-4-green">
    <img src="https://img.shields.io/badge/Python%20Dialect-100%25-blue">
    <img src="https://img.shields.io/badge/R%20Dialect-100%25-blue">
    <img src="https://img.shields.io/badge/JavaScript%20Dialect-90%25-blue">
    <img src="https://img.shields.io/badge/PCRE2%20Dialect-60%25-yellow">
    <img src="https://img.shields.io/badge/Rust%20Dialect-0%25-red">
</div>


# EZRegex
A readable and intuitive way to write Regular Expressions without having to know any of the syntax

* Frontend for this library: [ezregex.org](https://ezregex.org/)
* Documentation: [ezregex.readthedocs.io](https://ezregex.readthedocs.io/en/latest/)

### **Table of Contents**
* [Usage](#usage)
* [Invert](#inverting)
* [Generate](#generation)
* [Functions vs Methods](#functions-vs-methods)
* [Dialects](#dialects)
* [Documentation](https://ezregex.readthedocs.io/en/latest/)
* [Developer Docs](https://ezregex.readthedocs.io/en/latest/dev_docs/)
* [Installation](#installation)
* [Todos](https://github.com/smartycope/ezregex/issues)
* [License](#license)
* [Credits](#credits)

## Usage

### Quickstart

TLDR: This is to regular expressions what CMake is to makefiles

```python
from ezregex import *

'foo' + number + optional(whitespace) + group(word)
# Or if you prefer the method syntax (they can be mixed)
number.append(whitespace.optional).prepend('foo').append(word.group())

# These match `foo123abc` and `foo123 abc`
# but not `abc123foo` or  `foo bar`
```

Importing as a named package is recommended if you're using it in a larger project
```python
import ezregex as ez

# ow is part of ez already as "optional chunk of whitespace" (`\s*`)
params = ez.group(ez.atLeastNone(ez.ow + ez.word + ez.ow + ez.optional(',') + ez.ow))
# Seperate parts as variables for cleaner patterns
function = ez.word + ez.ow + '(' + params + ')'

# Automatically calls the re.search() function for you
function % 'some string containing func( param1 , param2)'

# The test() method is helpful for debugging, and color codes groups for you
function.test('this should match func(param1,\tparam2 ), foo(), and bar( foo,)')
```
.test() will print all the matches, color coded to match and group (colors not shown here):

```
╭───────────────────────────── Testing Regex ──────────────────────────────╮
│ Testing expression:                                                      │
│         \w+(?:\s+)?\(((?:(?:\s+)?\w+(?:\s+)?,?(?:\s+)?)*)\)              │
│ for matches in:                                                          │
│         this should match func(param1,  param2 ), foo(), and bar( foo,)  │
│                                                                          │
│ Match = "func(param1,  param2 )" (18:39)                                 │
│ Unnamed Groups:                                                          │
│         1: "param1, param2 " (23:38)                                     │
│                                                                          │
│ Match = "foo()" (41:46)                                                  │
│ Unnamed Groups:                                                          │
│         1: "" (45:45)                                                    │
│                                                                          │
│ Match = "bar( foo,)" (52:62)                                             │
│ Unnamed Groups:                                                          │
│         1: " foo," (56:61)                                               │
│                                                                          │
│                                                                          │
╰───────────────────────────────── Found  ─────────────────────────────────╯
```

<!-- This is all colored properly, if anything supported it
<pre>
╭───────────────────────────── Testing Regex ──────────────────────────────╮
│ Testing expression:                                                      │
│         \w+(?:\s+)?\(((?:(?:\s+)?\w+(?:\s+)?,?(?:\s+)?)*)\)              │
│ for matches in:                                                          │
│         this should match<span style="color: teal;">func(</span><span style="background-color: gray; color: teal;">param1,  param2 </span><span style="color: teal;">)</span>, <span style="color: red;">foo()</span>, and <span style="color: orange;">bar(</span><span style="background-color: green; color: orange;"> foo,</span><span style="color: orange;">)</span>   │
│                                                                          │
│ Match = "<span style="color: teal;">func(</span><span style="background-color: gray; color: teal;">param1,  param2 </span><span style="color: teal;">)</span>" (18:39)                                 │
│ Unnamed Groups:                                                          │
│         1: "<span style="color: gray;">param1,     param2 </span>" (23:38)                                 │
│                                                                          │
│ Match = "<span style="color: red;">foo()</span>" (41:46)                                                  │
│ Unnamed Groups:                                                          │
│         1: "" (45:45)                                                    │
│                                                                          │
│ Match = "<span style="color: orange;">bar(</span><span style="background-color: green; color: orange;"> foo,</span><span style="color: orange;">)</span>" (52:62)                                             │
│ Unnamed Groups:                                                          │
│         1: "<span style="color: green;"> foo,</span>" (56:61)                                               │
│                                                                          │
│                                                                          │
╰───────────────────────────────── <span style="color: blue;">Found</span>  ─────────────────────────────────╯
</pre>
-->


## Inverting
The `invert` function (available as ez.invert(`expression`), `expression`.invert(), or ~`expression`) is useful for debugging. You pass it an expression, and it returns an example of a string that is guaranteed to match the provided expression.

## Generation
In version v1.7.0 we introduced a new function: `generate_regex`. It takes in 2 sets of strings, and returns a regular expression that will match everything in the first set and nothing in the second set. It may be a bit crude, but it can be a good starting point if you don't know where to start. It's also really good at [regex golf](http://regex.alf.nu/).

## Functions vs Methods
As of v2.1.0, *elemental methods* were added to EZRegex objects. These shadow their function element counterparts exactly and work the same way, they're just for convenience and preference.

For example, these are all equivelent:
```python
# Element functions
optional(whitespace) + group(either(repeat('a'), 'b')) + if_followed_by(word)
# Elemental methods
whitespace.optional.append(literal('a').repeat.or_('b').unnamed).if_followed_by(word)
# Mixed
whitespace.optional + repeat('a').or_('b').unnamed + if_followed_by(word)
```

## Dialects
As of version v1.6.0, the concepts of *dialects* was introduced. Different languages often have slight variations on the regular expression syntax. As this library is meant to be language independent (even though it's written in Python), you should be able to compile regular expressions to work with other languages as well. To do that, you can simply import all the elements as a sub-package, and they should work identically, although some languages may not have the same features as others.
```python
>>> import ezregex as ez # The python dialect is the defualt dialect
>>> ez.group(digit, 'name') + ez.earlier_group('name')
EZRegex("(?P<name>\d)(?P=name)")
>>> import ezregex.pcre2 as ez
>>> ez.group(digit, 'name') + ez.earlier_group('name')
EZRegex("?P<name>\d)(\g<name>")
```

The currently implemented dialects are:
| Dialect    | Completeness | Tests pass |
|------------|--------------|------------|
| Python     | ~99%         | Yes        |
| JavaScript | ~90%         | Yes        |
| PCRE2      | ~60%         | Yes        |
| R          | 100%         | Yes        |
| Rust       | 0%           | No         |

Just because a dialect is implemented, doesn't mean it has all the features of the language. However, everything implemented is tested, so if you can import it, it's usable.

If you know a particular flavor of regex and would like to contribute, feel free to read the [developer documentation](#developer-documentation) and make a pull request! If you would like one that's not implemented yet, you can also add a [github issue](https://github.com/smartycope/ezregex/issues).

## Utilities
All the functions in the Python `re` library (`search`, `match`, `sub`, etc.) are implemented in the Python EZRegex dialect, and act identically to their equivalents. If you still want to use the Python `re` library directly, note that functions like `search` and `sub` don't accept EZRegex patterns as valid regex. Be sure to either call .str() (or cast it to a string) or .compile() (to compile to an re.Pattern) when passing to those. Using the member functions however, will be more efficient, as EZRegex caches the compiled re.Pattern internally.

There's also an api function, which acts like an API endpoint for regular expressions. This is used by the EZRegex frontend, as it loads this library locally in the browser. It made sense to put it in the library itself, becasue it could be useful for other purposes.

## Installation
EZRegex is distributed on [PyPI](https://pypi.org) as a pure-python universal wheel with no dependencies and is available on Linux, macOS and Windows and supports Python 3.10+ and PyPy.

```bash
pip install ezregex
```

The import name is the same as the package name:
```python
import ezregex as ez
```

## License
EZRegex is distributed under the [MIT License](https://choosealicense.com/licenses/mit)

## Contributing
I love contributions! I don't have many rules for contributing. I just ask that if you're going to add a dialect, before you open a PR, please set up tests for it, and make sure they pass. It doesn't have to be fully implemented, but it should at least be a valid framework to build off of.

## Credits
This library was written from scratch entirely by Copeland Carter.
Inspirations for this project include:

- [PyParsing](https://github.com/pyparsing/pyparsing)
    - I stole a bunch of the operators (especially the [] operator) from them, though we happened upon the same basic structure independantly (convergent evolution, anyone?)
- [regular-expressions.info](https://www.regular-expressions.info/refflavors.html)
    - Their reference is where I got a lot of the other regex flavors
- [human-regex](https://github.com/fleetingbytes/human-regex)
    - Gave me the idea for including element methods, instead of solely element functions
<!-- TODO: credit Peter Norvig here for generation -->

<!--
To publish on PyPI, run:
1. Ensure all the versions have been updated
2. hatch build
3. hatch publish
4. (optional) hatch clean
 -->