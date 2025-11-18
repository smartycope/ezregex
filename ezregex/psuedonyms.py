# camelCase versions (of the original, and it's psuedonyms) are automatically added,
# so only include actually different psuedonyms

psuedonyms = {
    'match_max'          : ('repeat',),
    'at_most'            : ('match_at_most',),
    'match_num'          : ('match_amt', 'match_num', 'num', 'amt'),
    'match_range'        : ('between', 'match_between',),
    'more_than'          : ('match_greater_than', 'match_more_than',),
    'at_least'           : ('match_min', 'match_at_least',),
    'line_starts_with'   : ('line_start',),
    'string_starts_with' : ('string_start',),
    'line_ends_with'     : ('line_end',),
    'string_ends_with'   : ('string_end',),
    'chunk'              : ('stuff',),
    'whitechunk'         : ('whitespace',),
    'anything'           : ('anychar', 'any_char', 'char',),
    'letter'             : ('alpha',),
    'alpha_num'          : ('alphanum'  , 'alpha_num',),
    'any_between'        : ('num_between', 'amt_between',),
    'hex_digit'          : ('hex',),
    'new_line'           : ('newline',),
    'period'             : ('dot',),
    'any_of'             : ('anyof', 'one_of',),
    'any_char_except'    : ('any_except', 'anything_except',),
    'if_proceded_by'     : ('if_followed_by',),
    'if_not_proceded_by' : ('if_not_followed_by',),
    'if_enclosed_with'   : ('if_enclosed_by',),
    'earlier_group'      : ('same_as', 'same_as_group',),
    'is_exactly'         : ('exactly',),
    'optional'           : ('one_or_none', 'opt',),
    'at_least_one'       : ('one_or_more', 'at_least_1',),
    'at_least_none'      : ('none_or_more', 'at_least_0', 'any_amt', 'zero_or_more',),
    'signed'             : ('integer', 'signed_int', 'signed_integer',),
    'rgroup'             : ('replace_group',),
    'replace_entire'     : ('replace_all',),
}

all_psuedonyms = set()
for psuedonym in psuedonyms.values():
    all_psuedonyms.update(psuedonym)