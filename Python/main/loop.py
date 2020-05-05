#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created 3 May 2020

@author: patricktoche

Calls the function stored in 'main.py' to loop over several files.
Make sure you have the appropriate parser libraries installed, e.g.
    pip install lxml        # for general purpose package manager and lxml parser
    conda install html5lib  # for Anaconda environment manager and html5 parser
"""

import os
import re
from bs4 import BeautifulSoup, Tag

# Step 1: List files to be processed
def make_names(filepath, first=None, last=None):
    path = os.path.dirname(filepath)
    name = os.path.basename(filepath)
    base, ext = os.path.splitext(name)
    part = re.split(r'(\d+)', base)[0]
    init = int(re.split(r'(\d+)', base)[1])
    if first is not None:
        init = first
    else:
        init = 0
    i = init
    r = []
    def new_name(i):
        nn = os.path.join(path, part) + str(i).zfill(4) + ext
        return nn
    n = new_name(i)
    if last is not None:
        while i < (last+1):
            i += 1
            r.append(n)
            n = new_name(i)
    else:
        while os.path.exists(n):
            i += 1
            r.append(n)
            n = new_name(i)
    return r

root = os.path.join(os.path.sep, 'Users', 'PatrickToche', 'KindleDict', 'GDLC-Kindle-Lookup', 'GDLC', 'mobi8', 'OEBPS', 'Text')
filepath = os.path.join(os.path.sep, root, 'part0000.xhtml')

make_names(filepath)
make_names(filepath, last = 4)
make_names(filepath, first = 2, last = 4)
make_names(filepath, first = 275)



# Step 2: Loop away
def loop_away(filelist, outpath):
    print('In Progress...')
    for file in filelist:
        filename = os.path.basename(filepath)
        outfile = os.path.join(outpath, filename)
        print('.', end='', flush=True)
        with open(file) as infile, open(outfile, 'w') as outfile:
            soup = BeautifulSoup(infile)
            body = soup.find('body')
            for h in body:
                e = body.find(['h1', 'h2', 'h3'])
                if e:
                    outfile.write(str(e))
                    e.decompose()
            b = body.findChildren(recursive=False)
            for x in b:
                s = str(dictionarize(str(x)))
                h = '<?xml version="1.0" encoding="utf-8"?>'
                s = s.replace(h, '')
                s = s+'\n'
                outfile.write(s)
        return s
 
filelist = make_names(filepath)
outpath = os.path.join(os.path.sep, 'Users', 'PatrickToche', 'KindleDict', 'GDLC-Kindle-Lookup', 'Python', 'output')
filelist2 = filelist[0:16]
xml_str = loop_away(filelist2, outpath)



## DEBUG
pretty = ""
soup = BeautifulSoup(xml_str, 'html.parser') 
for value in soup.find_all("foo"):
    pretty += value.prettify()

print(pretty)
