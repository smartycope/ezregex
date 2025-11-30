#


### findregex
```python
.findregex(
   winners: set, losers: set, calls: int = 1000, restarts: int = 3, max_len: int = 5
)
```

---
The entrypoint into generating regex expressions from lists
You give the function a set of things you want an expression to match (`winners`), and a set
of things you want it not to match (`losers`), and it generates an expression that does so.

`calls` sets the max number of iterations of the algorithm we do before we give up and return
what we have
`restarts` sets how many times we restart to algorithm in order to shake things up in case we've
gone down a sub-optimal path
`max_len` sets the maximum length of induvidual chunks that we OR together

The algorithm runs for `calls` * `restarts` times, so tread lightly when setting those values.
Increasing them causes the algorithm to run longer and find a shorter regex that meets the
specifications, but it will also be significantly slower.

Wrap this call in `raw()` to use it as an EZRegex expression

Credit for this algorithm goes to Peter Norvig and Stefan Pochmann. See:
https://nbviewer.jupyter.org/url/norvig.com/ipython/xkcd1313-part2.ipynb
