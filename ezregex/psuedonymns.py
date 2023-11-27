from .elements import *

match_max = matchMax
match_at_most = atMost = at_most = matchAtMost
match_num = matchAmt = match_amt = amt = num = matchNum
match_range = matchRange
match_more_than = match_greater_than = matchGreaterThan = moreThan = more_than = matchMoreThan
match_at_least = match_min = matchMin = atLeast = at_least = matchAtLeast
line_starts_with = line_start = lineStart = lineStartsWith
string_starts_with = string_start = stringStart = stringStartsWith
line_ends_with = line_end = lineEnd = lineEndsWith
string_ends_with = string_end = stringEnd = stringEndsWith
stuff      = chunk
whiteChunk = whitechunk
anychar    = anything
anyChar    = anything
char       = anything
alpha      = letter
alphanum   = alpha_num = alphaNum
white      = whitechunk

# anyAmt = any_amt = multi_optional = multiOpt = multi_opt = multiOptional
anyAmt = any_amt = atLeastNone
any_between = anyBetween
word_char = wordChar
hex_digit = hex
oct_digit = octDigit
newline = newLine
space_or_tab = spaceOrTab
carriage_return = carriageReturn
vertical_tab = verticalTab
form_feed = formFeed
dot = period
intOrFloat = int_or_float
not_whitespace = notWhitespace
not_digit = notDigit
not_word = notWord
# any_chars = anyChars
anyof = any_of = oneOf = one_of = anyOf
any_except = anyExcept
any_char_except = anyCharExcept
printable_and_space = printableAndSpace
ifFollowedBy     = ifProceededBy
ifNotFollowedBy  = ifNotProceededBy
if_proceeded_by = ifProceededBy
if_notProceeded_by = ifNotProceededBy
if_preceded_by = ifPrecededBy
if_notPreceded_by = ifNotPreceededBy
if_enclosed_with = ifEnclosedWith
if_proceeded_by = ifProceededBy
if_notProceeded_by = ifNotProceededBy
passive_group = passiveGroup
named_group = namedGroup
exactly = isExactly
oneOrNone = one_or_none = opt = optional
oneOrMore = one_or_more = at_least_one = atLeast1 = at_least_1 = atLeastOne
noneOrMore = none_or_more = at_least_none = at_least_0 = atLeast0 = atLeastNone
ascii = a = ASCII
dotall = s = DOTALL
ignorecase = i = ignoreCase = ignore_case = IGNORECASE
locale = L = LOCALE
multiline = m = MULTILINE
unicode = u = UNICODE
# Useful Combinations
integer = signed

replaceGroup = replace_group = rgroup
replace_all = replaceAll = replace_entire = replaceEntire
