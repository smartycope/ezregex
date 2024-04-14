"""
Generates a regex expression that matches everything in one list, but not the other
This file is a near-verbatim scrape of:
https://nbviewer.ipython.org/url/norvig.com/ipython/xkcd1313.ipynb
and
https://nbviewer.jupyter.org/url/norvig.com/ipython/xkcd1313-part2.ipynb
(if the links don't work, try them through the wayback machine)
Credit goes to Peter Norvig and Stefan Pochmann.
"""

import itertools
import random
import re
from collections import Counter, defaultdict

Set = frozenset # Data will be frozensets, so they can't be mutated.


cat = ''.join  # Join a sequence of strings with nothing between them

def OR(*regexes):
    """OR together component regexes. Ignore 'None' components.
    Allows both OR(a, b, c) and OR([a, b, c]), similar to max."""
    if len(regexes) == 1:
        regexes = regexes[0]
    return '|'.join(r for r in regexes if r)

def trivial(winners): return '^(' + OR(winners) + ')$'

def mistakes(regex, winners, losers):
    "The set of mistakes made by this regex in classifying winners and losers."
    return ({"Should have matched: " + W
             for W in winners if not re.search(regex, W)} |
            {"Should not have matched: " + L
             for L in losers if re.search(regex, L)})

def replacements(c):
    "All ways to replace character c with something interesting: for now, 'c' or '.'."
    return c if c in '^$' else c + '.'

def dotify(part):
    "Return all ways to replace a subset of chars in part with '.'."
    choices = map(replacements, part)
    return {cat(chars) for chars in itertools.product(*choices)}

def report(winners, losers):
    "Find a regex to match A but not B, and vice-versa.  Print summary."
    solution = findregex(winners, losers)
    assert not mistakes(solution, winners, losers)
    print('Chars: {}, ratio: {:.1f}, inputs: {}:{}'.format(
          len(solution), len(trivial(winners)) / len(solution) , len(winners), len(losers)))
    return solution

def subparts(word, max_len=5):
    "Return a set of subparts of word, consecutive characters up to length 5."
    return set(word[i:i+1+s] for i in range(len(word)) for s in range(max_len))

def matches(regex, strings):
    "Return a set of all the strings that are matched by regex."
    searcher = re.compile(regex).search
    return set(filter(searcher, strings))

def regex_parts(winners, losers):
    "Return parts that match at least one winner, but no loser."
    losers_str = '\n'.join(losers)
    def no_losers(part): return not re.compile(part, re.MULTILINE).search(losers_str)
    wholes = {'^' + w + '$' for w in winners}
    parts = {d for w in wholes for p in subparts(w) for d in dotify(p)}
    return wholes | set(filter(no_losers, parts))

def eliminate_dominated(covers):
    """Given a dict of {regex: {winner...}}, make a new dict with only the regexes
    that are not dominated by any others. A regex part p is dominated by p2 if p2 covers
    a superset of the matches covered by p, and rp is shorter."""
    newcovers = {}
    def signature(p): return (-len(covers[p]), len(p))
    for p in sorted(covers, key=signature):
        if not covers[p]: break # All remaining r must not cover anything
        # r goes in newcache if it is not dominated by any other regex
        if not any(covers[p2] >= covers[p] and len(p2) <= len(p)
                   for p2 in newcovers):
            newcovers[p] = covers[p]
    return newcovers

def select_necessary(covers):
    """Select winners covered by only one part; remove from covers.
    Return a pair of (covers, necessary)."""
    counts = Counter(w for p in covers for w in covers[p])
    necessary = {p for p in covers if any(counts[w] == 1 for w in covers[p])}
    if necessary:
        covered = {w for p in necessary for w in covers[p]}
        covers = {p: covers[p] - covered
                  for p in covers if p not in necessary}
        return covers, OR(necessary)
    else:
        return covers, None

def simplify_covers(covers, partial=None):
    "Eliminate dominated regexes, and select ones that uniquely cover a winner."
    previous = None
    while covers != previous:
        previous = covers
        covers = eliminate_dominated(covers)
        covers, necessary = select_necessary(covers)
        partial = OR(partial, necessary)
    return covers, partial

class BranchBound(object):
    "Hold state information for a branch and bound search."
    def __init__(self, winners, max_num_calls, k=4):
        self.cheapest = trivial(winners)
        self.calls    = max_num_calls
        self.k        = k

    def search(self, covers, partial=None):
        """Recursively extend partial regex until it matches all winners in covers.
        Try all reasonable combinations until we run out of calls."""
        if self.calls <= 0:
            return self.cheapest
        self.calls -= 1
        covers, partial = simplify_covers(covers, partial)
        if not covers: # Nothing left to cover; solution is complete
            self.cheapest = min(partial, self.cheapest, key=len)
        elif len(OR(partial, min(covers, key=len))) < len(self.cheapest):
            def score(p): return self.k * len(covers[p]) - len(p)
            best = max(covers, key=score) # Best part
            covered = covers[best] # Set of winners covered by best
            covers.pop(best)
            # Try with and without the greedy-best part
            self.search({c:covers[c]-covered for c in covers}, OR(partial, best))
            self.search(covers, partial)
        return self.cheapest

# TODO: Reimplement this eventually
# def consider_negative_lookahead(W, L):
#     "Return either SOLUTION[W, L] or negative lookup of SOLUTION[L, W], whichever is shorter."
#     solution = min(SOLUTION[W, L], '^(?!.*(' + SOLUTION[L, W] + '))',
#                    key=len)
#     assert not mistakes(solution, W, L)
#     return solution

class BranchBoundRandomRestart(BranchBound):
    def search(self, covers, partial=None):
        """Recursively extend partial regex until it matches all winners in covers.
        Try all reasonable combinations until we run out of calls."""
        if self.calls <= 0:
            return partial, covers
        self.calls -= 1
        covers, partial = simplify_covers(covers, partial)
        if not covers: # Nothing left to cover; solution is complete
            self.cheapest = min(partial, self.cheapest, key=len)
        elif len(OR(partial, min(covers, key=len))) < len(self.cheapest):
            # Try with and without the greedy-best component
            K = random.choice((2, 3, 4, 4, 4, 5, 6))
            F = random.choice((0.1, 0.1, 2.0))
            def score(c): return K * len(covers[c]) - len(c) + random.uniform(0., F)
            best = max(covers, key=score) # Best component
            covered = covers[best] # Set of winners covered by r
            covers.pop(best)
            self.search({c:covers[c]-covered for c in covers}, OR(partial, best))
            self.search(covers, partial)
        return self.cheapest

def repetitions(part):
    """Return a set of strings derived by inserting a single repetition character
    ('+' or '*' or '?'), after each non-special character.
    Avoid redundant repetition of dots."""
    splits = [(part[:i], part[i:]) for i in range(1, len(part)+1)]
    return {A + q + B
            for (A, B) in splits
            # Don't allow '^*' nor '$*' nor '..*' nor '.*.'
            if not (A[-1] in '^$')
            if not A.endswith('..')
            if not (A.endswith('.') and B.startswith('.'))
            for q in '*+?'}

def pairs(winners, special_chars=Set('*+?^$.[](){}|\\')):
    chars = Set(cat(winners)) - special_chars
    return {A+'.'+q+B
            for A in chars for B in chars for q in '*+?'}

def regex_covers(winners, losers, max_len=5):
    """Generate regex components and return a dict of {regex: {winner...}}.
    Each regex matches at least one winner and no loser."""
    losers_str = '\n'.join(losers)
    wholes = {'^'+winner+'$' for winner in winners}
    parts  = {d for w in wholes for p in subparts(w, max_len) for d in dotify(p)}
    reps   = {r for p in parts for r in repetitions(p)}
    pool   = wholes | parts | pairs(winners) | reps
    searchers = {p:re.compile(p, re.MULTILINE).search for p in pool}
    return {p: Set(filter(searchers[p], winners))
            for p in pool
            if not searchers[p](losers_str)}

def bb_findregex(winners, losers, calls=10000, restarts=10, max_len=5):
    "Find the shortest disjunction of regex components that covers winners but not losers."
    bb = BranchBoundRandomRestart(winners, calls)
    covers = eliminate_dominated(regex_covers(winners, losers, max_len))
    for _ in range(restarts):
        bb.calls = calls
        bb.search(covers.copy())
        if bb.calls > 0: # If search was not cut off, we have optimal solution
            return bb
    return bb

def findregex(winners:set, losers:set, calls:int=1000, restarts:int=3, max_len:int=5) -> str:
    """ The entrypoint into generating regex expressions from lists
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
    """
    return bb_findregex(set(winners), set(losers), calls=calls, restarts=restarts).cheapest
generate_regex = findregex
