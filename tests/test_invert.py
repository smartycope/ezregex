from multiprocessing import Value
from rich import print as rprint
from rich.table import Table
import time
import threading
from rich.text import Text
from ezregex import invert
from ezregex.python import literal
from ezregex import python

strictness=20
dontIncludePassed=True
invertBackend='re_parser'
invert_tries=5
import jstyleson


def test_invert():
    offset = 2

    # The structure is ["regex pattern", "replacement regex", "base string", "what the base string should look like after substitution"]
    with open('tests/replacements.jsonc') as f:
        replacements = jstyleson.load(f)

    with open('tests/regexs.jsonc') as f:
        regexs = jstyleson.load(f)

    # with open('deleteme.txt', 'w') as f:
    #     rprint(regexs + replacements, file=f)

    table = Table(title="invert tests", expand=False)
    table.add_column("Line", justify="center", style="grey37")#, max_width=2)
    table.add_column("Regex", justify="right", style="green")#, max_width=40)
    table.add_column("Inverse", justify="left", style="dim green")
    table.add_column("Success", justify="center")

    for cnt, r in enumerate(regexs + replacements):
        def do_test():
            # with open('log.txt', 'a') as f:
            #     rprint(f'testing {r[0]}', file=f)
            try:
                regex = eval(r[0], python.__dict__)

                if type(regex) is str:
                    regex = literal(regex)
                for _ in range(strictness):
                    # -1 means return it even if it's bad
                    inv = invert(regex, backend=invertBackend, tries=invert_tries)
                    if inv not in regex or not dontIncludePassed:
                        table.add_row(str(offset+(cnt*5)), Text(regex.str()), '`' + inv + '`', Text('passed', style='blue') if inv in regex else Text('failed', style='red'))
            except (Exception, AssertionError) as err:
                raise ValueError(f'Error @ approx. {__file__}, line {offset+(cnt*4)}: \nregex = `{r[0]}`') #from err#, inv = `{inv}`')
        thread = threading.Thread(target=do_test)
        thread.start()
        limit = 15
        thread.join(timeout=limit)
        assert not thread.is_alive(), f"Invert took too long (>{limit} seconds): `{r[0]}`'"

    if len(table.rows):
        with open('summary.txt', 'w') as f:
            rprint(table, file=f)
    assert not len(table.rows)


def test_function():
    start_time = time.time()
    for i in range(10):  # Change 10 to whatever your loop range is
        if time.time() - start_time > 5:
            raise AssertionError("Iteration took too long!")
        # Your loop code here

test_function()
