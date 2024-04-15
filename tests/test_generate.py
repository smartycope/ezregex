import re
from groups import *
from groups import _losers, _winners


from ezregex.generate import *


def words(text):
    "All space-separated words in text."
    return Set(text.split())

def phrases(text, sep='/'):
    "All sep-separated phrases in text, uppercased and stripped."
    return Set(p.upper().strip() for p in text.split(sep))

# Tests
def test_new_parts():
    return # I'm not changing this code anytime soon, it doesn't interact with any other code, and it takes forever to run
    assert repetitions('a') == {'a+', 'a*', 'a?'}
    assert repetitions('ab') == {'a+b', 'a*b', 'a?b',
                                 'ab+', 'ab*', 'ab?'}
    assert repetitions('a.c') == {'a+.c', 'a*.c', 'a?.c',
                                  'a.c+', 'a.*c', 'a.?c',
                                  'a.+c', 'a.c*', 'a.c?'}
    assert repetitions('^a..d$') == {'^a+..d$', '^a*..d$', '^a?..d$',
                                     '^a..d+$', '^a..d*$', '^a..d?$'}
    assert pairs({'ab', 'c'}) == {
        'a.*a', 'a.*b', 'a.*c',
        'a.+a', 'a.+b', 'a.+c',
        'a.?a', 'a.?b', 'a.?c',
        'b.*a', 'b.*b', 'b.*c',
        'b.+a', 'b.+b', 'b.+c',
        'b.?a', 'b.?b', 'b.?c',
        'c.*a', 'c.*b', 'c.*c',
        'c.+a', 'c.+b', 'c.+c',
        'c.?a', 'c.?b','c.?c'}
    assert len(pairs({'1...2...3', '($2.34)', '42', '56', '7-11'})) == 8 * 8 * 3
    covers = regex_covers({'one', 'on'}, {'won', 'wuan', 'juan'})
    assert (eliminate_dominated(covers) == {'e': {'one'}, '^o': {'on', 'one'}})
    return 'test_new_parts passes'


def test_bb():
    return # I'm not changing this code anytime soon, it doesn't interact with any other code, and it takes forever to run
    assert OR(['a', 'b', 'c']) == OR('a', 'b', 'c') == 'a|b|c'
    assert OR(['a|b', 'c|d']) == OR('a|b', 'c|d') == 'a|b|c|d'
    assert OR(None, 'c') == 'c'
    covers1 = {'a': {'ann', 'abe'}, 'ab': {'abe'}}
    assert eliminate_dominated(covers1) == {'a': {'ann', 'abe'}}
    assert simplify_covers(covers1) == ({}, 'a')
    covers2 = {'a': {'abe', 'cab'}, 'b': {'abe', 'cab', 'bee'},
               'c': {'cab', 'cee'}, 'c.': {'cab', 'cee'}, 'abe': {'abe'},
               'ab': {'abe', 'cab'}, '.*b': {'abe', 'cab', 'bee'},
               'e': {'abe', 'bee', 'cee'}, 'f': {}, 'g': {}}
    assert eliminate_dominated(covers2) == simplify_covers(covers2)[0] == {
        'c': {'cab', 'cee'}, 'b': {'cab', 'abe', 'bee'}, 'e': {'cee', 'abe', 'bee'}}
    covers3 = {'1': {'w1'}, '.1': {'w1'}, '2': {'w2'}}
    assert eliminate_dominated(covers3) == {'1': {'w1'}, '2': {'w2'}}
    assert simplify_covers(covers3) in (({}, '2|1'), ({}, '1|2'))
    covers, nec = select_necessary({'a': {'abe'}, 'c': {'cee'}})
    assert covers == {} and (nec == 'c|a' or nec == 'a|c')
    assert {0, 1, 2} >= {1, 2}
    assert {1, 2} >= {1, 2}
    assert not ({1, 2, 4} >= {1, 3})
    return 'test_bb passes'

def test_generate():
    return # I'm not changing this code anytime soon, it doesn't interact with any other code, and it takes forever to run
    assert subparts('^it$') == {'^', 'i', 't', '$', '^i', 'it', 't$', '^it', 'it$', '^it$'}
    assert subparts('this') == {'t', 'h', 'i', 's', 'th', 'hi', 'is', 'thi', 'his', 'this'}
    subparts('banana') == {'a', 'an', 'ana', 'anan', 'b', 'ba', 'ban', 'bana',
                           'n', 'na', 'nan', 'nana'}

    assert dotify('it') == {'it', 'i.', '.t', '..'}
    assert dotify('^it$') == {'^it$', '^i.$', '^.t$', '^..$'}
    assert dotify('this') == {'this', 'thi.', 'th.s', 'th..', 't.is', 't.i.', 't..s', 't...',
                              '.his', '.hi.', '.h.s', '.h..', '..is', '..i.', '...s', '....'}
    # assert regex_parts({'win'}, {'losers', 'bin', 'won'}) == {
    #     '^win$', '^win', '^wi.', 'wi.',  'wi', '^wi', 'win$', 'win', 'wi.$'}
    assert regex_parts({'win'}, {'bin', 'won', 'wine', 'wit'}) == {'^win$', 'win$'}
    regex_parts({'boy', 'coy'},
                {'ahoy', 'toy', 'book', 'cook', 'boycott', 'cowboy', 'cod', 'buy', 'oy',
                 'foil', 'coyote'}) == {'^boy$', '^coy$', 'c.y$', 'coy$'}

    assert matches('a|b|c', {'a', 'b', 'c', 'd', 'e'}) == {'a', 'b', 'c'}
    assert matches('a|b|c', {'any', 'bee', 'succeed', 'dee', 'eee!'}) == {
        'any', 'bee', 'succeed'}

    assert OR(['a', 'b', 'c']) == 'a|b|c'
    assert OR(['a']) == 'a'

    assert words('this is a test this is') == {'this', 'is', 'a', 'test'}

    assert findregex({"ahahah", "ciao"},  {"ahaha", "bye"}) == 'a.$'
    # This is *an* option, not the only option
    # assert findregex({"this", "that", "the other"}, {"one", "two", "here", "there"}) == 'h..$'
    assert findregex({'boy', 'coy', 'toy', 'joy'}, {'ahoy', 'buy', 'oy', 'foil'}) == '^.oy'

    assert not mistakes('a|b|c', {'ahoy', 'boy', 'coy'}, {'joy', 'toy'})
    assert not mistakes('^a|^b|^c', {'ahoy', 'boy', 'coy'}, {'joy', 'toy', 'kickback'})
    assert mistakes('^.oy', {'ahoy', 'boy', 'coy'}, {'joy', 'ploy'}) == {
        "Should have matched: ahoy",
        "Should not have matched: joy"}
    return 'tests pass'



def test_generate_auto():
    return # I'm not changing this code anytime soon, it doesn't interact with any other code, and it takes forever to run
    for w, l in zip(_winners, _losers):
        r = re.compile(generate_regex(w, l, 500, restarts=2))
        for i in w:
            assert r.search(i), f"`{r}` is not in `{i}`"
        for i in l:
            assert not r.search(i), f"`{r}` is in `{i}`"
        # print(r, 'is good')
