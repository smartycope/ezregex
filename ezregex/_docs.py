import ast
import os
from copy import deepcopy
from pathlib import Path
# from clipboard import copy
from rich import print

# ASSUMPTION: Groups are designated using the form "Group: <name>\n<optional description>"
# ASSUMPTION: strings below variables act as the descriptions for those variables
# ASSUMPTION: There aren't any extraneous variables or functions in the .pyi dialect files

class DocGenerator(ast.NodeVisitor):
    """ This parses the .pyi file and gets all the relevant info out of it """
    def __init__(self, node) -> None:
        self.docs = {}
        self.group = None
        self.key = None

        # ASSUMPTION: all dialects inhereit the base dialect, and only the base dialect
        with open('./base/interface.py') as f:
                self.visit(ast.parse(f.read(), type_comments=True))
        self.visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign):
        self.key = node.target.id # type: ignore
        self.docs[self.group][self.key] = [None, '']

    def visit_Expr(self, node: ast.Expr):
        if type(node.value) is ast.Constant:
            if type(node.value.value) is str and node.value.value.strip().startswith('Group: '):
                self.group = node.value.value.strip().splitlines()[0].strip()[len('Group: '):]
                self.docs[self.group] = {'description': '\n'.join(node.value.value.strip().splitlines()[1:]).strip().replace('\n', '')}

            elif self.key:
                self.docs[self.group][self.key][1] = node.value.value.strip().replace('\n', '')
                self.key = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
        n = deepcopy(node)
        n.body = []
        self.docs[self.group][node.name] = [ast.unparse(n)[4:-1], ast.get_docstring(node)]

    def delete_key_recursive(self, dictionary, key_to_delete):
        keys_to_delete = []
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.delete_key_recursive(value, key_to_delete)
            elif key == key_to_delete:
                keys_to_delete.append(key)
        for key in keys_to_delete:
            del dictionary[key]

    # ASSUMPTION: The only way we remove parts from the base dialect is using the del keyword
    def visit_Delete(self, node: ast.Delete):
        for i in node.targets:
            for group, d in self.docs.items():
                if i.id in d:
                    del d[i.id]

    # def visit_Module(self, node: ast.Module):
        # if node.body[0].module == 'base.interface' and node.body[0].names[0].name =='*':
        #     with open('./base/interface.py') as f:
        #         self.visit(ast.parse(f.read(), type_comments=True))

    # def generic_visit(self, node):
        # print(type(node).__name__)
        # super().generic_visit(node)


# Go through all the .pyi files and generate the docs for each dialect
docs = {}
for path in os.walk('.'):
    for file in path[2]:
        # ASSUMPTION: we don't want to parse api.pyi, and it's the only *.pyi file we *don't* want to parse
        if file.endswith('.pyi') and not file.endswith('api.pyi'):
            p = os.path.join(path[0] + '/' + file)
            print('Parsing', p)
            with open(p) as f:
                s = f.read()
                # ASSUMPTION: the official name of all the dialects is the same as the folder their in
                docs[path[0][2:]] = DocGenerator(ast.parse(s, type_comments=True)).docs

# TODO: This should probably move somewhere else eventually
operator_docs = {
    "`+`, `<<`, `>>`": "These all do the same thing: combine expressions",
    "`*`": "Multiplies an expression a number of times. `expr * 3` is equivelent to `expr + expr + expr`. Can also be used like `expr * ...` is equivalent to `anyAmt(expr)`",
    "`+`": "A unary + operator acts exactly as a match_max() does, or, if you're familiar with regex syntax, the + operator",
    "`[]`": "expr[2, 3] is equivalent to `match_range(2, 3, expr)`\n\t- expr[2, ...] or expr[2,] is equivalent to `at_least(2, expr)`\n\t- expr[... , 2] is equivalent to `at_most(2, expr)`\n\t- expr[...] or expr[0, ...] is equivelent to `at_least_0(expr)`\n\t- expr[1, ...] is equivalent to `at_least_1(expr)`",
    "`&`": "Coming soon! This will work like the + operator, but they can be out of order. Like an and operation.",
    "`|`": "Coming soon! This will work like an or operation, which will work just like anyOf()",
}

sdocs = ''
for dialect, spec in docs.items():
    s = ''
    # Iterate through the groups
    for group, elements in spec.items():
        #  style="padding-left: 20px;"
        s += f'<details>\n\t<summary>{group.title()}</summary>\n\n'
        # Add the group description, if there is one
        if 'description' in elements:
            s += '#### ' + elements.pop('description') + '\n'

        # Iterate through the elements within the groups
        for element, about in elements.items():
            signature, description = about

            s += '- '
            # if signature:
                # Remove the last 27 chars of the functions, because those are the "-> ..." part
                # s += str(inspect.signature(getattr(er, element)))[:-27]
            s += (signature[:-10] if signature.endswith('-> EZRegex') else signature) if signature else element

            s += '\n'

            # Add the additional explanation, if there is one
            if description:
                s += '\t- ' + description + '\n'
        s += '\n</details>\n\n'

    sdocs += f'<details>\n\t<summary><strong><u>{dialect}</u></strong></summary>{s}</details>\n'

# sdocs += '<details>\n\t<summary>Operators</summary>\n\n'
# for op, desc in operator_docs.items():
#     sdocs += '- ' + op + '\n\t- ' + desc + '\n'

    # Leave this open, cause we have the additional 2 operators manually added in the README
    # (because they're not relevant to ezregex.org)
    # s += '\n</details>\n\n'

# The exact same thing, just using headers instead of collapsible sections
# else:
#     s = ''
#     # Iterate through the groups
#     for group, elements in __groups__.items():
#         s += '### ' + group.title() + '\n'
#         if group in __docs__['groups_docs']:
#             s += '#### ' + __docs__['groups_docs'][group] + '\n'

#         # Iterate through the elements within the groups
#         for element in elements:
#             s += '- ' + element
#             if inspect.isfunction(getattr(er, element)):
#                 # Remove the last 27 chars of the functions, because those are the "-> ..." part
#                 s += str(inspect.signature(getattr(er, element)))[:-27]
#             s += '\n'
#             # Add the additional explanation, if there is one
#             if element in __docs__ and __docs__[element] is not None:
#                 s += '\t- ' + __docs__[element] + '\n'

    # s += '### Operators\n'
    # for op, desc in operator_docs.items():
    #     s += '- ' + op + '\n\t- ' + desc + '\n'

# print(sdocs)
# copy(sdocs)
# This automatically opens the README and inserts the docs between the markdown comments.
readme = Path(__file__).parent.parent / 'README.md'
print(readme)
with open(readme, 'r') as f:
    lines = f.readlines()

start = lines.index('<!-- Start of generated docs -->\n') + 1
end = lines.index('<!-- End of generated docs -->\n')
# First, get rid of the old one
lines = lines[:start] + lines[end:]
# Now add the new one
lines.insert(start, sdocs)

with open(readme, 'w') as f:
    f.writelines(lines)
