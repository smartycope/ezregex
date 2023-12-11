# A quick script to generate the docs to be pasted into the README from the docs in the __init__.py file
from ezregex.python import __docs__, __groups__
from clipboard import copy

s = ''
for group, elements in __groups__.items():
    s += '### ' + group.title() + '\n'
    if group in __docs__['groups_docs']:
        s += '#### ' + __docs__['groups_docs'][group] + '\n'

    for element in elements:
        s += '- ' + element + '\n'
        if element in __docs__ and __docs__[element] is not None:
            s += '\t- ' + __docs__[element] + '\n'

copy(s)
