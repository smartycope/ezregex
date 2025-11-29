# import pdoc
# import os
# from pathlib import Path

# PACKAGE = "ezregex"  # change this

# out = Path("docs/dialects")
# out.mkdir(parents=True, exist_ok=True)

# # Render Markdown instead of HTML
# renderer = pdoc.Renderer(docformat="markdown")

# (Path.home() / 'HERE.deleteme.txt').write_text('generate_dialect_docs.py ran')

# modules = pdoc.Module.from_package(PACKAGE)

# for module in modules.walk():
#     md = renderer.render_module(module)
#     path = out / f"{module.name}.md"
#     path.write_text(md, encoding="utf-8")

# print(f"Generated {len(list(modules.walk()))} modules into docs/dialects/")


#!/usr/bin/env python3
from pathlib import Path
import shutil

from pdoc import pdoc
from pdoc import render


# exclude = (
#     "!flag_docs",
#     "!inject_parts",
#     "!invert_old",
#     "!psuedonyms",
#     '!mixins',
#     '!r',
#     '!javascript',
#     '!pcre2',
#     '!python',
# )

# # pdoc("pdoc", "!pdoc.", "pdoc.doc", output_directory=out)
# pdoc("ezregex", *exclude, output_directory=out)
# # pdoc("ezregex.EZRegex", *exclude, output_directory=out)
# # pdoc("ezregex.invert", *exclude, output_directory=out)
# # pdoc("ezregex.api", *exclude, output_directory=out)
# # pdoc("ezregex.generate", *exclude, output_directory=out)
# # pdoc("ezregex.r", *exclude, output_directory=out)
# # pdoc("ezregex.javascript", *exclude, output_directory=out)
# # pdoc("ezregex.pcre2", *exclude, output_directory=out)
# # pdoc("ezregex.python", *exclude, output_directory=out)

# # ...and rename the .html files to .md so that mkdocs picks them up!
# for f in out.glob("**/*.html"):
#     f.rename(f.with_suffix(".md"))


#!/usr/bin/env python3
import ezregex as ez

import pdoc

here = Path(__file__).parent
dialects = here / "docs" / "dialects"

if dialects.exists():
    shutil.rmtree(dialects)

dialects.mkdir(parents=True, exist_ok=True)

# # Render parts of pdoc's documentation into docs/api...
render.configure(template_directory=here / "docs" / "pdoc-template", search=False)


ezregex    = pdoc.doc.Module(ez)
# generate   = pdoc.doc.Module(ez.generate)
# invert     = pdoc.doc.Function("ezregex", ez.invert.__qualname__, ez.invert, ('ezregex', ez.invert.__qualname__))
# api        = pdoc.doc.Function("ezregex", ez.api.__qualname__, ez.api, ('ezregex', ez.api.__qualname__))
r          = pdoc.doc.Module(ez.r)
# r          = pdoc.doc.Class("ezregex.r", ez.r.REZRegex.__qualname__, ez.r.REZRegex, ('ezregex.r', ez.r.REZRegex.__qualname__))
# javascript = pdoc.doc.Class("ezregex.javascript", ez.javascript.JavascriptEZRegex.__qualname__, ez.javascript.JavascriptEZRegex, ('ezregex.javascript', ez.javascript.JavascriptEZRegex.__qualname__))
# pcre2      = pdoc.doc.Class("ezregex.pcre2", ez.pcre2.PCRE2EZRegex.__qualname__, ez.pcre2.PCRE2EZRegex, ('ezregex.pcre2', ez.pcre2.PCRE2EZRegex.__qualname__))
# python     = pdoc.doc.Class("ezregex.python", ez.python.PythonEZRegex.__qualname__, ez.python.PythonEZRegex, ('ezregex.python', ez.python.PythonEZRegex.__qualname__))

# We can override most pdoc doc attributes by just assigning to them.
# python.get("word").docstring = "HERE! Dynamic docstring for word"
# ezregex.functions.append(invert)
# ezregex.functions.append(api)
# ezregex.submodules.append(generate)
# ezregex.classes.extend([r, javascript, pcre2, python])

(dialects / "index.md"     ).write_text(pdoc.render.html_module(ezregex,    {"ezregex"   : ezregex, "r" : r}))
# (dialects / "generate.md"  ).write_text(pdoc.render.html_module(generate,   {"generate"  : generate}))
# (dialects / "invert.md"    ).write_text(pdoc.render.html_function(invert,     {"invert"    : invert}))
# (dialects / "api.md"       ).write_text(pdoc.render.html_function(api,        {"api"       : api}))
# (dialects / "r.md"         ).write_text(pdoc.render.html_module(r,          {"r"         : r}))
# (dialects / "javascript.md").write_text(pdoc.render.html_class(javascript, {"javascript": javascript}))
# (dialects / "pcre2.md"     ).write_text(pdoc.render.html_class(pcre2,      {"pcre2"     : pcre2}))
# (dialects / "python.md"    ).write_text(pdoc.render.html_class(python,     {"python"    : python}))