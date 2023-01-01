
# EASY REGEX
An readable and intuitive way to generate Regular Expressions

TLDR: This is to Regex expressions what CMake is to makefiles

# Explination of how this works:
    This is version 2. The original version just had an EasyRegex class with a bunch of members that returned self,
    then you chained together member function calls.
    This version uses a bunch of constant singletons (of type EasyRegexSingleton) that have the __call__() dunder function
    overridden to return a seperate class (EasyRegexMember) which override the __add__() and __str__() dunder functions.
    What happens is you have all the singletons created in this file, specifying lambdas (or strings, for convenience)
    describing how they interact with the regex expression, and then optional inverted lambdas (get to that in a moment)
    and seperate dialog lambdas. When those are called later on by the user, (they can be treated like regular functions)
    they initialize a EasyRegexMember, and give it the function they hold. Then, EasyRegexMembers are chained together with
    +'s (or <<'s). EasyRegexMembers all have internal ordered lists of functions that get added to when +'ed. If you assign
    the chain (or chains!) to a varaible or put in ()'s, what you end up with is one EasyRegexMember that has an ordered
    list of all the functions from all the EasyRegexMembers in that chain. When you then cast that to a string (or call .str()
    or .compile()), it finally goes through and calls all those functions, which results in the final regex string.

# Status:
# Current limitations include:
    .inverse() doesn't work well with broken up chains. A large code refactoring would be required. So to get proper
        inversing on broken up functions, you have to put .inverse() at the end of every chain, before it enters the main chain.
        This will mess up your end result however, so use only for debugging purpouses.
    The "not" operator doesn't currently work. Again, another large code refactoring would be required.
    Everything is kinda just mushed together as generic dialect. Seperating of python and generic dialects would be helpful.
    The Perl dialect isn't implemented at all. I don't know any perl, but this is meant to be a cross-platform solution.
# Usage:
    optionalParams = multiOptional(match(',') + whitechunk() + chunk())
    regex = stuff() + match('test(') + ifFollowedBy(match('ing') + optionalParams)
    regex.test('Testing test(ing, ?) + test-ing!')


# Python Syntax (source: my python linter):
    "."      Matches any character except a newline.
    "^"      Matches the start of the string.
    "$"      Matches the end of the string or just before the newline at
             the end of the string.
    "*"      Matches 0 or more (greedy) repetitions of the preceding RE.
             Greedy means that it will match as many repetitions as possible.
    "+"      Matches 1 or more (greedy) repetitions of the preceding RE.
    "?"      Matches 0 or 1 (greedy) of the preceding RE.
    *?,+?,?? Non-greedy versions of the previous three special characters.
    {m,n}    Matches from m to n repetitions of the preceding RE.
    {m,n}?   Non-greedy version of the above.
    "\\"     Either escapes special characters or signals a special sequence.
    []       Indicates a set of characters.
             A "^" as the first character indicates a complementing set.
    "|"      A|B, creates an RE that will match either A or B.
    (...)    Matches the RE inside the parentheses.
             The contents can be retrieved or matched later in the string.
    (?aiLmsux) The letters set the corresponding flags defined below.
    (?:...)  Non-grouping version of regular parentheses.
    (?P name ...) The substring matched by the group is accessible by name.
    (?P=name)     Matches the text matched earlier by the group named name.
    (?#...)  A comment; ignored.
    (?=...)  Matches if ... matches next, but doesn't consume the string.
    (?!...)  Matches if ... doesn't match next.
    (? =...) Matches if preceded by ... (must be fixed length).
    (? !...) Matches if not preceded by ... (must be fixed length).
    (?(id/name)yes|no) Matches yes pattern if the group with id/name matched,
                       the (optional) no pattern otherwise.

    The special sequences consist of "\" and a character from the list below.
    If the ordinary character is not on the list, then the resulting RE will match the second character.
    \number  Matches the contents of the group of the same number.
    \A       Matches only at the start of the string.
    \Z       Matches only at the end of the string.
    \b       Matches the empty string, but only at the start or end of a word.
    \B       Matches the empty string, but not at the start or end of a word.
    \d       Matches any decimal digit; equivalent to the set [0-9] in
             bytes patterns or string patterns with the ASCII flag.
             In string patterns without the ASCII flag, it will match the whole
             range of Unicode digits.
    \D       Matches any non-digit character; equivalent to [^\d].
    \s       Matches any whitespace character; equivalent to [ \t\n\r\f\v] in
             bytes patterns or string patterns with the ASCII flag.
             In string patterns without the ASCII flag, it will match the whole
             range of Unicode whitespace characters.
    \S       Matches any non-whitespace character; equivalent to [^\s].
    \w       Matches any alphanumeric character; equivalent to [a-zA-Z0-9_]
             in bytes patterns or string patterns with the ASCII flag.
             In string patterns without the ASCII flag, it will match the
             range of Unicode alphanumeric characters (letters plus digits
             plus underscore).
             With LOCALE, it will match the set [0-9_] plus characters defined
             as letters for the current locale.
    \W       Matches the complement of \w.
    \\       Matches a literal backslash.

# [What I'm using as] Generic syntax (source: DuckDuckGo):
    Anchors
    ^	Start of string or line
    \A	Start of string
    $	End of string or line
    \Z	End of string
    \b	Word boundary
    \B	Not word boundary
    \<	Start of word
    \>	End of word
    Character Classes
    \c	Control character
    \s	Whitespace [ \t\r\n\v\f]
    \S	Not Whitespace [^ \t\r\n\v\f]
    \d	Digit [0-9]
    \D	Not digit [^0-9]
    \w	Word [A-Za-z0-9_]
    \W	Not Word [^A-Za-z0-9_]
    \x	Hexadecimal digit [A-Fa-f0-9]
    \O	Octal Digit [0-7]
    POSIX Classes
    [:upper:]	Uppercase letters [A-Z]
    [:lower:]	Lowercase letters [a-z]
    [:alpha:]	All letters [A-Za-z]
    [:alnum:]	Digits and letters [A-Za-z0-9]
    [:digit:]	Digits [0-9]
    [:xdigit:]	Hexadecimal digits [0-9a-f]
    [:punct:]	Punctuation
    [:blank:]	Space and tab [ \t]
    [:space:]	Blank characters [ \t\r\n\v\f]
    [:cntrl:]	Control characters [\x00-\x1F\x7F]
    [:graph:]	Printed characters [\x21-\x7E]
    [:print:]	Printed characters and spaces [\x20-\x7E]
    [:word:]	Digits, letters and underscore [A-Za-z0-9_]
    Pattern Modifiers
    //g	Global Match (all occurrences)
    //i	Case-insensitive
    //m	Multiple line
    //s	Treat string as single line
    //x	Allow comments and whitespace
    //e	Evaluate replacement
    //U	Ungreedy pattern
    Escape Sequences
    \	Escape following character
    \Q	Begin literal sequence
    \E	End literal sequence
    Quantifiers
    *	0 or more
    +	1 or more
    ?	0 or 1 (optional)
    {3}	Exactly 3
    {3,}	3 or more
    {2,5}	2, 3, 4 or 5
    Groups and Ranges
    .	Any character except newline (\n)
    (a|b)	a or b
    (...)	Group
    (?:...)	Passive (non-capturing) group
    [abc]	Single character (a or b or c)
    [^abc]	Single character (not a or b or c)
    [a-q]	Single character range (a or b ... or q)
    [A-Z]	Single character range (A or B ... or Z)
    [0-9]	Single digit from 0 to 9
    Assertions
    ?=	Lookahead assertion
    ?!	Negative lookahead
    ?<=	Lookbehind assertion
    ?!= / ?<!	Negative lookbehind
    ?>	Once-only Subexpression
    ?()	Condition [if then]
    ?()|	Condition [if then else]
    ?#	Comment
    Special Characters
    \n	New line
    \r	Carriage return
    \t	Tab
    \v	Vertical tab
    \f	Form feed
    \ooo	Octal character ooo
    \xhh	Hex character hh
    String Replacement
    $n	n-th non-passive group
    $2	"xyz" in /^(abc(xyz))$/
    $1	"xyz" in /^(?:abc)(xyz)$/
    $`	Before matched string
    $'	After matched string
    $+	Last matched string
    $&	Entire matched string

# I don't know Perl syntax specifically, if you do, and would like to help me, contact me!
