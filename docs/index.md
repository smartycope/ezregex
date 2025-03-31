# EZRegex Documentation

```{toctree}
:maxdepth: 2
:caption: Contents

getting_started
dialects/index
api/index
examples
contributing
```

## What is EZRegex?

EZRegex is a library for creating regular expressions in a readable way. It supports multiple regex dialects including Python, JavaScript, Java, PCRE, and more.

## Quick Start

```python
from ezregex import word, digit, optional

# Create a pattern for matching a phone number
pattern = digit + digit + digit + optional('-') + digit + digit + digit + digit

# Test the pattern
pattern.test('123-4567')  # True
pattern.test('1234567')   # True
pattern.test('abcd-efg')  # False
```

## Features

- **Multiple Dialect Support**: Write regex once, use it in multiple languages
- **Readable Syntax**: Build complex patterns using simple, chainable functions
- **Type Safety**: Full type hints and IDE support
- **Extensive Testing**: Comprehensive test suite for all supported dialects
