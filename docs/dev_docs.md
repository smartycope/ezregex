# Developer Documentation
*Note: this page hasn't been updated in a while*
## The EZRegex class
Everything relies on the EZRegex class. The EZRegex class is an abstract class, and each dialect subclasses the EZRegex class to define their own elements specific to that dialect (more on that later). The EZRegex class is not technically a metaclass, but functions similarly: at define time (not at instantiation time), it does a number of things:
1. Add variables to the class (more on that later)
2. Take members & methods of the subclass (including from mixins), and instantiate them into instances of the subclass (I'm calling these `singleton members`)
3. Generate the options function from the flags parameter
4. Make the subclass immutable
5. Add psuedonyms

Step 2 is probably the most confusing part. There are 2 reasons for doing it this way, generally. Firstly, I wanted to support chain-like syntax, like `word.anyof('123').digit`. But mainly, I wanted a more object-oriented way of defining dialects, instead of the hodge-podge pile of global functions I had before. The original operator syntax, `word + anyof('123') + digit`, still functions, because at the end of each dialect I simply have a function that puts all the singleton members into the global scope. This is much cleaner than the other way around.

<!-- TODO: autogenerate snakeCase versions, while still keeping the other psuedonyms -->
The psuedonyms are simply alternate names for most of the functions. Internally, each singleton member has 1 name (lowercase, camel_case), but because this library is intended to be used by people writing in other languages, there's also snakeCase versions of each of them. Also, for many of the concepts, either there's multiple sensible names for them, or different dialects tend to call them different things (`letter` vs `alpha`, `at_least_none` vs `any_amt` vs `zero_or_more`, etc).

Each `singleton member` (and their associated global version) represents a fundamental part of the Regular Expression syntax for that language, as well as less-fundemental common combinations for convenience (like email and float).

## Mixins
~90% of each regex dialect is exactly the same. \w always is a word character, ...? is always optional, etc.

## Creating a New Dialect
An example is worth a thousand explanations, so here's an example dialect:

```python

```

EZRegex can accept a string or a function to define how it's supposed to interact with the current "chain" of elements. If it's a string, it just adds it to the end. If it's a function, it can accept any positional or named parameters, but has to accept `cur=...` as the last parameter (it's complicated). The `cur` parameter is the currently compiled regular expression chain, as a string. What's returned becomes the new `cur` parameter of the next element, or, if there is no next element, the final regex. That way you can add to the front or back of an expression, and you can change what exactly gets added to the current expression based on other parameters.



## Inverting
There's actually 2 algorithms implemented for "inverting" regexs. The old algorithm regexs the regexs in a specific order to replace parts one at a time. This is just as nasty and horrifying as it sounds. Dispite it being a terrible, *terrible* solution, I actually got it to work decently well.

Later, when I was reading up on abstract syntax trees, and scrolling around on PyPi, I realized that Python has one built in, and that it's available to use. I reimplemented the whole algorithm to instead parse the AST given by the built-in re lexer, and wrote my own parser on top of it, which works *much* better.

Along the way, I also discovered, deep in the corners of the internet, 2 other Python libraries which do almost the same thing: `xeger` (regex backwards), and `sre_yield`. `xeger` technically works, however it tends to include unprintable characters, so it's output isn't very readable. `sre_yeild` is better, but it can be very slow, and is not quite the use case I'm going for. My invert algorithm is meant to be a debugging tool (though it doubles well for a testing tool), so it does things like detecting words (as opposed to seperate word characters) and inserts actual words, and doing the same for numbers and inserting `12345...`, as well as a couple other enhancements.

## Tests
Tests are run using GitHub Actions, and are run in a Docker container. The Dockerfile is in the `tests` directory, and the manager script is in the same directory. The manager script is run using `bash manager.sh`

How it works:
1. The docker container is built, either locally, or by GitHub Actions
2. The manager script is run inside the docker container, given the arguments passed to the docker run command
3. The manager script runs the appropriate tests
    * For dialect tests, because the regexs in regexs.jsonc are EZRegexs, not regular expression strings, the file needs to be "compiled" by python in order to be used by other languages, before running individual test runner scripts. This is handled by the `compile_regexs.py` script, which is called by the manager script when appropriate.
    * Each dialect has its own test runner script, which is run by the manager script. These are written in their appropriate language.

Commands:
(All commands should be run from the project root directory)
* To build locally:
    * `docker build -f ./tests/Dockerfile -t ezregex-test .`
    * Note: the first time building takes a while
* To force rebuild locally:
    * `docker build -f ./tests/Dockerfile -t ezregex-test --no-cache .`
* To run tests locally (syncs the project directory and the terminal with the container):
    * `docker run -it -v "$(pwd)":/app ezregex-test <args>`
    * Args:
        * `invert [args] | generate | all | most | dialect <dialect> | pytests`
        * dialect accepts `py | js | r | pcre2 | all | misc`
            * misc runs additional dialect tests that can't be covered by the standard suite of regexs.jsonc/replacements.jsonc tests, like when things should throw errors. They're not specific to any given dialect
        * invert accepts
            * `--strictness <int>`
                * How many times we try inverting a regex, to ensure they all work
            * `--tries <int>`
                * How many times we try inverting before giving up (-1 means just return a bad inversion)
            * `--timeout <int>`
                * How many seconds we allow inverting to take before calling it an infinite loop
            * `--passed`
                * Include passed inversions in the summary
            * `--backend <backend>`
                * The backend to use for inverting. Defaults to "whatever works, in order". For testing the custom backend, it's recommended to use `re_parser`
        * generate takes a long time, and is not run by default
        * pytests runs all the pytests (other than invert and generate)
        * most runs all the tests other than generate
        * all runs all the tests

### Some helpful hints
* If one of the dialect runners *fails*, it could be just a problem with the regexs.jsonc file.
* If one of the dialect runners *errors*, you're probably allowing compilation of a regex that the dialect doesn't support. That means it's a problem with the code itself, and the regexs.jsonc file has innaccurate dialects specified.
* If the compile_regexs.py script fails, it's probably a problem with the regexs.jsonc file trying to use a feature of a dialect that it doesn't support (innaccurate dialects).
