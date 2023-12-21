"""
A quick script to generate the docs in the README from the docs in the __init__.py file.
Automatically opens the README and inserts them between the markdown comments.
"""

from ezregex.python import __docs__, __groups__
import ezregex.python as er
from os.path import join, dirname
from clipboard import copy
import inspect

USE_COLLAPSIBLE = True

if USE_COLLAPSIBLE:
    s = ''
    # Iterate through the groups
    for group, elements in __groups__.items():
        s += f'<details>\n\t<summary>{group.title()}</summary>\n\n'
        if group in __docs__['groups_docs']:
            s += '#### ' + __docs__['groups_docs'][group] + '\n'

        # Iterate through the elements within the groups
        for element in elements:
            s += '- ' + element
            if inspect.isfunction(getattr(er, element)):
                # Remove the last 27 chars of the functions, because those are the "-> ..." part
                s += str(inspect.signature(getattr(er, element)))[:-27]
            s += '\n'

            # Add the additional explanation, if there is one
            if element in __docs__ and __docs__[element] is not None:
                s += '\t- ' + __docs__[element] + '\n'
        s += '\n</details>\n\n'

    s += '<details>\n\t<summary>Operators</summary>\n\n'
    for op, desc in __docs__['operator_docs'].items():
        s += '- ' + op + '\n\t- ' + desc + '\n'

    # Leave this open, cause we have the additional 2 operators manually added in the README
    # (because they're not relevant to ezregex.org)
    # s += '\n</details>\n\n'

# The exact same thing, just using headers instead of collapsible sections
else:
    s = ''
    # Iterate through the groups
    for group, elements in __groups__.items():
        s += '### ' + group.title() + '\n'
        if group in __docs__['groups_docs']:
            s += '#### ' + __docs__['groups_docs'][group] + '\n'

        # Iterate through the elements within the groups
        for element in elements:
            s += '- ' + element
            if inspect.isfunction(getattr(er, element)):
                # Remove the last 27 chars of the functions, because those are the "-> ..." part
                s += str(inspect.signature(getattr(er, element)))[:-27]
            s += '\n'
            # Add the additional explanation, if there is one
            if element in __docs__ and __docs__[element] is not None:
                s += '\t- ' + __docs__[element] + '\n'

    s += '### Operators\n'
    for op, desc in __docs__['operator_docs'].items():
        s += '- ' + op + '\n\t- ' + desc + '\n'


# copy(s)
with open(join(dirname(__file__), 'README.md'), 'r') as f:
    lines = f.readlines()

start = lines.index('<!-- Start of generated docs -->\n') + 1
end = lines.index('<!-- End of generated docs -->\n')
# First, get rid of the old one
lines = lines[:start] + lines[end:]
# Now add the new one
lines.insert(start, s)

with open(join(dirname(__file__), 'README.md'), 'w') as f:
    f.writelines(lines)
