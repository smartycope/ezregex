# Categories of EZRegexs

## Positionals
These differentiate between the *string* starting with the sequence, and a *line* starting with the sequence. Do note that the start of the string is also the start of a line. These can also be called without parameters to denote the start/end of a string/line without something specific having to be next to it.

## Conditionals
These can only be used once in a given expression. They only match a given expression if the expression is/ins't
followed/preceeded by a the given pattern

## Replacement
In the intrest of "I don't want to think about any syntax at all", I have included replace members. Do note that they are *not* interoperable with the other EZRegexs, and can only be used with other strings and each other.

## Premade
These are some useful combinations that may be commonly used. They are not as stable, and may be changed and added to in later versions to make them more accurate

## Flags
These shadow python regex flags, and can just as easily be specified directly to the re library instead. They're provided here for compatibility with other regex dialects. See https://docs.python.org/3/library/re.html#flags for details. Note that other regex dialects may not support all of these, or may implement others.

## Literals
These are the most basic EZRegexs. Fairly self explanatory.

## Not Literals
## Categories
## Amounts
## Choices
## Grouping
## Misc