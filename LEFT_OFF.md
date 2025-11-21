Where I left off:
I was running tests to see what I missed in the OOP refactor. It's runnable, but still has issues.

Still to do:
- get tests working/debug whatever I didn't finish
- update readme
- alphanum and 2 other aliases are not being instantiated (they're still strings)
- update other docs
- update docs for lazy_check_params
- add some tests specific to this refactor
    - a bunch of tests that cover the word.digit.anyof() style syntax
    - make sure all the psuedonyms are covered
    - fill out a lot of the missing "should match" in the tests (not specific to this refactor, however)
    - Make sure all of the methods in EZRegex are tests (I think most of them are, but I did add some I believe)
    - I added a bunch of options() tests, but I don't remember if they're complete
- update readthedocs docs so that the autodocs stuff works now -- it's currently brokenish, and needs to be changed after the refactor

- make a note in GOTCHAS aboud the difference between
digit + whitespace.opt
and
digit.whitespace.opt
    - also note that whitespace == whitechunk, and not white_char