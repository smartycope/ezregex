from copy import deepcopy
import ast
import os

# This parses the .pyi file and gets all the relevant info out of it
class DocGenerator(ast.NodeVisitor):
    docs = {}
    group = None

    def __init__(self, node) -> None:
        self.visit(node)

    def visit_Constant(self, node: ast.Constant):
        print('~~here~~', node.value)

    def visit_AnnAssign(self, node: ast.AnnAssign):
        self.key = node.target.id
        self.docs[self.group][self.key] = [None, '']

    def visit_Expr(self, node: ast.Expr):
        if type(node.value) is ast.Constant:
            if type(node.value.value) is str and node.value.value.strip().startswith('Group: '):
                self.group = node.value.value.strip().splitlines()[0].strip()[len('Group: '):]
                self.docs[self.group] = {'description': '\n'.join(node.value.value.strip().splitlines()[1:]).strip()}

            elif self.key:
                self.docs[self.group][self.key][1] = node.value.value.strip()
                self.key = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
        n = deepcopy(node)
        n.body = []
        self.docs[self.group][node.name] = [ast.unparse(n)[4:-1], ast.get_docstring(node)]

    # def generic_visit(self, node):
    #     print(type(node).__name__)
    #     super().generic_visit(node)


docs = {}

for path in os.walk('.'):
    for file in path[2]:
        if file.endswith('.pyi') and not file.endswith('api.pyi'):
            p = os.path.join(path[0] + '/' + file)
            print('Parsing', p)
            with open(p) as f:
                s = f.read()
                docs[path[0][2:]] = DocGenerator(ast.parse(s, type_comments=True)).docs

from rich import print
print(docs)

operator_docs = {
    "`+`, `<<`, `>>`": "These all do the same thing: combine expressions",
    "`*`": "Multiplies an expression a number of times. `expr * 3` is equivelent to `expr + expr + expr`. Can also be used like `expr * ...` is equivalent to `anyAmt(expr)`",
    "`+`": "A unary + operator acts exactly as a match_max() does, or, if you're familiar with regex syntax, the + operator",
    "`[]`": "expr[2, 3] is equivalent to `match_range(2, 3, expr)`\n\t- expr[2, ...] or expr[2,] is equivalent to `at_least(2, expr)`\n\t- expr[... , 2] is equivalent to `at_most(2, expr)`\n\t- expr[...] or expr[0, ...] is equivelent to `at_least_0(expr)`\n\t- expr[1, ...] is equivalent to `at_least_1(expr)`",
    "`&`": "Coming soon! This will work like the + operator, but they can be out of order. Like an and operation.",
    "`|`": "Coming soon! This will work like an or operation, which will work just like anyOf()",
}
