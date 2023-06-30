Switch to re.escape() instead of custom escape chars
TODO is matchMax(either('a', 'b')) supposed to match 'aba' or just 'aaa' or 'bbb'?
in test(), overlapping groups print multiple times
in test(), if there's an empty match, it prints None -- and also prints wrong cause the span is (-1,-1)
