# PythonEZRegex


    Official docs:
    https://docs.python.org/3/library/re.html
    

## options

Documentation:
    https://docs.python.org/3/library/re.html#flags

Usage:
    word + options(ignore_case=True)
    word + options('ignore_case')
    word + options('ignore_case', 'multiline')
    word + options('ignore_case', multiline=True)

Args:
    ascii:
        Make matching words, word boundaries, digits, and whitespace perform ASCII-only matching instead of full Unicode matching (which is default). This is only meaningful for Unicode (str) patterns, and is ignored for bytes patterns
    ignore_case:
        Perform case-insensitive matching, including expressions that explicitly use uppercase members. Full Unicode matching (such as Ü matching ü) also works unless the ASCII flag is used to disable non-ASCII matches. The current locale does not change the effect of this flag unless the LOCALE flag is also used
    single_line:
        Not recommended. Makes the '.' special character match any character at all, including a newline. It's recommended you simply use literally_anything instead
    locale:
        Try not to use this, and rely on unicode matching instead
    multiline:
        Not recommended. Makes the '^' and '$' special characters match the start and end of lines, instead of the start and end of the string. This is automatically inserted when using line_start and line_end, you shouldn't need to add it manually
    unicode:
        Match using the full unicode standard, instead of just ASCII. Enabled by default, and therefore redundant


## any_between
<span style='font-style: italic; font-size: small;'>Aliases: amt_between, anyBetween, amtBetween, num_between, numBetween</span>

 Match any char between `char` and `and_char`, using the ASCII table for reference

                Args:
                    char (str): the first character
                    and_char (str): the second character
            

## any_char_except
<span style='font-style: italic; font-size: small;'>Aliases: anythingExcept, any_except, anyExcept, anything_except, anyCharExcept</span>

 This matches any char that is NOT in `chars`. `chars` can be multiple parameters,
                or a single string of chars to split.

                Args:
                    chars (str): any of the characters to match
            

## any_of
<span style='font-style: italic; font-size: small;'>Aliases: oneOf, oneof, anyOf, one_of, anyof</span>

 Match any of the given `patterns`. Note that `patterns` can be multiple parameters,
                or a single string. Can also accept parameters chars and split. If char is set
                to True, then `patterns` must only be a single string, it interprets `patterns`
                as characters, and splits it up to find any of the chars in the string. If
                split is set to true, it forces the ?(...) regex syntax instead of the [...]
                syntax. It should act the same way, but your output regex will look different.
                By default, it just optimizes it for you.

                Args:
                    patterns: any of the patterns to match
                    chars (bool): whether to interpret patterns as characters (default: auto)
                    split (bool): whether to split patterns into characters (default: auto)
            

## anything
<span style='font-style: italic; font-size: small;'>Aliases: any_char, char, anychar, anyChar</span>

Matches any single character, except a newline. To also match a newline, use literally_anything

## at_least_none
<span style='font-style: italic; font-size: small;'>Aliases: noneOrMore, atLeastNone, none_or_more, zeroOrMore, zero_or_more, any_amt, at_least_0, anyAmt, atLeast0</span>

## at_least_one
<span style='font-style: italic; font-size: small;'>Aliases: atLeast1, atLeastOne, one_or_more, oneOrMore, at_least_1</span>

## chunk
<span style='font-style: italic; font-size: small;'>Aliases: stuff</span>

A "chunk": Any clump of characters up until the next newline

## earlier_group
<span style='font-style: italic; font-size: small;'>Aliases: same_as, sameAs, earlierGroup, same_as_group, sameAsGroup</span>

 Matches whatever the group referenced by `num_or_name` matched earlier. Must be *after* a
                group which would match `num_or_name`

                Args:
                    num_or_name (int | str): either the number or name of the previous group
            

## either
<span style='font-style: italic; font-size: small;'>Aliases: or, or_</span>

 Match either `pattern` or `or_pattern`. To choose between more than 2 things,
                you can either chain multiple `either` calls, or use `any_of`. Note that
                the order here matters: it first tries `pattern`, and if that doesn't
                match, then it tries `or_pattern`.

                Args:
                    pattern: a pattern to match
                    or_pattern: a pattern to match if the first one fails
            

## hex_digit
<span style='font-style: italic; font-size: small;'>Aliases: hex, hexDigit</span>

## if_enclosed_with
<span style='font-style: italic; font-size: small;'>Aliases: ifEnclosedBy, if_enclosed_by, ifEnclosedWith</span>

## if_not_proceded_by
<span style='font-style: italic; font-size: small;'>Aliases: ifNotFollowedBy, if_not_followed_by, ifNotProcededBy</span>

## if_proceded_by
<span style='font-style: italic; font-size: small;'>Aliases: ifFollowedBy, ifProcededBy, if_followed_by</span>

## is_exactly
<span style='font-style: italic; font-size: small;'>Aliases: isExactly, exactly</span>

## letter
<span style='font-style: italic; font-size: small;'>Aliases: alpha</span>

Matches just a letter -- not numbers or _ like word_char

## letter_num
<span style='font-style: italic; font-size: small;'>Aliases: letterNum, alpha_num, alphanum, alphaNum</span>

## line_ends_with
<span style='font-style: italic; font-size: small;'>Aliases: line_end, lineEndsWith, lineEnd</span>

 Matches at a line if it ends with `pattern`

                Args:
                    pattern: the pattern to match
            

## line_starts_with
<span style='font-style: italic; font-size: small;'>Aliases: lineStartsWith, lineStart, line_start</span>

 Matches at a line if it starts with `pattern`

                Args:
                    pattern: the pattern to match
            

## match_at_least
<span style='font-style: italic; font-size: small;'>Aliases: atLeast, at_least, match_min, matchMin, matchAtLeast</span>

## match_at_most
<span style='font-style: italic; font-size: small;'>Aliases: matchAtMost, at_most, atMost</span>

## match_max
<span style='font-style: italic; font-size: small;'>Aliases: repeat, matchMax</span>

## match_more_than
<span style='font-style: italic; font-size: small;'>Aliases: matchGreaterThan, more_than, moreThan, match_greater_than, matchMoreThan</span>

## match_num
<span style='font-style: italic; font-size: small;'>Aliases: num, matchNum, matchAmt, match_amt, amt</span>

## match_range
<span style='font-style: italic; font-size: small;'>Aliases: matchBetween, between, matchRange, match_between</span>

## new_line
<span style='font-style: italic; font-size: small;'>Aliases: newLine, newline</span>

## optional
<span style='font-style: italic; font-size: small;'>Aliases: one_or_none, opt, oneOrNone</span>

## period
<span style='font-style: italic; font-size: small;'>Aliases: dot</span>

## signed
<span style='font-style: italic; font-size: small;'>Aliases: signedInt, signed_int, integer, signedInteger, signed_integer</span>

a signed number, including 123, -123, and +123

## string_ends_with
<span style='font-style: italic; font-size: small;'>Aliases: stringEnd, string_end, stringEndsWith</span>

 Matches the string if it ends with `pattern`

                Args:
                    pattern: the pattern to match
            

## string_starts_with
<span style='font-style: italic; font-size: small;'>Aliases: stringStartsWith, string_start, stringStart</span>

 Matches the string if it starts with `pattern`

                Args:
                    pattern: the pattern to match
            

## white_char
<span style='font-style: italic; font-size: small;'>Aliases: whitechar, whiteChar</span>

## whitechunk
<span style='font-style: italic; font-size: small;'>Aliases: white_space, white_chunk, whiteSpace, whiteChunk, whitespace</span>

A "chunk" of whitespace. Just any amount of whitespace together



---

## Replacement EZRegexs

## replace_entire
<span style='font-style: italic; font-size: small;'>Aliases: replace_all, replaceAll, replaceEntire</span>

Puts in its place the entire match

## rgroup
<span style='font-style: italic; font-size: small;'>Aliases: replaceGroup, replace_group</span>

 Puts in its place the group specified, either by group number (for unnamed
            groups) or group name (for named groups). Named groups are typically also counted by
            number, check your specific dialect docs for details.
            Group 0 is handled specially by this function, so it calls for the entire match,
            even if 0 doesn't mean the entire match in your dialect.

            Args:
                num_or_name (int | str): the number or name of the group you want to insert here
        

## replace

 Generates a valid regex replacement string, using Python f-string like syntax.

                Args:
                    string (str): the templated replacement string
                    compile (bool): whether to compile the string into an EZRegex subclass instance (default: True)

                Example:
                    ``` replace("named: {group}, numbered: {1}, entire: {0}") ```

                Like Python f-strings, use {{ and }} to specify { and }

                Set the `compile` parameter to False to have it return an EZRegex subclass instance instead of a string

                Note: 0 is handled specially by this function, so it calls for the entire match,
                    even if 0 doesn't mean the entire match in your dialect.

                There's a few of advantages to using this instead of just the regular regex replacement syntax:
                - It's consistent between dialects
                - It's closer to Python f-string syntax, which is cleaner and more familiar
                - It handles numbered, named, and entire replacement types the same
            

