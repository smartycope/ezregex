# REZRegex


    Official docs:
    https://www.rdocumentation.org/packages/base/versions/3.6.2/topics/regex
    

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

## anything
<span style='font-style: italic; font-size: small;'>Aliases: char, anychar, anyChar, any_char</span>

Matches any single character, except a newline. To also match a newline, use literally_anything

## at_least_none
<span style='font-style: italic; font-size: small;'>Aliases: any_amt, anyAmt, zeroOrMore, atLeastNone, atLeast0, zero_or_more, at_least_0, noneOrMore, none_or_more</span>

## at_least_one
<span style='font-style: italic; font-size: small;'>Aliases: atLeast1, at_least_1, one_or_more, oneOrMore, atLeastOne</span>

## chunk
<span style='font-style: italic; font-size: small;'>Aliases: stuff</span>

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
        

