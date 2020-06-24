#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract portions from large dictionaries. KindleUnpack produces large html file from mobi dictionaries, sometimes over 100MB. For instance, Diccionario de la lengua española (Real Academia Española) distributed by Amazon is over 120MB. Not many text editors are comfortable with such large files. The code below helps produce extracts of much smaller sizes. 

Created 21 June 2020

@author: patricktoche
"""

# must look inside html to find cut-off text
# For RAE dictionary, I use <tr class="calibre17">
from bs4 import BeautifulSoup
from pathlib import Path

# Set paths:
dir0 = Path('~/calibre-unpacked/RAE_mobi/mobi7').expanduser()
dir1 = Path('~/calibre-unpacked/RAE_mobi/extract').expanduser()
name0 = 'book.html'

# skip_split() used to save extract from body:
# grab everything between ith and jth occurrences of separator:
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


# save document root (everything around the <body> tag):
with open(dir0/name0) as infile, open(dir1/'extract.html', 'w') as outfile:  
    infile = infile.read()
    # print head to file:
    head, sep, tail = infile.partition('<body>')
    outfile.write(head)
    outfile.write('\n')
    outfile.write(sep)
    outfile.write('\n')
    # print extract to file:
    extract = skip_split(infile, separator='<tr class="calibre17">', start=0, end=10)[1]
    outfile.write(extract)
    # print tail to file:
    head, sep, tail = infile.partition('</body>')
    outfile.write(sep)
    outfile.write('\n')
    outfile.write(tail)

