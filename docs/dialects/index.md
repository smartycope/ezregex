# Regex Dialects

EZRegex supports multiple regex dialects, each with its own specific features and syntax.

```{toctree}
:maxdepth: 1

python
javascript
java
pcre
```

## Common Features

All dialects support these basic features:
- Basic pattern matching (literals, wildcards)
- Character classes
- Quantifiers
- Groups and capturing
- Alternation

## Dialect-Specific Features

Each dialect has its own specialized features:

### Python
- Full Unicode support
- Verbose mode
- Conditional patterns
- Named groups

### JavaScript
- Named capture groups
- Lookbehind assertions
- Unicode property escapes
- Sticky and Unicode flags

### Java
- Named capturing groups
- Possessive quantifiers
- Atomic groups
- Unicode categories
- Flag groups

### PCRE
- Subroutines
- Recursive patterns
- Possessive quantifiers
- Atomic groups
- Reset match
- Conditionals
