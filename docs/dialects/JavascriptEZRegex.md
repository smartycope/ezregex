# JavascriptEZRegex


    Official docs:
    https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions
    

## any_between
<span style='font-style: italic; font-size: small;'>Aliases: amt_between, numBetween, num_between, anyBetween, amtBetween</span>

 Match any char between `char` and `and_char`, using the ASCII table for reference

                Args:
                    char (str): the first character
                    and_char (str): the second character
            

## any_char_except
<span style='font-style: italic; font-size: small;'>Aliases: any_except, anything_except, anythingExcept, anyExcept, anyCharExcept</span>

 This matches any char that is NOT in `chars`. `chars` can be multiple parameters,
                or a single string of chars to split.

                Args:
                    chars (str): any of the characters to match
            

## any_of
<span style='font-style: italic; font-size: small;'>Aliases: anyof, oneof, anyOf, one_of, oneOf</span>

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
<span style='font-style: italic; font-size: small;'>Aliases: char, anychar, anyChar, any_char</span>

Matches any single character, except a newline. To also match a newline, use literally_anything

## at_least_none
<span style='font-style: italic; font-size: small;'>Aliases: any_amt, anyAmt, zeroOrMore, atLeastNone, atLeast0, zero_or_more, at_least_0, noneOrMore, none_or_more</span>

## at_least_one
<span style='font-style: italic; font-size: small;'>Aliases: atLeast1, at_least_1, one_or_more, oneOrMore, atLeastOne</span>

## chunk
<span style='font-style: italic; font-size: small;'>Aliases: stuff</span>

A "chunk": Any clump of characters up until the next newline

## earlier_group
<span style='font-style: italic; font-size: small;'>Aliases: sameAs, earlierGroup, sameAsGroup, same_as, same_as_group</span>

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
<span style='font-style: italic; font-size: small;'>Aliases: ifNotProcededBy, if_not_followed_by, ifNotFollowedBy</span>

## if_proceded_by
<span style='font-style: italic; font-size: small;'>Aliases: ifProcededBy, if_followed_by, ifFollowedBy</span>

## is_exactly
<span style='font-style: italic; font-size: small;'>Aliases: exactly, isExactly</span>

## letter
<span style='font-style: italic; font-size: small;'>Aliases: alpha</span>

Matches just a letter -- not numbers or _ like word_char

## letter_num
<span style='font-style: italic; font-size: small;'>Aliases: alpha_num, alphaNum, alphanum, letterNum</span>

## line_ends_with
<span style='font-style: italic; font-size: small;'>Aliases: lineEnd, lineEndsWith, line_end</span>

 Matches at a line if it ends with `pattern`

                Args:
                    pattern: the pattern to match
            

## line_starts_with
<span style='font-style: italic; font-size: small;'>Aliases: lineStart, lineStartsWith, line_start</span>

 Matches at a line if it starts with `pattern`

                Args:
                    pattern: the pattern to match
            

## match_at_least
<span style='font-style: italic; font-size: small;'>Aliases: match_min, matchAtLeast, atLeast, at_least, matchMin</span>

## match_at_most
<span style='font-style: italic; font-size: small;'>Aliases: matchAtMost, atMost, at_most</span>

## match_max
<span style='font-style: italic; font-size: small;'>Aliases: repeat, matchMax</span>

## match_more_than
<span style='font-style: italic; font-size: small;'>Aliases: more_than, match_greater_than, moreThan, matchGreaterThan, matchMoreThan</span>

## match_num
<span style='font-style: italic; font-size: small;'>Aliases: matchNum, match_amt, amt, num, matchAmt</span>

## match_range
<span style='font-style: italic; font-size: small;'>Aliases: matchBetween, matchRange, match_between, between</span>

## new_line
<span style='font-style: italic; font-size: small;'>Aliases: newLine, newline</span>

## optional
<span style='font-style: italic; font-size: small;'>Aliases: opt, oneOrNone, one_or_none</span>

## period
<span style='font-style: italic; font-size: small;'>Aliases: dot</span>

## signed
<span style='font-style: italic; font-size: small;'>Aliases: signed_int, integer, signedInt, signedInteger, signed_integer</span>

a signed number, including 123, -123, and +123

## string_ends_with
<span style='font-style: italic; font-size: small;'>Aliases: string_end, stringEndsWith, stringEnd</span>

## string_starts_with
<span style='font-style: italic; font-size: small;'>Aliases: string_start, stringStartsWith, stringStart</span>

## white_char
<span style='font-style: italic; font-size: small;'>Aliases: whiteChar, whitechar</span>

## whitechunk
<span style='font-style: italic; font-size: small;'>Aliases: white_space, whiteSpace, whiteChunk, white_chunk, whitespace</span>

A "chunk" of whitespace. Just any amount of whitespace together



---

## Replacement EZRegexs

## replace_entire
<span style='font-style: italic; font-size: small;'>Aliases: replaceEntire, replace_all, replaceAll</span>

Puts in its place the entire match

## rgroup
<span style='font-style: italic; font-size: small;'>Aliases: replace_group, replaceGroup</span>

 Puts in its place the group specified, either by group number (for unnamed
            groups) or group name (for named groups). Named groups are typically also counted by
            number, check your specific dialect docs for details.
            Group 0 is handled specially by this function, so it calls for the entire match,
            even if 0 doesn't mean the entire match in your dialect.

            Args:
                num_or_name (int | str): the number or name of the group you want to insert here
        

