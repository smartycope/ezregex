# Developer Documentation
*Note: this page hasn't been updated in a while*
## The EZRegex class
Everything relies on the EZRegex class. EZRegex shouldn't be instantiated by the user, as each dialect subclasses the EZRegex class and defines their own elements specific to that dialect (more on that later). Each element represents a fundamental part of the Regular Expression syntax for that language, as well as less-fundemental common combinations for convenience (like email and float).

EZRegex can accept a string or a function to define how it's supposed to interact with the current "chain" of elements. If it's a string, it just adds it to the end. If it's a function, it can accept any positional or named parameters, but has to accept `cur=...` as the last parameter (it's complicated). The `cur` parameter is the current regular expression chain, as a string. What's returned becomes the new `cur` parameter of the next element, or, if there is no next element, the final regex. That way you can add to the front or back of an expression, and you can change what exactly gets added to the current expression based on other parameters.

The EZRegex class has operators overloaded so you can combine them in intuitive ways and call them by intuitive names.

## Typing & Linting
The updated method of doing this is to define all the EZRegex elements of a dialect in `elements.py`, and then add type hints and doc strings in the `elements.pyi` file. EZRegex elements that accept parameters are typed as functions (even though they're not), for both convenience for the user when using linter, and to give documentation in an easier way. EZRegex elements that don't accept parameters should be typed as EZRegex, and given documentation as a string on the line below it. This is *slightly* non-standard, but linters support it, as well as my documentation generator script, which parses the .pyi files. The elements can also be seperated into groups in the .pyi files by using `"Group: \<group name\>\n\<group description\>"`, which also gets parsed by the documentation script. The groups aren't used in the actual library, but are helpful in seperating the documentation, as well as used in [ezregex.org](http://ezregex.org)

## Dialects
Because most regex dialects *are* 90% identical, a parent EZRegex class implements most of the applicable logic, and a hidden "base" dialect is implemented, but works a bit differently. It has an `elements.py` file, but it defines all the elements as a dict in the form of {"element_name": {"keyword": "arguements"}}. It then has a `load_dialect()` function, which is the only thing importable from it. The reason it's done this way is because most elements, though identical in different dialects, have to be the appropriate dialect subclass. `load_dialect()` takes the dialect type as a parameter, and instantiates the base elements from it's dict and returns a new dict of initialized elements to be dumped into the global scope of the dialect. The `elements.py` file of a specific dialect can then remove any elements that it doesn't support (using the `del` keyword) and add/overwrite any it does support, or that work differently.

Each subclass of EZRegex must implement a few options to describe the dialect-specific behavior of the EZRegex class, for example, in the JavaScript dialect, /'s are added to the beginning and end of the pattern, and flags are handled differently in each dialect. This has to be implemented directly into the EZRegex subclass.

There's 2 parts that are required:
- `_flag_func`
    - An abstract function that gets called with `final`, which is the final compiled pattern *with* `beginning` and `end` attached, and `flags`, which is a string of all the flags applied to the pattern. Internally, the flags are single digits, because flags usually are. They get passed to this function as a single string, which can be parsed and modified if necissary (it usually isn't)
- `_escape_chars`
    - The characters that need to be escaped. Should be a byte string (i.e. b'...')
- `_final_func`
    - An optional function which takes in the final string about to be returned, and returns the *final* string. Useful for some dialects, for example, in JS adding `/` to the beginning and end of the final pattern

## Inverting
There's actually 2 algorithms implemented for "inverting" regexs. The old algorithm regexs the regexs in a specific order to replace parts one at a time. This is just as nasty and horrifying as it sounds. Dispite it being a terrible, *terrible* solution, I actually got it to work decently well.

Later, when I was reading up on abstract syntax trees, and scrolling around on PyPi, I realized that Python has one built in, and that it's available to use. I reimplemented the whole algorithm to instead parse the AST given by the built-in re lexer, and wrote my own parser on top of it, which works *much* better.

Along the way, I also discovered, deep in the corners of the internet, 2 other Python libraries which do almost the same thing: `xeger` (regex backwards), and `sre_yield`. `xeger` technically works, however it tends to include unprintable characters, so it's output isn't very readable. `sre_yeild` is better, but it can be very slow, and is not quite the use case I'm going for. My invert algorithm is meant to be a debugging tool (though it doubles well for a testing tool), so it does things like detecting words (as opposed to seperate word characters) and inserts actual words, and doing the same for numbers and inserting `12345...`, as well as a couple other enhancements.

## Tests
Tests are implemented using pytest. Dependancies required for testing are:

```pytest jstyleson py_js_runner rich Cope pydantic```
