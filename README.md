# EasyRegex
An readable and intuitive way to generate Regular Expressions

TL;DR: This is to regular expressions what CMake is to makefiles

## Usage:
```
    optionalParams = multiOptional(match(',') + whitechunk() + chunk())
    regex = stuff() + 'test(' + ifFollowedBy(match('ing') + optionalParams)
    regex.test('Testing test(ing, ?) + test-ing!')
```

## Current limitations
- inverse() doesn't work well with broken up chains. A large code refactoring would be required. So to get proper
    inverting on broken up functions, you have to put .inverse() at the end of every chain, before it enters the main chain.
    This will mess up your end result however, so use only for debugging purposes.
- inverse() is also not totally function yet? It's closish, but currently only works on simple regex expressions
- The "not" operator doesn't currently work. Another large code refactoring would be required.
- Everything is kinda just mushed together as generic dialect. Separating of python and generic dialects would be helpful.
- The Perl dialect isn't implemented at all. I don't know any perl, but this is meant to be a cross-platform solution.

## Explination of How it Works
This is version 2. The original version just had an EasyRegex class with a bunch of members that returned self, then you chained together member function calls.

This version uses a bunch of constant singletons (of type EasyRegexSingleton) that have the __call__() dunder function overridden to return a separate class (EasyRegexMember) which override the __add__() and __str__() dunder functions. What happens is you have all the singletons created in this file, specifying lambdas (or strings, for convenience) describing how they interact with the regex expression, and then optional inverted lambdas (get to that in a moment) and separate dialog lambdas. When those are called later on by the user, (they can be treated like regular functions) they initialize a EasyRegexMember, and give it the function they hold. Then, EasyRegexMembers are chained together with +'s (or <<'s). EasyRegexMembers all have internal ordered lists of functions that get added to when +'ed. If you assign the chain (or chains!) to a varaible or put in ()'s, what you end up with is one EasyRegexMember that has an ordered list of all the functions from all the EasyRegexMembers in that chain. When you then cast that to a string (or call .str() or .compile()), it finally goes through and calls all those functions, which results in the final regex string.
