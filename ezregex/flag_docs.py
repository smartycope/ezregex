common_flag_docs = {
    'ascii': '''Make matching words, word boundaries, digits, and whitespace \
perform ASCII-only matching instead of full Unicode matching (which is \
default). This is only meaningful for Unicode (str) patterns, and is \
ignored for bytes patterns''',
    'ignore_case': '''Perform case-insensitive matching, including expressions that \
explicitly use uppercase members. Full Unicode matching (such as Ü \
matching ü) also works unless the ASCII flag is used to disable \
non-ASCII matches. The current locale does not change the effect of \
this flag unless the LOCALE flag is also used''',
    'unicode': '''Match using the full unicode standard, instead of just ASCII. \
Enabled by default, and therefore redundant''',
    'global': '''Global mode. Match everything in the given string, instead of just the first match''',
    'anchor': '''The pattern is forced to become anchored at the start of the \
search or at the position of the last successful match.''',
    'single_line': '''Not recommended. Makes the '.' special character match any character at all, including \
a newline. It's recommended you simply use literally_anything instead''',
    'multiline': '''Not recommended. Makes the '^' and '$' special characters match the start and end of \
lines, instead of the start and end of the string. This is automatically inserted when using \
line_start and line_end, you shouldn\'t need to add it manually''',
    'verbose': '''Not recommended. Allows for comments and whitespace, which both don\'t do anything \
in this library.''',
    'lazy': '''The engine will per default to lazy matching, instead of greedy. It's recommended you \
just specify greedy=False instead''',
    'duplicate_groups': '''This allows regex to accept duplicate pattern names, \
however each capture group still has its own ID. Thus the two capture \
groups produce their own match instead of a single combined one''',
}