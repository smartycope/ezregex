"""Sphinx configuration file."""

project = 'EZRegex'
copyright = '2025'
author = 'smartycope'

extensions = [
    'sphinx.ext.autodoc',        # Auto-generate docs from docstrings
    'sphinx.ext.napoleon',       # Support Google/NumPy style docstrings
    'sphinx.ext.viewcode',       # Add links to source code
    'sphinx.ext.intersphinx',    # Link to other projects' documentation
    # 'sphinx-autodoc-typehints',  # Include type hints in docs
    'myst_parser',              # Support Markdown files
]

# Configure autodoc to read type hints from .pyi files
autodoc_typehints = 'description'
autodoc_type_aliases = {
    'EZRegexDefinition': 'str | Callable[[VarArg, DefaultNamedArg[str, "cur"]], str] | list[partial[str]]'
}

# Theme configuration
html_theme = 'furo'  # Modern, responsive theme
html_static_path = ['_static']

# Intersphinx configuration
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'typing': ('https://typing.readthedocs.io/en/latest/', None),
}
