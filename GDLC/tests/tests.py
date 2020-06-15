#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
`test_examples()` runs a series of doctests on some of the functions used in the GDLC module. 
`helper_debug()` runs a doctest on file `helper_debug.py`. Used when building new tests.
`helper_doctest()` runs a doctest on file `helper_doctest.py`: Contains hints on how to avoid common pitfalls.

Created 3 May 2020

@author: patricktoche
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

    if verbose: print('...testing examples in file test_default_copy.py')
    r = doctest.testfile('test_default_copy.py', optionflags=flags)
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_default_head.py')
    r = doctest.testfile('test_default_head.py', optionflags=flags)
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_default_root.py')
    r = doctest.testfile('test_default_root.py', optionflags=flags)
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_destroy_tags.py')
    r = doctest.testfile('test_destroy_tags.py', optionflags=flags)
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_extract_patched.py')
    r = doctest.testfile('test_extract_patched.py', optionflags=flags)
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_get_body.py')
    r = doctest.testfile('test_get_body.py')
    a[0] += r[0] ; a[1] += r[1]
    
    if verbose: print('...testing examples in file test_get_function_name.py')
    r = doctest.testfile('test_get_function_name.py')
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_get_head.py')
    r = doctest.testfile('test_get_head.py')
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_get_headword.py')
    r = doctest.testfile('test_get_headword.py')
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_get_html_attrs.py')
    r = doctest.testfile('test_get_html_attrs.py')
    a[0] += r[0] ; a[1] += r[1]

#    TO DO: FIX IT
#    if verbose: print('...testing examples in file test_get_root.py')
#    r = doctest.testfile('test_get_root.py')
#    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_get_meta_opf.py')
    r = doctest.testfile('test_get_meta_opf.py')
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_get_sorted_id.py')
    r = doctest.testfile('test_get_sorted_id.py')
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_list_files_all.py')
    r = doctest.testfile('test_list_files_all.py')
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_list_files_ignore.py')
    r = doctest.testfile('test_list_files_ignore.py')
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_list_files_range.py')
    r = doctest.testfile('test_list_files_range.py')
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_list_invalid_tags.py')
    r = doctest.testfile('test_list_invalid_tags.py')
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_list_invalid_tags_kf8.py')
    r = doctest.testfile('test_list_invalid_tags_kf8.py')
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_list_valid_tags.py')
    r = doctest.testfile('test_list_valid_tags.py')
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_make_definition.py')
    r = doctest.testfile('test_make_definition.py')
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_make_dml.py')
    r = doctest.testfile('test_make_dml.py')
    a[0] += r[0] ; a[1] += r[1]
    
    if verbose: print('...testing examples in file test_make_entry.py')
    r = doctest.testfile('test_make_entry.py')
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_make_entry_idx.py')
    r = doctest.testfile('test_make_entry_idx.py')
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_make_headword.py')
    r = doctest.testfile('test_make_headword.py')
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_make_label.py')
    r = doctest.testfile('test_make_label.py')
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_markup_handler.py')
    r = doctest.testfile('test_markup_handler.py')
    a[0] += r[0] ; a[1] += r[1]

    # todo:
    #if verbose: print('...testing examples in file test_parser.py')
    #r = doctest.testfile('test_parser.py')
    #a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_replace_strings.py')
    r = doctest.testfile('test_replace_strings.py')
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_split_entry.py')
    r = doctest.testfile('test_split_entry.py')
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_strip_arrows.py')
    r = doctest.testfile('test_strip_arrows.py')
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_strip_attrs.py')
    r = doctest.testfile('test_strip_attrs.py')
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_strip_chars.py')
    r = doctest.testfile('test_strip_chars.py')
    a[0] += r[0] ; a[1] += r[1]
    
    if verbose: print('...testing examples in file test_strip_classes.py')
    r = doctest.testfile('test_strip_classes.py')
    a[0] += r[0] ; a[1] += r[1]
    
    if verbose: print('...testing examples in file test_strip_comments.py')
    r = doctest.testfile('test_strip_comments.py')
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_strip_empty_tags.py')
    r = doctest.testfile('test_strip_empty_tags.py')
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_strip_header.py')
    r = doctest.testfile('test_strip_header.py')
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_strip_spaces.py')
    r = doctest.testfile('test_strip_spaces.py')
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_strip_squares.py')
    r = doctest.testfile('test_strip_squares.py')
    a[0] += r[0] ; a[1] += r[1]

    if verbose: print('...testing examples in file test_strip_tags.py')
    r = doctest.testfile('test_strip_tags.py')
    a[0] += r[0] ; a[1] += r[1]

    return tuple(a)




def helper_debug(verbose = True):
    """Used for debugging: function `helper_debug()` runs doctest on `helper_debug.py`""" 
    import doctest
    a = [0,0]
    if verbose: 
      print('...testing examples in file helper_debug.py')
    r = doctest.testfile('helper_debug.py', optionflags=flags)
    a[0] += r[0] ; a[1] += r[1] 
    return tuple(a)

def helper_doctest(verbose = True):
    """Template for doctest: function `helper_doctest()` runs doctest on `helper_doctest.py`""" 
    import doctest
    a = [0,0]
    if verbose: 
      print('...testing examples in file helper_doctest.py')
    r = doctest.testfile('helper_doctest.py', optionflags=flags)
    a[0] += r[0] ; a[1] += r[1] 
    return tuple(a)

