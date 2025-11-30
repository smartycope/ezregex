#


### invert
```python
.invert(
   expr: Union[str, 'EZRegex'], tries: int = 10, backend: Literal['re_parser',
   'regex', 'xeger', 'sre_yield'] = ..., words: (Literal['lookup',
   'random']|None) = 'lookup', random_numbers = False, alot = 8
)
```

---
"Inverts" a regular expression by returning an example of something which is guaruanteed to
match the passed expression.
NOTE: This only works on valid Python regular expressions.


**Args**

* **expr**  : The regular expression to invert. Can be a string, or a EZRegex expression
* **words**  : Controls how works are handled. If `random`, words are made of random letters. If `lookup`,
    it looks up valid english words and inserts them to make it more readable.
* **random_numbers**  : controls whether all numbers are 12345... to a desired length, or if they're
    just random numbers (again, for readability)
* **alot**  : When given a choice of how many characters to put someone, it inserts a random integer
    between 1 and `alot`.
* **tries**  : Controls how many times to try to invert the expression before giving up. This is effective,
    because there is an element of randomness involved in inverting the regex given.
* **backend**  : One of ('re_parser', 'regex', 'xeger', 'sre_yield').
    `re_parser` is the default, it uses the build-in parser in the re package to create an AST
        of the regex
    `regex` uses regular expressions to parse regular expressions, which is as gross as it sounds.
        It's slightly buggy, but mostly works.
    `xeger` imports the `xeger` pacakge and uses it instead. Xeger inverts work, but are less
        readable. Must have the `xeger` package installed.
    `sre_yield` imports the `sre_yield` package and uses it instead. I don't think this works
        right now, and may be significantly slower.

