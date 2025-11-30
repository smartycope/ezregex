#!/usr/bin/env python3
from pathlib import Path
import shutil
from ezregex.psuedonyms import psuedonyms
from ezregex.EZRegex import _to_camel_case
import ezregex as ez

# from pdoc import pdoc
# from pdoc import render

here = Path(__file__).parent
dialects = here / "docs" / "dialects"

if dialects.exists():
    shutil.rmtree(dialects)

dialects.mkdir(parents=True, exist_ok=True)

# # Render parts of pdoc's documentation into docs/api...
# render.configure(template_directory=here / "docs" / "pdoc-template", search=False)

# I gave up trying to mess with pdoc and just decided to parse everything by hand for now

# TODO: this still has issues:
# I think some of the replacement regexs aren't getting added?
# General formatting (still want to see if I can get pdoc to work with it)
# Overwriting docs should be a thing (not a problem with this specifically, but elsewhere)
# There's no args, or arg formatting yet. That both needs to be added here, and in all the docstrings
for dialect in [ez.r.REZRegex, ez.javascript.JavascriptEZRegex, ez.pcre2.PCRE2EZRegex, ez.python.PythonEZRegex]:
    doc = ''
    doc += f"# {dialect.__name__}\n\n{dialect.__doc__}\n\n"
    for repl in (False, True):
        for part_name in dialect.parts(include_psuedonyms=False, include_options=False):
            if getattr(dialect, part_name).replacement != repl:
                continue
            doc += f"## {part_name}\n"
            aliases = set()
            for i in psuedonyms.get(part_name, set()):
                aliases.add(_to_camel_case(i))
                aliases.add(i)
            aliases.add(part_name)
            aliases.add(_to_camel_case(part_name))
            aliases.remove(part_name)
            doc += f"<span style='font-style: italic; font-size: small;'>Aliases: {', '.join(aliases)}</span>\n\n"
            if (d := getattr(dialect, part_name).docstring):
                doc += f"{d}\n\n"
        if not repl:
            doc += '\n\n---\n\n## Replacement EZRegexs\n\n'

    (dialects / f"{dialect.__name__}.md").write_text(doc)

import pdoc
pdoc.pdoc('invert', 'api', 'generate', output_directory=here / 'docs')