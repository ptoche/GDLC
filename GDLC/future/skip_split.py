#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Not thoroughly tested: edge cases probably fail
def skip_split(string, separator=' ', start=None, end=None):
    """
    Split a string between two occurrences of the same separator.
    Returns:
        (head, body, tail)
    Modules:
        string (separator)
    """
    # initialize counters:
    a, b, i, j = 0, len(string), 0, 0
    if not start:
        start = 0
    if not end:
        end = b
    if start >= end:
        return ''
    print('  start = ', start)
    print('  end = ', end)
    print('  a = ', a)
    print('  b = ', b)
    # save the step size:
    k = len(separator)
    # get the index of the first occurrence:
    j = string.find(separator)
    if j == -1:
        return ''
    # search forward every k steps:
    while j >= 0 and i <= end:
        print('  s[j:j+(k+1)]', s[j:j+(k+1)])
        print('  i = ', i)
        print('  j = ', j)
        if i == start:
            a = j
        if i == end:
            b = j
        j = string.find(separator, j+k)
        i = i + 1
        print('  a = ', a)
        print('  b = ', b)
        if a >= b:
            return ''
    return (string[0:a], string[a:b], string[b::])

s = '''<body><div>a</div><div>b</div><div>c</div><div>d</div><div>e</div><div>f</div><div>g</div><div>h</div><div>i</div><div>j</div><div>k</div><div>l</div></body>'''


skip_split(string=s, separator='<div>', start=2, end=3)

skip_split(string=s, separator='<div>', start=0)
skip_split(string=s, separator='<div>', end=2)

# minimal version of the above:
def skip_split(string, separator=' ', start=None, end=None):
    """
    Split a string between two occurrences of the same separator.
    Returns: (head, body, tail)
    """
    # initialize counters:
    a, b, i, j = 0, len(string), 0, 0
    # save the step size:
    k = len(separator)
    # get the index of the first occurrence:
    j = string.find(separator)
    if j == -1:
        return ''
    # search forward every k steps:
    while j >= 0 and i <= end:
        if i == start:
            a = j
        if i == end:
            b = j
        j = string.find(separator, j+k)
        i = i + 1
    return (string[0:a], string[a:b], string[b::])
skip_split(string=s, separator='<div>', start=2, end=3)
