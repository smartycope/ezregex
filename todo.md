TODO:
is matchMax(either('a', 'b')) supposed to match 'aba' or just 'aaa' or 'bbb'?
in test(), overlapping groups print multiple times
in test(), if there's an empty match, it prints None -- and also prints wrong cause the span is (-1,-1)
"stuff" + EZRegexMember() doesn't seem to work if it starts with a string
match_at_most()
emoji() member
AnyExcept: ^(?!.*county).* (matches any line which doesn't have 'county' in it)
figure out how to add proper linting to all of them -- manually override __doc__?
maybe a function like line(stuff in a line), which automatically adds line start and line end to it
same as above, but with string?
README links are broken
change conditionals to taking in 2 parameters (the current pattern, and their associated condition) instead

ADD TESTS FOR:
lineStart
stringStart
lineEnd
stringEnd

FINISHED:
start_of_string, and end, start_of_line, and end
