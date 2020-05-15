#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created 3 May 2020

@author: patricktoche

`test_examples()` runs a series of doctests on some of the functions used in the GDLC module. 
`test_debug()` runs a doctest on file `test_debug.py`. `test_template()` hints at how to avoid common pitfalls.

"""

import doctest

flags = (
    doctest.REPORT_ONLY_FIRST_FAILURE |
    doctest.NORMALIZE_WHITESPACE |
    doctest.REPORT_NDIFF)


def test_examples(verbose = False):
    # initiate counters
    a = [0,0]
    r = [0,0]

    if verbose: print('...testing examples in file test_clean_tags.py')
    r = doctest.testfile('test_clean_tags.py', optionflags=flags)
    a[0] += r[0] ; a[1] += r[1] 

    if verbose: print('...testing examples in file test_dictionarize.py')
    r = doctest.testfile('test_dictionarize.py')
    a[0] += r[0] ; a[1] += r[1] 

    if verbose: print('...testing examples in file test_get_body.py')
    r = doctest.testfile('test_get_body.py')
    a[0] += r[0] ; a[1] += r[1] 

    if verbose: print('...testing examples in file test_get_head.py')
    r = doctest.testfile('test_get_head.py')
    a[0] += r[0] ; a[1] += r[1] 

    if verbose: print('...testing examples in file test_make_defn.py')
    r = doctest.testfile('test_make_defn.py')
    a[0] += r[0] ; a[1] += r[1] 

    if verbose: print('...testing examples in file test_make_html.py')
    r = doctest.testfile('test_make_html.py')
    a[0] += r[0] ; a[1] += r[1] 

    if verbose: print('...testing examples in file test_make_names.py')
    r = doctest.testfile('test_make_names.py')
    a[0] += r[0] ; a[1] += r[1] 

    if verbose: print('...testing examples in file test_make_label.py')
    r = doctest.testfile('test_make_label.py')
    a[0] += r[0] ; a[1] += r[1] 

    if verbose: print('...testing examples in file test_make_word.py')
    r = doctest.testfile('test_make_word.py')
    a[0] += r[0] ; a[1] += r[1] 

#    if verbose: print('...testing examples in file test_parser.py')
#    r = doctest.testfile('test_parser.py') # doctest: +SKIP
#    a[0] += r[0] ; a[1] += r[1] 

    if verbose: print('...testing examples in file test_remove_char.py')
    r = doctest.testfile('test_remove_char.py')
    a[0] += r[0] ; a[1] += r[1] 

    if verbose: print('...testing examples in file test_remove_header.py')
    r = doctest.testfile('test_remove_header.py')
    a[0] += r[0] ; a[1] += r[1] 

    if verbose: print('...testing examples in file test_remove_tag.py')
    r = doctest.testfile('test_remove_tag.py')
    a[0] += r[0] ; a[1] += r[1] 

    if verbose: print('...testing examples in file test_split_defn.py')
    r = doctest.testfile('test_split_defn.py')
    a[0] += r[0] ; a[1] += r[1] 

    if verbose: print('...testing examples in file test_trim_defn.py')
    r = doctest.testfile('test_trim_defn.py')
    a[0] += r[0] ; a[1] += r[1] 

    return tuple(a)



def test_debug(verbose = True):
    """Used for debugging: function `test_debug()` runs doctest on `test_debug.py`""" 
    import doctest
    a = [0,0]
    if verbose: 
      print('...testing examples in file test_debug.py')
    r = doctest.testfile('test_debug.py', optionflags=flags)
    a[0] += r[0] ; a[1] += r[1] 
    return tuple(a)

def test_template(verbose = True):
    """Test template: function `test_template()` runs doctest on `test_template.py`""" 
    import doctest
    a = [0,0]
    if verbose: 
      print('...testing examples in file test_template.py')
    r = doctest.testfile('test_template.py', optionflags=flags)
    a[0] += r[0] ; a[1] += r[1] 
    return tuple(a)

