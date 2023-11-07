# EZRegex
An readable and intuitive way to generate Regular Expressions

Try my new frontend for this library at https://ezregex.streamlit.app/!

TLDR: This is to regular expressions what CMake is to makefiles

**Table of Contents**
* [Usage](#usage)
* [Installation](#installation)
* [Explanation](#Explanation)
* [Limitations](#current_limitations)
* [Documentation](#documentation)
* [ToDo](#todo)
* [License](#license)

## Usage

Quickstart
```python
from ezregex import *
number + optional(whitespace) + word
# Matches `123abc` and `123 abc`
# but not `abc123` or  `foo bar`
```

Importing as a named package is recommended, as many of the functions have common names
```python
import ezregex as er
# ow is part of er already as optional whitespace
params = er.group(er.atLeastNone(er.ow + er.word + er.ow + er.optional(',') + er.ow))
function = er.word + er.ow + '(' + params + ')'
re.search('some string containing func( param1 , param2)', str(function))
# or the test() method is super helpful (if I don't say so myself)
function.test('this should match func(param1,\tparam2 ), foo(), and bar( foo,)')
```
```markdown
╭───────────────────────────────────────────────── Testing Regex ─────────────────────────────────────────────────╮
│ Testing expression:                                                                                             │
│         \w+(?:\s+)?\(((?:(?:\s+)?\w+(?:\s+)?,?(?:\s+)?)*)\)                                                     │
│ for matches in:                                                                                                 │
│         this should match func(param1, param2 ), foo(), and bar( foo,)                                          │
│                                                                                                                 │
│ Match = "func(param1, param2 )" (18:39)                                                                         │
│ Unnamed Groups:                                                                                                 │
│         1: "param1, param2 " (23:38)                                                                            │
│                                                                                                                 │
│ Match = "foo()" (41:46)                                                                                         │
│ Unnamed Groups:                                                                                                 │
│         1: "" (45:45)                                                                                           │
│                                                                                                                 │
│ Match = "bar( foo,)" (52:62)                                                                                    │
│ Unnamed Groups:                                                                                                 │
│         1: " foo," (56:61)                                                                                      │
│                                                                                                                 │
╰──────────────────────────────────────────────────── Found  ─────────────────────────────────────────────────────╯
```


## Installation
ezregex is distributed on [PyPI](https://pypi.org) as a universal
wheel and is available on Linux/macOS and Windows and supports
Python 3.10+ and PyPy.

```bash
$ pip install ezregex
```

## Explanation of How it Works
Everything relies on the EZRegexMember class. In the \__init\__ file of the package, I have defined a ton of pre-made EZRegexMembers which mimic all (or at least as many as I can) fundamental parts of the regex syntax, plus a few others which are common combinations (like chunk or whitechunk). These have operators overloaded so you can combine them in intuitive ways and call them by intuitive names. All EZRegexMembers take a function parameter (or a string which gets converted to a function for convenience), which gets called with the current regex expression and any parameters passed along when the instance gets called with the () operator. That way you can add things to the front or back of an expression for example, and you can change what exactly gets added to the current expression based on other parameters. You can also chain strings together, and pass them as parameters to other EZRegexMembers, which auto-compiles them and adds them appropriately.

I also have everything which could capture a group capture it passively, except for actual group operators, and always have the (?m) (multiline) flag automatically asserted whenever lineStartsWith/lineEndsWith are used so as to differentiate between capturing at the beginning/end of a string and the beginning/end of a line.

## Current limitations
- inverse() is not totally functional yet. It's close, but has a couple bugs I haven't yet figured out. It's very useful, but try not to rely on it *too* much
- I had previously included seperate dialects of the regex syntax, but ultimately decided it was too much effort and complication to maintain, so I did away with it and it only produces Python-style regex now.
- Not quite all of the regex syntax is implemented yet, though it's close. See the ToDo section

## Documentation
### Notes and Gotchas
- When using the re library, functions like search() and sub() don't accept EZRegexMembers as valid regex patterns. Be sure to call either .str() or .compile() when passing to those. Also, be careful to call the function on the entire pattern: chunk + whitespace.str() is not the same as (chunk isEx+ whitespace).str().
- The `input` parameter can accept strings, other EZRegexMembers, or entire sequences of EZRegex patterns.
- A few of these have `greedy` and `possessive` optional parameters. They can be useful, but can get complicated. Refer to https://docs.python.org/3/library/re.html for details.
- In future versions, conditionals may change to taking in 2 parameters (the current pattern, and their associated condition) instead
- In regular Regex, a lot of random things capture groups for no reason. I find this annoying. All regexes in EZRegex intentionally capture passively, so to capture any groups, use group() or namedGroup().
- All EZRegexMembers (except for raw) auto-sanitize strings given to them, so there's no need to escape braces or question marks and the like. This *does* mean, however, that you cannot pass actual regex strings to any of them, as they'll think you're talking about it literally. To include already written regex strings, use raw
- Note that I have camelCase and snake_case versions of each of the functions, because I waver back and forth between which I like better. Both versions function identically.
### Matching
- literal(input)
    - This is a redundant function. You should always be able to use "... + 'stuff'" just as easily as "... + match('stuff')"
- isExactly(input)
    - This matches the string if and only if the entire string is exactly equal to `input`
### Amounts
- matchMax(input='')
    - Match as many of `input` in the string as you can. If `input` is not provided, it works on the previous regex pattern. That's not recommended for clarity's sake though
- matchNum(num, input='')
    - Match `num` amount of `input` in the string
- matchMoreThan(min, input='')
    - Match more than `min` sequences of `input` in the string
- matchAtLeast(min, input='')
    - Match at least `min` sequences of `input` in the string
- matchRange(min, max, input='', greedy=True, possessive=False)
    - Match between `min` and `max` sequences of `input` in the string.
### Optionals
- optional(input='', greedy=True, possessive=False)
    - Match `input` if it's in string, otherwise still match.
- atLeastOne(input='', greedy=True, possessive=False)
    - Match at least one of `input` in the string.
- atLeastNone(input='', greedy=True, possessive=False)
    - Match 0 or more sequences of `input`
- either(input, or_input)
- anyBetween(char, and_char)
    - Match any char between `char` and `and_char`, using the ASCII table for reference
- anyOf(*inputs, chars=None, split=None)
    - Match any of the given `inputs`. Note that `inputs` can be multiple parameters, or a single string. If char is set to True, then `inputs` must only be a single string, and it interprets `inputs` as characters, and splits it up to find any of the chars in the string. If split is set to true, it forces the ?(...) regex syntax instead of the \[...\] syntax. It should act the same way, but your output regex will look different. None just means "optimize it for me"
- anyCharExcept(*inputs)
    - This matches any char that is NOT in `inputs`. `inputs` can be multiple parameters, or a single string of chars to split.
- anyExcept(input)
    - Matches anything other than `input`
### Positional
#### These differentiate the *string* starting with a sequence, and a *line* starting with a sequence. Do note that the start of the string is also the start of a line. These can also be called without parameters to denote the start/end of a string/line without something specific having to be next to it.
- stringStartsWith(input='') / stringStart
- stringEndsWith(input='') / stringEnd
- lineStartsWith(input='') / lineStart
- lineEndsWith(input='') / lineEnd
### Single CharactersMatches
- whitespace
- whitechunk
    - A "chunk" of whitespace. Just any amount of whitespace together
- digit
    - Matches a single digit
- number
    - Matches multiple digits next to each other. Does **not** match negatives or decimals
- word
- wordChar
    - Matches just a single "word character", defined as any letter, number, or _
- anything
    - Matches any single character, except a newline. To also match a newline, use literallyAnything
- chunk
    - A "chunk": Any clump of characters up until the next newline
### Explicit Characters
- spaceOrTab
- newLine
- carriageReturn
- tab
- space
- quote
- verticalTab
- formFeed
- comma
- period
### Not Chuncks
- notWhitespace
- notDigit
- notWord
### Sets
- uppercase
    - Matches just uppercase letters
- lowercase
    - Matches just lowercase letters
- letter
    - Matches just a letter -- not numbers or _ like wordChar.
- hexDigit
- octDigit
- controller
    - Matches a metadata ASCII characters
- printable
    - Matches printable ASCII characters
- printableAndSpace
- unicode(name)
    - Matches a unicode character by name
### Conditionals
- ifProceededBy(condition)
    - Matches the prior pattern if it has `condition` coming after it
- ifNotProceededBy(condition)
    - Matches the prior pattern if it does **not** have `condition` coming after it
- ifPrecededBy(condition)
    - Matches the prior pattern if it has `condition` coming before it
- ifNotPreceededBy(condition)
    - Matches the prior pattern if it does **not** have `condition` coming before it
- ifEnclosedWith(open, stuff, close)
    - Matches if the string has `open`, then `stuff`, then `close`, but only "matches" stuff. Just a combination of ifProceededBy and ifPreceededBy.
### Groups
- group(chain)
    - Causes `chain` to be captured as an unnamed group. Only useful for replacing regexs
- passiveGroup(chain)
    - As all regexs in EZRegex capture passively, this is entirely useless. But if you really want to, here it is
- namedGroup(name, chain)
    - Causes `chain` to be captured as a named group, with the name `name`. Only useful for replacing regexs
### Flags
#### These shadow python regex flags, and can just as easily be specified directly to the re library instead. They're provided here for compatibility with other regex dialects. See https://docs.python.org/3/library/re.html#flags for details
- ASCII
- DOTALL
- IGNORECASE
- LOCALE
- MULTILINE
- UNICODE
### Misc.
- raw(regex)
    - If you already have some regular regex written, and you want to incorperate it, this will allow you to include it without sanatizing all the backslaches and such, which all the other EZRegexMembers do automatically.
### Replace syntax
#### In the intrest of "I don't want to think about any syntax at all", I have included replace members. Do note that they are **not** interoperable with the other EZRegexMembers, and can only be used with other strings and each other.
- replace_group(num_or_name)
    - Puts in its place the group specified, either by group number (for unnamed groups) or group name (for named groups). Named groups are also counted by number, I'm pretty sure. Groups are numbered starting from 1.
- replace_entire
    - Puts in its place the entire match
### Useful Combinations
#### These are some useful combinations that may be commonly used. They are not as stable, and may be changed and added to in later versions to make them more accurate
- literallyAnything
    - *Any* character, include newline
- signed
    - a signed number, including 123, -123, and +123
- unsigned
    - Same as number. Will not match +123
- plain_float
    - Will match 123.45 and 123.
- full_float
    - Will match plain_float as well as things like 1.23e-10 and 1.23e+10
- int_or_float
    - Exactly what it sounds like
- ow
    - "Optional Whitechunk"
- email
    - Matches an email

## ToDo
See https://docs.python.org/3/library/re.html for details
- (?>...)
    - Attempts to match ... as if it was a separate regular expression, and if successful, continues to match the rest of the pattern following it.
- (?P=name)
    - A backreference to a named group; it matches whatever text was matched by the earlier group named name.
- \b
    - Matches the empty string, but only at the beginning or end of a word.
- \B
    Matches the empty string, but only when it is not at the beginning or end of a word.
- (?(id/name)yes-pattern|no-pattern)
    - Will try to match with yes-pattern if the group with given id or name exists, and with no-pattern if it doesn’t.
- \number
    - Matches the contents of the group of the same number.

## License
ezregex is distributed under the [MIT License](https://choosealicense.com/licenses/mit)
