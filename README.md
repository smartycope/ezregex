<div align="center">
    <img src="https://ezregex.org/favicon.png">
    <br>
    <br>
    <a href="https://github.com/smartycope/ezregex/actions/workflows/unit-tests.yml">
        <img src="https://github.com/smartycope/ezregex/actions/workflows/unit-tests.yml/badge.svg" alt="Unit Tests">
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
    <img src="https://img.shields.io/badge/Supported%20Dialects-3-green">
    <img src="https://img.shields.io/badge/Python%20Dialect-100%25-blue">
    <img src="https://img.shields.io/badge/JavaScript%20Dialect-50%25-yellow">
    <img src="https://img.shields.io/badge/Perl%20Dialect-20%25-red">
</div>


# EZRegex
A readable and intuitive way to make Regular Expressions without having to know any of the syntax

Try the frontend for this library at [ezregex.org](https://ezregex.org/)!

TLDR: This is to regular expressions what CMake is to makefiles

### **Table of Contents**
* [Usage](#usage)
* [Invert](#inverting)
* [Generate](#generation)
* [Dialects](#dialects)
* [Documentation](#documentation)
* [Developer Docs](#developer-documentation)
* [Installation](#installation)
* [Todo](#todo)
* [License](#license)

## Usage

Quickstart
```python
from ezregex import *
'foo' + number + optional(whitespace) + word
# Matches `foo123abc` and `foo123 abc`
# but not `abc123foo` or  `foo bar`
```

Importing as a named package is recommended
```python
import ezregex as er

# ow is part of er already as optional whitespace
params = er.group(er.atLeastNone(er.ow + er.word + er.ow + er.optional(',') + er.ow))
# Seperate parts as variables for cleaner patterns
function = er.word + er.ow + '(' + params + ')'

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
The `invert` function (available as er.invert(`expression`), `expression`.invert(), or ~`expression`) is useful for debugging. You pass it an expression, and it returns an example of a string that is guaranteed to match the provided expression.


## Generation
In version 1.7.0 we introduced a new function: `generate_regex`. It takes in 2 sets of strings, and returns a regular expression that will match everything in the first set and nothing in the second set. It may be a bit crude, but it can be a good starting point if you don't know where to start. It's also really good at [regex golf](http://regex.alf.nu/).


## Dialects
As of version 1.6.0, the concepts of *dialects* was introduced. Different languages often have slight variations on the regular expression syntax. As this library is meant to be language independent (even though it's written in Python), you should be able to compile regular expressions to work with other languages as well. To do that, you can simply import all the elements as a sub-package, and they should work identically, although some languages may not have the same features as others.
```python
>>> import ezregex as er # The python dialect is the defualt dialect
>>> er.group(digit, 'name') + er.earlier_group('name')
EZRegex("(?P<name>\d)(?P=name)")
>>> import ezregex.perl as er
>>> er.group(digit, 'name') + er.earlier_group('name')
EZRegex("?P<name>\d)(\g<name>")
```

The currently implemented dialects are:
- Python
    - Well tested, ~99% implemented
- JavaScript
    - Under active development, the basics *should* work, though tests aren't in place yet
- Perl
    - Next on the roadmap, technically importable, but not implemented yet

If you know a particular flavor of regex and would like to contribute, feel free to read the [developer documentation](#developer-documentation) and make a pull request! If you would like one that's not implemented yet, you can also add a [github issue](https://github.com/smartycope/ezregex/issues).

## Documentation
### Notes and Gotchas
- The different Regular Expression dialects don't all have the same features, and those features don't all work the same way. I've tried to standardize these as best I can and use reasonable names for all the elements. If you're confused by something not working as expected, be sure to understand how your language specifically handles regular expressions.
- When using the Python `re` library, functions like re.search() and re.sub() don't accept EZRegex patterns as valid regex. Be sure to either call .str() (or cast it to a string) or .compile() (to compile to an re.Pattern) when passing to those. Also, be careful to call the function on the entire pattern: chunk + whitespace.str() is not the same as (chunk + whitespace).str().
- In regular regex, a lot of random things capture groups for no apparent reason. All regexes in EZRegex intentionally capture passively, so to capture any groups, use group(), with the optional `name` parameter.
- All EZRegexs (except for `raw`) auto-sanitize strings given to them, so there's no need to escape characters or use r strings. This *does* mean, however, that you cannot pass actual regex strings to any of them, as they'll think you're talking about it literally (unless you want that, of course). To include already written regex strings, use `raw`
- Note that I have camelCase and snake_case versions of each of the functions, because I waver back and forth between which I like better. Both versions function identically.
- The `InputType` can accept strings, other EZRegexs, or entire sequences of EZRegex patterns. It can also accept things that can be cast to a string, but it will warn you when it does, so it's better to cast to a string yourself.
- The `invert` function can accept any regular expression, not just EZRegex expressions, if you want to use it independently of the rest of the library.

<!-- Start of generated docs -->
<details>
	<summary><strong><u>perl</u></strong></summary><details>
	<summary>Positionals</summary>

#### These differentiate the *string* starting with a sequence, and a *line* starting with a sequence. Do note that the startof the string is also the start of a line. These can also be called without parameters to denote the start/end of astring/line without something specific having to be next to it.
- string_starts_with
- string_ends_with
- line_starts_with
- line_ends_with
- word_boundary
	- Matches the boundary of a word, i.e. the empty space between a word character and not a word character, or the end of a string
- not_word_boundary
	- The opposite of `wordBoundary`

</details>

<details>
	<summary>Literals</summary>

####
- tab
- space
- space_or_tab
- new_line
- carriage_return
- quote
	- Matches ', ", and `
- vertical_tab
- form_feed
- comma
- period
- underscore

</details>

<details>
	<summary>Not Literals</summary>

####
- not_whitespace
- not_digit
- not_word

</details>

<details>
	<summary>Catagories</summary>

####
- whitespace
- whitechunk
	- A "chunk" of whitespace. Just any amount of whitespace together
- digit
- number
	- Matches multiple digits next to each other. Does not match negatives or decimals
- word
- word_char
	- Matches just a single "word character", defined as any letter, number, or _
- anything
	- Matches any single character, except a newline. To also match a newline, use literally_anything
- chunk
	- A "chunk": Any clump of characters up until the next newline
- uppercase
- lowercase
- letter
	- Matches just a letter -- not numbers or _ like word_char
- hex_digit
- oct_digit
- punctuation
- controller
	- Matches a metadata ASCII characters
- printable
	- Matches printable ASCII characters
- printable_and_space
- alpha_num
- unicode
	- Matches a unicode character by name
- any_between(char: str, and_char: str)
	- Match any char between `char` and `and_char`, using the ASCII table for reference

</details>

<details>
	<summary>Amounts</summary>

####
- match_max(input: InputType)
	- Match as many of `input` in the string as you can. This is equivelent to using the unary + operator.
If `input` is not provided, it works on the previous regex pattern. That's not recommended for
clarity's sake though
- match_num(num: int, input: InputType)
	- Match `num` amount of `input` in the string
- match_more_than(min: int, input: InputType)
	- Match more than `min` sequences of `input` in the string
- match_at_least(min: int, input: InputType)
	- Match at least `min` sequences of `input` in the string
- match_at_most(max: int, input: InputType)
	- Match at most `max` instances of `input` in the string
- match_range(min: int, max: int, input: InputType, greedy: bool=True, possessive: bool=False)
	- Match between `min` and `max` sequences of `input` in the string. This also accepts `greedy` and `possessive` parameters
Max can be an empty string to indicate no maximum
`greedy` means it will try to match as many repititions as possible
non-greedy will try to match as few repititions as possible
`possessive` means it won't backtrack to try to find any repitions
see https://docs.python.org/3/library/re.html for more help
- at_least_one(input: InputType, greedy: bool=True, possessive: bool=False)
	- Match at least one of `input` in the string. This also accepts `greedy` and `possessive` parameters
`greedy` means it will try to match as many repititions as possible
non-greedy will try to match as few repititions as possible
`possessive` means it won't backtrack to try to find any repitions
see https://docs.python.org/3/library/re.html for more help
- at_least_none(input: InputType, greedy: bool=True, possessive: bool=False)
	- Match 0 or more sequences of `input`. This also accepts `greedy` and `possessive` parameters
`greedy` means it will try to match as many repititions as possible
non-greedy will try to match as few repititions as possible
`possessive` means it won't backtrack to try to find any repitions
see https://docs.python.org/3/library/re.html for more help

</details>

<details>
	<summary>Choices</summary>

####
- optional(input: InputType, greedy: bool=True, possessive: bool=False)
	- Match `input` if it's there. This also accepts `greedy` and `possessive` parameters
`greedy` means it will try to match as many repititions as possible
non-greedy will try to match as few repititions as possible
`possessive` means it won't backtrack to try to find any repitions
see https://docs.python.org/3/library/re.html for more help
- either(input: InputType, or_input: InputType)
- any_of(*inputs: str, chars: bool | None=None, split: bool | None=None)
	- Match any of the given `inputs`. Note that `inputs` can be multiple parameters,
or a single string. Can also accept parameters chars and split. If char is set
to True, then `inputs` must only be a single string, it interprets `inputs`
as characters, and splits it up to find any of the chars in the string. If
split is set to true, it forces the ?(...) regex syntax instead of the [...]
syntax. It should act the same way, but your output regex will look different.
By default, it just optimizes it for you.
- any_char_except(*inputs: str)
	- This matches any char that is NOT in `inputs`. `inputs` can be multiple parameters, or a single string of chars to split.
- any_except(input: InputType, type: InputType='.*')
	- Matches anything other than `input`, which must be a single string or EZRegex chain, **not** a list. Also
optionally accepts the `type` parameter, which works like this: "Match any `type` other than `input`". For example,
"match any word which is not foo". Do note that this function is new, and I'm still working out the kinks.
- each(*inputs: InputType)
	- Matches if the next part of the string can match all of the given inputs. Like the + operator, but out of order.

</details>

<details>
	<summary>Conditionals</summary>

#### These can only be used once in a given expression. They only match a given expression if the expression is/ins'tfollowed/preceeded by a the given pattern
- if_proceded_by(input: InputType)
	- Matches the pattern if it has `input` coming after it. Can only be used once in a given pattern,
as it only applies to the end
- if_not_proceded_by(input: InputType)
	- Matches the pattern if it does **not** have `input` coming after it. Can only be used once in
a given pattern, as it only applies to the end
- if_preceded_by(input: InputType)
	- Matches the pattern if it has `input` coming before it. Can only be used once in a given pattern,
as it only applies to the beginning
- if_not_preceded_by(input: InputType)
	- Matches the pattern if it does **not** have `input` coming before it. Can only be used once
in a given pattern, as it only applies to the beginning
- if_enclosed_with(open: str, stuff: InputType, close: str | None=None)
	- Matches if the string has `open`, then `stuff`, then `close`, but only "matches"
stuff. Just a convenience combination of ifProceededBy and ifPreceededBy.

</details>

<details>
	<summary>Grouping</summary>

####
- group(input: InputType, name: str | None=None)
	- Causes `input` to be captured as an unnamed group. Only useful when replacing regexs
- passive_group(input: InputType)
	- As all regexs in EZRegex capture passively, this is entirely useless. But if you really want to, here it is
- earlier_group(num_or_name: int | str)
	- Matches whatever the group referenced by `num_or_name` matched earlier. Must be *after* a
group which would match `num_or_name`
- if_exists(num_or_name: int | str, does: InputType, doesnt: InputType | None=None)
	- Matches `does` if the group `num_or_name` exists, otherwise it matches `doesnt`

</details>

<details>
	<summary>Replacement</summary>

#### In the intrest of "I don't want to think about any syntax at all", I have included replace members. Do note that theyare not interoperable with the other EZRegexs, and can only be used with other strings and each other.
- rgroup(num_or_name: str | int)
	- Puts in its place the group specified, either by group number (for unnamed
groups) or group name (for named groups). Named groups are also counted by
number, I'm pretty sure. Groups are numbered starting from 1
- replace_entire
	- Puts in its place the entire match
- replace(string: str, rtn_str: bool=True) -> str | EZRegex
	- Generates a valid regex replacement string, using Python f-string like syntax.

Example:
    ``` replace("named: {group}, numbered: {1}, entire: {0}") ```

Like Python f-strings, use {{ and }} to specify { and }

Set the `rtn_str` parameter to True to have it return an EZRegex type instead of a string

Note: Remember that index 0 is the entire match

There's a few of advantages to using this instead of just the regular regex replacement syntax:
- It's consistent between dialects
- It's closer to Python f-string syntax, which is cleaner and more familiar
- It handles numbered, named, and entire replacement types the same

</details>

<details>
	<summary>Misc</summary>

####
- is_exactly(input: InputType)
	- This matches the string if and only if the entire string is exactly equal to `input`
- literal(input: InputType)
	- This is a redundant function. You should always be able to use `... + 'stuff'` just as easily as `... + literal('stuff')`
- raw(regex: str)
	- If you already have some regular regex written, and you want to incorperate
it, this will allow you to include it without sanatizing all the backslaches
and such, which all the other EZRegexs do automatically

</details>

<details>
	<summary>Premade</summary>

#### These are some useful combinations that may be commonly used. They are not as stable, and may be changed and added to inlater versions to make them more accurate
- literally_anything
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
- ow
	- "Optional Whitechunk"
- email
	- Matches an email
- version
	- The *official* regex for matching version numbers from https://semver.org/. It includes 5 groups that can bematched/replaced: `major`, `minor`, `patch`, `prerelease`, and `buildmetadata`
- version_numbered
	- Same as `version`, but it uses numbered groups for each version number instead of named groups

</details>

<details>
	<summary>Flags</summary>

#### These shadow python regex flags, and can just as easily be specified directly to the re library instead. They're providedhere for compatibility with other regex dialects. See https://docs.python.org/3/library/re.html#flags for details
- ASCII
	- Make matching words, word boundaries, digits, and whitespace perform ASCII-only matching instead of full Unicodematching. This is only meaningful for Unicode (str) patterns, and is ignored for bytes patterns
- IGNORECASE
	- Perform case-insensitive matching, including expressions that explicitly use uppercase members. Full Unicode matching(such as Ü matching ü) also works unless the ASCII flag is used to disable non-ASCII matches. The current locale does notchange the effect of this flag unless the LOCALE flag is also used
- DOTALL
	- Make the '.' special character match any character at all, including a newline. It's recommended you simply useliterally_anything instead
- LOCALE
	- Try not to use this, and rely on unicode matching instead
- MULTILINE
	- This is automatically inserted when using line_start and line_end, you shouldn't need to add it manually
- UNICODE
	- Match using the full unicode standard, instead of just ASCII. Enabled by default, and therefore redundant.

</details>

</details>
<details>
	<summary><strong><u>javascript</u></strong></summary><details>
	<summary>Positionals</summary>

#### These differentiate the *string* starting with a sequence, and a *line* starting with a sequence. Do note that the startof the string is also the start of a line. These can also be called without parameters to denote the start/end of astring/line without something specific having to be next to it.
- string_starts_with
- string_ends_with
- line_starts_with
- line_ends_with
- word_boundary
	- Matches the boundary of a word, i.e. the empty space between a word character and not a word character, or the end of a string
- not_word_boundary
	- The opposite of `wordBoundary`

</details>

<details>
	<summary>Literals</summary>

####
- tab
- space
- space_or_tab
- new_line
- carriage_return
- quote
	- Matches ', ", and `
- vertical_tab
- form_feed
- comma
- period
- underscore

</details>

<details>
	<summary>Not Literals</summary>

####
- not_whitespace
- not_digit
- not_word

</details>

<details>
	<summary>Catagories</summary>

####
- whitespace
- whitechunk
	- A "chunk" of whitespace. Just any amount of whitespace together
- digit
- number
	- Matches multiple digits next to each other. Does not match negatives or decimals
- word
- word_char
	- Matches just a single "word character", defined as any letter, number, or _
- anything
	- Matches any single character, except a newline. To also match a newline, use literally_anything
- chunk
	- A "chunk": Any clump of characters up until the next newline
- uppercase
- lowercase
- letter
	- Matches just a letter -- not numbers or _ like word_char
- hex_digit
- oct_digit
- punctuation
- controller
	- Matches a metadata ASCII characters
- printable
	- Matches printable ASCII characters
- printable_and_space
- alpha_num
- unicode
	- Matches a unicode character by name
- any_between(char: str, and_char: str)
	- Match any char between `char` and `and_char`, using the ASCII table for reference

</details>

<details>
	<summary>Amounts</summary>

####
- match_max(input: InputType)
	- Match as many of `input` in the string as you can. This is equivelent to using the unary + operator.
If `input` is not provided, it works on the previous regex pattern. That's not recommended for
clarity's sake though
- match_num(num: int, input: InputType)
	- Match `num` amount of `input` in the string
- match_more_than(min: int, input: InputType)
	- Match more than `min` sequences of `input` in the string
- match_at_least(min: int, input: InputType)
	- Match at least `min` sequences of `input` in the string
- match_at_most(max: int, input: InputType)
	- Match at most `max` instances of `input` in the string
- match_range(min: int, max: int, input: InputType, greedy: bool=True, possessive: bool=False)
	- Match between `min` and `max` sequences of `input` in the string. This also accepts `greedy` and `possessive` parameters
Max can be an empty string to indicate no maximum
`greedy` means it will try to match as many repititions as possible
non-greedy will try to match as few repititions as possible
`possessive` means it won't backtrack to try to find any repitions
see https://docs.python.org/3/library/re.html for more help
- at_least_one(input: InputType, greedy: bool=True, possessive: bool=False)
	- Match at least one of `input` in the string. This also accepts `greedy` and `possessive` parameters
`greedy` means it will try to match as many repititions as possible
non-greedy will try to match as few repititions as possible
`possessive` means it won't backtrack to try to find any repitions
see https://docs.python.org/3/library/re.html for more help
- at_least_none(input: InputType, greedy: bool=True, possessive: bool=False)
	- Match 0 or more sequences of `input`. This also accepts `greedy` and `possessive` parameters
`greedy` means it will try to match as many repititions as possible
non-greedy will try to match as few repititions as possible
`possessive` means it won't backtrack to try to find any repitions
see https://docs.python.org/3/library/re.html for more help

</details>

<details>
	<summary>Choices</summary>

####
- optional(input: InputType, greedy: bool=True, possessive: bool=False)
	- Match `input` if it's there. This also accepts `greedy` and `possessive` parameters
`greedy` means it will try to match as many repititions as possible
non-greedy will try to match as few repititions as possible
`possessive` means it won't backtrack to try to find any repitions
see https://docs.python.org/3/library/re.html for more help
- either(input: InputType, or_input: InputType)
- any_of(*inputs: str, chars: bool | None=None, split: bool | None=None)
	- Match any of the given `inputs`. Note that `inputs` can be multiple parameters,
or a single string. Can also accept parameters chars and split. If char is set
to True, then `inputs` must only be a single string, it interprets `inputs`
as characters, and splits it up to find any of the chars in the string. If
split is set to true, it forces the ?(...) regex syntax instead of the [...]
syntax. It should act the same way, but your output regex will look different.
By default, it just optimizes it for you.
- any_char_except(*inputs: str)
	- This matches any char that is NOT in `inputs`. `inputs` can be multiple parameters, or a single string of chars to split.
- any_except(input: InputType, type: InputType='.*')
	- Matches anything other than `input`, which must be a single string or EZRegex chain, **not** a list. Also
optionally accepts the `type` parameter, which works like this: "Match any `type` other than `input`". For example,
"match any word which is not foo". Do note that this function is new, and I'm still working out the kinks.
- each(*inputs: InputType)
	- Matches if the next part of the string can match all of the given inputs. Like the + operator, but out of order.

</details>

<details>
	<summary>Conditionals</summary>

#### These can only be used once in a given expression. They only match a given expression if the expression is/ins'tfollowed/preceeded by a the given pattern
- if_proceded_by(input: InputType)
	- Matches the pattern if it has `input` coming after it. Can only be used once in a given pattern,
as it only applies to the end
- if_not_proceded_by(input: InputType)
	- Matches the pattern if it does **not** have `input` coming after it. Can only be used once in
a given pattern, as it only applies to the end
- if_preceded_by(input: InputType)
	- Matches the pattern if it has `input` coming before it. Can only be used once in a given pattern,
as it only applies to the beginning
- if_not_preceded_by(input: InputType)
	- Matches the pattern if it does **not** have `input` coming before it. Can only be used once
in a given pattern, as it only applies to the beginning
- if_enclosed_with(open: str, stuff: InputType, close: str | None=None)
	- Matches if the string has `open`, then `stuff`, then `close`, but only "matches"
stuff. Just a convenience combination of ifProceededBy and ifPreceededBy.

</details>

<details>
	<summary>Grouping</summary>

####
- group(input: InputType, name: str | None=None)
	- Causes `input` to be captured as an unnamed group. Only useful when replacing regexs
- passive_group(input: InputType)
	- As all regexs in EZRegex capture passively, this is entirely useless. But if you really want to, here it is
- earlier_group(num_or_name: int | str)
	- Matches whatever the group referenced by `num_or_name` matched earlier. Must be *after* a
group which would match `num_or_name`
- if_exists(num_or_name: int | str, does: InputType, doesnt: InputType | None=None)
	- Matches `does` if the group `num_or_name` exists, otherwise it matches `doesnt`

</details>

<details>
	<summary>Replacement</summary>

#### In the intrest of "I don't want to think about any syntax at all", I have included replace members. Do note that theyare not interoperable with the other EZRegexs, and can only be used with other strings and each other.
- rgroup(num_or_name: str | int)
	- Puts in its place the group specified, either by group number (for unnamed
groups) or group name (for named groups). Named groups are also counted by
number, I'm pretty sure. Groups are numbered starting from 1
- replace_entire
	- Puts in its place the entire match
- replace(string: str, rtn_str: bool=True) -> str | EZRegex
	- Generates a valid regex replacement string, using Python f-string like syntax.

Example:
    ``` replace("named: {group}, numbered: {1}, entire: {0}") ```

Like Python f-strings, use {{ and }} to specify { and }

Set the `rtn_str` parameter to True to have it return an EZRegex type instead of a string

Note: Remember that index 0 is the entire match

There's a few of advantages to using this instead of just the regular regex replacement syntax:
- It's consistent between dialects
- It's closer to Python f-string syntax, which is cleaner and more familiar
- It handles numbered, named, and entire replacement types the same

</details>

<details>
	<summary>Misc</summary>

####
- is_exactly(input: InputType)
	- This matches the string if and only if the entire string is exactly equal to `input`
- literal(input: InputType)
	- This is a redundant function. You should always be able to use `... + 'stuff'` just as easily as `... + literal('stuff')`
- raw(regex: str)
	- If you already have some regular regex written, and you want to incorperate
it, this will allow you to include it without sanatizing all the backslaches
and such, which all the other EZRegexs do automatically

</details>

<details>
	<summary>Premade</summary>

#### These are some useful combinations that may be commonly used. They are not as stable, and may be changed and added to inlater versions to make them more accurate
- literally_anything
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
- ow
	- "Optional Whitechunk"
- email
	- Matches an email
- version
	- The *official* regex for matching version numbers from https://semver.org/. It includes 5 groups that can bematched/replaced: `major`, `minor`, `patch`, `prerelease`, and `buildmetadata`
- version_numbered
	- Same as `version`, but it uses numbered groups for each version number instead of named groups

</details>

<details>
	<summary>Flags</summary>

#### These shadow python regex flags, and can just as easily be specified directly to the re library instead. They're providedhere for compatibility with other regex dialects. See https://docs.python.org/3/library/re.html#flags for details
- ASCII
	- Make matching words, word boundaries, digits, and whitespace perform ASCII-only matching instead of full Unicodematching. This is only meaningful for Unicode (str) patterns, and is ignored for bytes patterns
- IGNORECASE
	- Perform case-insensitive matching, including expressions that explicitly use uppercase members. Full Unicode matching(such as Ü matching ü) also works unless the ASCII flag is used to disable non-ASCII matches. The current locale does notchange the effect of this flag unless the LOCALE flag is also used
- DOTALL
	- Make the '.' special character match any character at all, including a newline. It's recommended you simply useliterally_anything instead
- LOCALE
	- Try not to use this, and rely on unicode matching instead
- MULTILINE
	- This is automatically inserted when using line_start and line_end, you shouldn't need to add it manually
- UNICODE
	- Match using the full unicode standard, instead of just ASCII. Enabled by default, and therefore redundant.

</details>

</details>
<details>
	<summary><strong><u>python</u></strong></summary><details>
	<summary>Positionals</summary>

#### These differentiate the *string* starting with a sequence, and a *line* starting with a sequence. Do note that the startof the string is also the start of a line. These can also be called without parameters to denote the start/end of astring/line without something specific having to be next to it.
- string_starts_with
- string_ends_with
- line_starts_with
- line_ends_with
- word_boundary
	- Matches the boundary of a word, i.e. the empty space between a word character and not a word character, or the end of a string
- not_word_boundary
	- The opposite of `wordBoundary`

</details>

<details>
	<summary>Literals</summary>

####
- tab
- space
- space_or_tab
- new_line
- carriage_return
- quote
	- Matches ', ", and `
- vertical_tab
- form_feed
- comma
- period
- underscore

</details>

<details>
	<summary>Not Literals</summary>

####
- not_whitespace
- not_digit
- not_word

</details>

<details>
	<summary>Catagories</summary>

####
- whitespace
- whitechunk
	- A "chunk" of whitespace. Just any amount of whitespace together
- digit
- number
	- Matches multiple digits next to each other. Does not match negatives or decimals
- word
- word_char
	- Matches just a single "word character", defined as any letter, number, or _
- anything
	- Matches any single character, except a newline. To also match a newline, use literally_anything
- chunk
	- A "chunk": Any clump of characters up until the next newline
- uppercase
- lowercase
- letter
	- Matches just a letter -- not numbers or _ like word_char
- hex_digit
- oct_digit
- punctuation
- controller
	- Matches a metadata ASCII characters
- printable
	- Matches printable ASCII characters
- printable_and_space
- alpha_num
- unicode
	- Matches a unicode character by name
- any_between(char: str, and_char: str)
	- Match any char between `char` and `and_char`, using the ASCII table for reference

</details>

<details>
	<summary>Amounts</summary>

####
- match_max(input: InputType)
	- Match as many of `input` in the string as you can. This is equivelent to using the unary + operator.
If `input` is not provided, it works on the previous regex pattern. That's not recommended for
clarity's sake though
- match_num(num: int, input: InputType)
	- Match `num` amount of `input` in the string
- match_more_than(min: int, input: InputType)
	- Match more than `min` sequences of `input` in the string
- match_at_least(min: int, input: InputType)
	- Match at least `min` sequences of `input` in the string
- match_at_most(max: int, input: InputType)
	- Match at most `max` instances of `input` in the string
- match_range(min: int, max: int, input: InputType, greedy: bool=True, possessive: bool=False)
	- Match between `min` and `max` sequences of `input` in the string. This also accepts `greedy` and `possessive` parameters
Max can be an empty string to indicate no maximum
`greedy` means it will try to match as many repititions as possible
non-greedy will try to match as few repititions as possible
`possessive` means it won't backtrack to try to find any repitions
see https://docs.python.org/3/library/re.html for more help
- at_least_one(input: InputType, greedy: bool=True, possessive: bool=False)
	- Match at least one of `input` in the string. This also accepts `greedy` and `possessive` parameters
`greedy` means it will try to match as many repititions as possible
non-greedy will try to match as few repititions as possible
`possessive` means it won't backtrack to try to find any repitions
see https://docs.python.org/3/library/re.html for more help
- at_least_none(input: InputType, greedy: bool=True, possessive: bool=False)
	- Match 0 or more sequences of `input`. This also accepts `greedy` and `possessive` parameters
`greedy` means it will try to match as many repititions as possible
non-greedy will try to match as few repititions as possible
`possessive` means it won't backtrack to try to find any repitions
see https://docs.python.org/3/library/re.html for more help

</details>

<details>
	<summary>Choices</summary>

####
- optional(input: InputType, greedy: bool=True, possessive: bool=False)
	- Match `input` if it's there. This also accepts `greedy` and `possessive` parameters
`greedy` means it will try to match as many repititions as possible
non-greedy will try to match as few repititions as possible
`possessive` means it won't backtrack to try to find any repitions
see https://docs.python.org/3/library/re.html for more help
- either(input: InputType, or_input: InputType)
- any_of(*inputs: str, chars: bool | None=None, split: bool | None=None)
	- Match any of the given `inputs`. Note that `inputs` can be multiple parameters,
or a single string. Can also accept parameters chars and split. If char is set
to True, then `inputs` must only be a single string, it interprets `inputs`
as characters, and splits it up to find any of the chars in the string. If
split is set to true, it forces the ?(...) regex syntax instead of the [...]
syntax. It should act the same way, but your output regex will look different.
By default, it just optimizes it for you.
- any_char_except(*inputs: str)
	- This matches any char that is NOT in `inputs`. `inputs` can be multiple parameters, or a single string of chars to split.
- any_except(input: InputType, type: InputType='.*')
	- Matches anything other than `input`, which must be a single string or EZRegex chain, **not** a list. Also
optionally accepts the `type` parameter, which works like this: "Match any `type` other than `input`". For example,
"match any word which is not foo". Do note that this function is new, and I'm still working out the kinks.
- each(*inputs: InputType)
	- Matches if the next part of the string can match all of the given inputs. Like the + operator, but out of order.

</details>

<details>
	<summary>Conditionals</summary>

#### These can only be used once in a given expression. They only match a given expression if the expression is/ins'tfollowed/preceeded by a the given pattern
- if_proceded_by(input: InputType)
	- Matches the pattern if it has `input` coming after it. Can only be used once in a given pattern,
as it only applies to the end
- if_not_proceded_by(input: InputType)
	- Matches the pattern if it does **not** have `input` coming after it. Can only be used once in
a given pattern, as it only applies to the end
- if_preceded_by(input: InputType)
	- Matches the pattern if it has `input` coming before it. Can only be used once in a given pattern,
as it only applies to the beginning
- if_not_preceded_by(input: InputType)
	- Matches the pattern if it does **not** have `input` coming before it. Can only be used once
in a given pattern, as it only applies to the beginning
- if_enclosed_with(open: str, stuff: InputType, close: str | None=None)
	- Matches if the string has `open`, then `stuff`, then `close`, but only "matches"
stuff. Just a convenience combination of ifProceededBy and ifPreceededBy.

</details>

<details>
	<summary>Grouping</summary>

####
- group(input: InputType, name: str | None=None)
	- Causes `input` to be captured as an unnamed group. Only useful when replacing regexs
- passive_group(input: InputType)
	- As all regexs in EZRegex capture passively, this is entirely useless. But if you really want to, here it is
- earlier_group(num_or_name: int | str)
	- Matches whatever the group referenced by `num_or_name` matched earlier. Must be *after* a
group which would match `num_or_name`
- if_exists(num_or_name: int | str, does: InputType, doesnt: InputType | None=None)
	- Matches `does` if the group `num_or_name` exists, otherwise it matches `doesnt`

</details>

<details>
	<summary>Replacement</summary>

#### In the intrest of "I don't want to think about any syntax at all", I have included replace members. Do note that theyare not interoperable with the other EZRegexs, and can only be used with other strings and each other.
- rgroup(num_or_name: str | int)
	- Puts in its place the group specified, either by group number (for unnamed
groups) or group name (for named groups). Named groups are also counted by
number, I'm pretty sure. Groups are numbered starting from 1
- replace_entire
	- Puts in its place the entire match
- replace(string: str, rtn_str: bool=True) -> str | EZRegex
	- Generates a valid regex replacement string, using Python f-string like syntax.

Example:
    ``` replace("named: {group}, numbered: {1}, entire: {0}") ```

Like Python f-strings, use {{ and }} to specify { and }

Set the `rtn_str` parameter to True to have it return an EZRegex type instead of a string

Note: Remember that index 0 is the entire match

There's a few of advantages to using this instead of just the regular regex replacement syntax:
- It's consistent between dialects
- It's closer to Python f-string syntax, which is cleaner and more familiar
- It handles numbered, named, and entire replacement types the same

</details>

<details>
	<summary>Misc</summary>

####
- is_exactly(input: InputType)
	- This matches the string if and only if the entire string is exactly equal to `input`
- literal(input: InputType)
	- This is a redundant function. You should always be able to use `... + 'stuff'` just as easily as `... + literal('stuff')`
- raw(regex: str)
	- If you already have some regular regex written, and you want to incorperate
it, this will allow you to include it without sanatizing all the backslaches
and such, which all the other EZRegexs do automatically

</details>

<details>
	<summary>Premade</summary>

#### These are some useful combinations that may be commonly used. They are not as stable, and may be changed and added to inlater versions to make them more accurate
- literally_anything
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
- ow
	- "Optional Whitechunk"
- email
	- Matches an email
- version
	- The *official* regex for matching version numbers from https://semver.org/. It includes 5 groups that can bematched/replaced: `major`, `minor`, `patch`, `prerelease`, and `buildmetadata`
- version_numbered
	- Same as `version`, but it uses numbered groups for each version number instead of named groups

</details>

<details>
	<summary>Flags</summary>

#### These shadow python regex flags, and can just as easily be specified directly to the re library instead. They're providedhere for compatibility with other regex dialects. See https://docs.python.org/3/library/re.html#flags for details
- ASCII
	- Make matching words, word boundaries, digits, and whitespace perform ASCII-only matching instead of full Unicodematching. This is only meaningful for Unicode (str) patterns, and is ignored for bytes patterns
- IGNORECASE
	- Perform case-insensitive matching, including expressions that explicitly use uppercase members. Full Unicode matching(such as Ü matching ü) also works unless the ASCII flag is used to disable non-ASCII matches. The current locale does notchange the effect of this flag unless the LOCALE flag is also used
- DOTALL
	- Make the '.' special character match any character at all, including a newline. It's recommended you simply useliterally_anything instead
- LOCALE
	- Try not to use this, and rely on unicode matching instead
- MULTILINE
	- This is automatically inserted when using line_start and line_end, you shouldn't need to add it manually

</details>

</details>
<!-- End of generated docs -->
<details>
<summary>Operators</summary>

- `+`, `<<`, `>>`
	- These all do the same thing: combine expressions
- `*`
	- Multiplies an expression a number of times. `expr * 3` is equivelent to `expr + expr + expr`. Can also be used like `expr * ...` is equivalent to `any_amt(expr)`
- `+`
	- A unary + operator acts exactly as a match_max() does, or, if you're familiar with regex syntax, the + operator
- `[]`
	- expr[2, 3] is equivalent to `match_range(2, 3, expr)`
	- expr[2, ...] or expr[2,] is equivalent to `at_least(2, expr)`
	- expr[... , 2] is equivalent to `at_most(2, expr)`
	- expr[...] or expr[0, ...] is equivelent to `at_least_0(expr)`
	- expr[1, ...] is equivalent to `at_least_1(expr)`
- `&`
	- Coming soon! This will work like the + operator, but they can be out of order. Like an and operation.
- `|`
	- Coming soon! This will work like an or operation, which will work just like any_of()
- `%`
    - This automatically calls re.search() for you and returns the match object (or None). Use like this: `(digit * 2) % '99 beers on the wall'`
- `~`
    - This inverts the expression, equivalent to calling the .invert() method
</details>

## Developer Documentation
### The EZRegex class
Everything relies on the EZRegex class. EZRegex shouldn't be instantiated by the user, as each dialect defines their own EZRegex elements specific to that dialect (more on that later). Each element represents a fundamental part of the Regular Expression syntax for that language, as well as less-fundemental common combinations for convenience (like email and float).

EZRegex can accept a string or a function to define how it's supposed to interact with the current "chain" of elements. If it's a string, it just adds it to the end. If it's a function, it can accept any positional or named parameters, but has to accept `cur=...` as the last parameter (it's complicated). The `cur` parameter is the current regular expression chain, as a string. What's returned becomes the new `cur` parameter of the next element, or, if there is no next element, the final regex. That way you can add to the front or back of an expression, and you can change what exactly gets added to the current expression based on other parameters.

The EZRegex class has operators overloaded so you can combine them in intuitive ways and call them by intuitive names.

### Typing & Linting
The updated method of doing this is to define all the EZRegex elements of a dialect in `elements.py`, and then add type hints and doc strings in the `elements.pyi` file. EZRegex elements that accept parameters are typed as functions (even though they're not), for both convenience for the user when using linter, and to give documentation in an easier way. EZRegex elements that don't accept parameters should be typed as EZRegex, and given documentation as a string on the line below it. This is *slightly* non-standard, but linters support it, as well as my documentation generator script, which parses the .pyi files. The elements can also be seperated into groups in the .pyi files by using `"Group: \<group name\>\n\<group description\>"`, which also gets parsed by the documentation script. The groups aren't used in the actual library, but are helpful in seperating the documentation, as well as used in [ezregex.org](http://ezregex.org)

### Dialects
Because most regex dialects *are* 90% identical, a hidden "base" dialect is implemented, but it works a bit differently. It has an `elements.py` file, but it defines all the elements as a dict in the form of {"element_name": {"keyword": "arguements"}}. It then has a `load_dialect()` function, which is the only thing importable from it. The reason it's done this way is because `dialect` is a required parameter of the EZRegex constructor, so `load_dialect()` takes a `dialect` parameter, and constructs the base elements from it's dict and returns a new dict of initialized elements to be dumped into the global scope of the dialect. The `elements.py` file of a specific dialect can then remove any elements that it doesn't support (using the `del` keyword) and add/overwrite any it does support.

### Inverting
There's actually 2 algorithms implemented for "inverting" regexs. The old algorithm regexs the regexs in a specific order to replace parts one at a time. This is just as nasty and horrifying as it sounds. Dispite it being a terrible, *terrible* solution, I actually got it to work decently well.

Later, when I was reading up on abstract syntax trees, and scrolling around on PyPi, I realized that Python has one built in, and that it's available to use. I reimplemented the whole algorithm to instead parse the AST given by the built-in re lexer, and wrote my own parser on top of it, which works *much* better.

Along the way, I also discovered, deep in the corners of the internet, 2 other Python libraries which do almost the same thing: `xeger` (regex backwards), and `sre_yield`. `xeger` technically works, however it tends to include unprintable characters, so it's output isn't very readable. `sre_yeild` is better, but it can be very slow, and is not quite the use case I'm going for. My invert algorithm is meant to be a debugging tool (though it doubles well for a testing tool), so it does things like detecting words (as opposed to seperate word characters) and inserts actual words, and doing the same for numbers and inserting `12345...`, as well as a couple other enhancements.

### Tests
Tests for a while now have just been in a single `tests.py` file, which was a giant pile of all the tests. I'm currently moving to use pytest. There's a `regexs.json` file (and a `replacements.json` file) that have a bunch of regexs, along with things they're supposed to match, and things they're not supposed to match, for testing.

## Installation
EZRegex is distributed on [PyPI](https://pypi.org) as a universal wheel and is available on Linux, macOS and Windows and supports Python 3.10+ and PyPy.

```bash
pip install ezregex
```

The import name is the same as the package name:
```python
import ezregex as er
```

## Todo
See [the todo](todo.txt). I'm slowly moving these to [GitHub issues](https://github.com/smartycope/ezregex/issues), but for now, they're mostly still there


## License
EZRegex is distributed under the [MIT License](https://choosealicense.com/licenses/mit)
