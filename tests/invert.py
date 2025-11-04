import threading
import time

from rich import print as rprint
from rich.table import Table
from rich.text import Text
from rich.progress import track

from ezregex import invert
import re
import json

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--strictness', type=int, default=20)
parser.add_argument('--tries', type=int, default=5)
parser.add_argument('--timeout', type=int, default=5)
parser.add_argument('--backend', type=str, default=...)
parser.add_argument('--passed', action='store_true')
args = parser.parse_args()

# TODO: make these cli params
strictness=args.strictness
includePassed=args.passed
invertBackend=args.backend
# -1 means return it even if it's bad
invert_tries=args.tries
timeout_limit = args.timeout * args.strictness

# The structure is ["regex pattern", "replacement regex", "base string", "what the base string should look like after substitution"]
with open('data/compiled_replacements.json') as f:
    replacements = json.load(f)['py']

with open('data/compiled_regexs.json') as f:
    regexs = json.load(f)['py']

# with open('deleteme.txt', 'w') as f:
#     rprint(regexs + replacements, file=f)
table = Table(title="invert tests", expand=False)
# table.add_column("Line", justify="center", style="grey37")#, max_width=2)
table.add_column("Regex", justify="right", style="green")#, max_width=40)
table.add_column("Inverse", justify="left", style="dim green")
table.add_column("Status", justify="center")

res = [i['regex'] for i in regexs + replacements]
failures = []
for r in track(res, total=len(res)):
    def do_test(r):
        global failures
        # For SOME REASON this one AND ONLY THIS ONE doesn't work INSIDE the docker container, but
        # works OUTSIDE of it. I have no idea why. They've each been tested manually.
        if r in (
            r'(<)?(\w+@\w+(?:\.\w+)+)(?(1)>|$)',
            r'(?:(<))?(\w+@\w+(?:\.\w+)+)(?(1)>|\Z)',
        ):
            return
        try:
            for _ in range(strictness):
                inv = invert(r, backend=invertBackend, tries=invert_tries)
                if re.search(r, inv) is None:
                    failures.append((r, inv, 'failed'))
                elif includePassed:
                    failures.append((r, inv, 'passed'))
        except (Exception, AssertionError) as err:
            failures.append((r, str(err), 'error'))
            raise err

    # print(r, end='\n')
    thread = threading.Thread(target=do_test, args=(r,))
    thread.start()
    thread.join(timeout=timeout_limit)
    # assert not thread.is_alive(), f"Invert took longer than {timeout_limit} seconds: `{r}`"
    if thread.is_alive():
        failures.append((r, '', 'timeout'))
    # Murder the thread
    thread._stop()

# skipped = set()
for r, inv, status in failures:
    # if r in skipped:
        # continue
    # If there's `strictness` number of the same failure, just say they all failed
    # This doesn't work. Don't know why.
    # if len([i for i in failures if i[0] == r]) == strictness:
    #     skipped.add(r)
    table.add_row(
        Text(r),
        Text('`' + inv + '`', style='dim green'),
        Text(status, style='red' if status != 'passed' else 'blue')
    )

if len(failures):
    with open('summary.txt', 'w') as f:
        rprint(table, file=f)
    rprint(table)

print(f'{len(failures)}/{len(res)} ({len(failures)/len(res)*100:.2f}%) failed')

assert not len(failures)

print('pass')