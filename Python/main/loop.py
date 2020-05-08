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
from bs4 import BeautifulSoup


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


# Step 2: Loop away
def loop_away(filelist, outdir, verbose=False, clean=False, parser='xml'):
    print('In Progress...')
    for file in filelist:
        filename = os.path.basename(file)
        outpath = os.path.join(outdir, filename)
        with open(file, encoding='utf8') as infile:
            head = get_head(infile, parser=parser)
        with open(file) as infile, open(outpath, 'w') as outfile:
            soup = BeautifulSoup(infile, parser=parser)
            body = soup.find('body')
            for line in body:
                DEBUGGING
                s = str(dictionarize(str(line), verbose=verbose, clean=clean, parser=parser))
                # PROBLEM: dictionarize introduces body tag
                if parser == 'xml':
                    s = remove_header(s)
                s = s+'\n'
                print(s, file=outfile)
                #outfile.write(s)
            print('■', end='', flush=True)
        with open(outpath, 'r+') as outfile:
            body = outfile.read()
            return body, head
            html = make_html(body=body, head=head, parser=parser)
            print('debug: here I am')
            print('debug: type(html) = ', type(html))
            return None
            outfile.seek(0)
            outfile.write(html)
            outfile.truncate()
    print('\nEnd.')
    return s



# Make names and run loop
indir = os.path.join(os.path.sep, 'Users', 'PatrickToche', 'KindleDict', 'GDLC-Kindle-Lookup', 'GDLC', 'mobi8', 'OEBPS', 'Text')
outdir = os.path.join(os.path.sep, 'Users', 'PatrickToche', 'KindleDict', 'GDLC-Kindle-Lookup', 'Python', 'output')
filepath = os.path.join(os.path.sep, indir, 'part0000.xhtml')
make_names(filepath, last = 4)
make_names(filepath, first = 2, last = 4)
make_names(filepath, first = 275)
filelist = make_names(filepath)
f = filelist[16:17]
xml = loop_away(f, outdir)

