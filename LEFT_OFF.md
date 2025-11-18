Where I left off:
I was running tests to see what I missed in the OOP refactor. It's runnable, but still has issues. One specifically where some methods are not being instantiated for some reason.

Still to do:
- get tests working/debug whatever I didn't finish
- update readme
- update other docs
- add some tests specific to this refactor
    - a bunch of tests that cover the word.digit.anyof() style syntax
    - make sure all the psuedonyms are covered
    - fill out a lot of the missing "should match" in the tests (not specific to this refactor, however)
    - Make sure all of the methods in EZRegex are tests (I think most of them are, but I did add some I believe)
    - I added a bunch of options() tests, but I don't remember if they're complete
- update readthedocs docs so that the autodocs stuff works now -- it's currently brokenish, and needs to be changed after the refactor