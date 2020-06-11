#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
`helper_future()` helps debug development code in `future/future.py`

Created 9 June 2020

@author: patricktoche
"""

import doctest

flags = (
    doctest.REPORT_ONLY_FIRST_FAILURE |
    doctest.NORMALIZE_WHITESPACE |
    doctest.REPORT_NDIFF)


def test_future(verbose = True):
    """Used for debugging development code""" 
    import doctest
    a = [0,0]
    if verbose: 
      print('...testing examples in file future/helper_future.py')
    r = doctest.testfile('test_read_head_future.py', optionflags=flags)
    a[0] += r[0] ; a[1] += r[1] 
    return tuple(a)

