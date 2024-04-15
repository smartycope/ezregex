from rich import print as rprint
from rich.table import Table
from rich.text import Text
import jsonc
from ezregex import invert
from ezregex.python import literal

strictness=20
dontIncludePassed=True
invertBackend='re_parser'
invert_tries=5
import jstyleson
# from jsonc_parser.parser import JsoncParser

#! This works


def test_invert():
    offset = 2

    # The structure is ["regex pattern", "replacement regex", "base string", "what the base string should look like after substitution"]
    with open('tests/replacements.jsonc') as f:
        replacements = jstyleson.load(f)

    with open('tests/regexs.jsonc') as f:
        regexs = jstyleson.load(f)

    # replacements = JsoncParser.parse_file('tests/replacements.jsonc')
    # regexs = JsoncParser.parse_file('tests/regexs.jsonc')


    table = Table(title="invert tests", expand=False)
    table.add_column("Line", justify="center", style="grey37")#, max_width=2)
    table.add_column("Regex", justify="right", style="green")#, max_width=40)
    table.add_column("Inverse", justify="left", style="dim green")
    table.add_column("Success", justify="center")

    for cnt, r in enumerate(regexs + replacements):
        regex = r[0]
        if type(regex) is str:
            regex = literal(regex)

        try:
            for _ in range(strictness):
                # -1 means return it even if it's bad
                inv = invert(regex, backend=invertBackend, tries=invert_tries)
                if inv not in regex or not dontIncludePassed:
                    table.add_row(str(offset+(cnt*5)), Text(regex.str()), '`' + inv + '`', Text('passed', style='blue') if inv in regex else Text('failed', style='red'))
        except (Exception, AssertionError) as err:
            print(f'Error @ approx. {__file__}, line {offset+(cnt*5)}: \nregex = `{regex}`')#, inv = `{inv}`')
            raise err#.with_traceback(None)
    if len(table.rows):
        with open('summary.txt', 'w') as f:
            rprint(table, file=f)
    assert not len(table.rows)
