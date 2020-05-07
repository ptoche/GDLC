#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created 3 May 2020

@author: patricktoche

Main functions to edit the xhtml source code for the GDLC (Kindle edition).
"""

import os
import re
from bs4 import BeautifulSoup, Tag


def dictionarize(item, verbose=False, clean=False):
    """
    Takes a well-formed block of html code and formats it to conform with the Kindle dictionary structure. Written for the 'Gran diccionari de la llengua catalana' published by Institut d'Estudis Catalans in 2013, purchased from Amazon for 6 euros and downloaded in the `mobi` format. After conversion to the `azw` format via the `Calibre` plugin `KindleUnpack` the dictionary entries appears as well-formed blocks of html code inside `blockquote` tags. The code loops through the blocks and formats them one at a time. The code below may hopefully be adapted to other dictionaries, but almost certainly will not work without alterations. My original plan was to make a lookup dictionary for Aranes and Occitan. I started with Catalan because I happen to own an electronic copy of the dictionary. I may never have time to do the same thing for other languages. The code has not been optimized and was written over two days without prior thoughts. It relies on the BeautifulSoup library, a library I had never used before. @author: Patrick Toche. 
    """
    try:
        #soup = BeautifulSoup(item, 'html.parser')
        soup = BeautifulSoup(item, 'xml')  # revert to html.parser if problem
    except Exception as ex:
        print("Warning: function expects a string.\n\n")
        er = RuntimeError("An exception was raised!")
        raise er from ex
    if verbose:
        print('No. children:   ', len(list(soup.children)))
        print('\n', list(soup.children))
        print('\nNo. descendants:', len(list(soup.descendants)))
        print('\n', list(soup.descendants))
        print('\n')
    # Step 0: clean and break down the problem into chunks
    s1, s2, s3 = '', '', ''
    # delete entries that lack classes 'rf' and/or 'df'
    p = soup.find_all('p', attrs={'class':'rf'})
    if not p:
        return ''
    p = soup.find_all('p', attrs={'class':'df'})
    if not p:
        return ''
    if clean:
        # delete all '<a href' tags
        for a in soup.find_all('a'):
            a.replaceWithChildren()
        # delete all id tags:
        for i in soup.find_all('id'):        
            i.replaceWithChildren()
        # delete all classes associated with <strong>:
        for strong in soup.find_all('strong'):
            del strong.attrs['class']
        # delete all classes associated with <em>:
        for em in soup.find_all('em'):
            del em.attrs['class']
        # delete all classes associated with <sup>:
        for sup in soup.find_all('sup'):
            del sup.attrs['class']
    # Always remove special character <sup>■</sup>
    for x in soup.find_all('sup'):
        if '■' in x.get_text():
            x.extract()
            break
    # delete all code tags
    soup.code.unwrap()
    # slice soup into chunks
    for p in soup.find_all('p', attrs={'class':'rf'}):
        s1 = soup.p.extract()
    for p in soup.find_all('p', attrs={'class':'df'}):
        s2 = soup.p.extract()
    for p in soup.find_all('p', attrs={'class':['rf','df']}):
        soup.p.decompose()
    s3 = soup
    # Step 1: 
    s = s1
    # Extract label value for word entry: 
    x = s.contents[0]
    x = x.replace('->', '')
    # Now substitute the label into:
    s = """
    <idx:orth value="label">
      <idx:infl>
        <idx:iform name="" value="label"/>
      </idx:infl>
    </idx:orth>
    """
    s = s.replace('label', x, 2)
    s = str(s)
    s = s.strip('\n')
    s1 = s
    # Step 2:
    s = s2
    # Extract first word for word header: 
    y0 = s.contents[0].contents[0].split(' ', 1)[0]
    # Extract all words:
    y1 = ''
    for child in s.children:
        y1 += str(child)
    # Now substitute the words into:
    s = """
    <div><span><b>y0</b></span></div><span>y1.</span>
    """
    s = s.replace('y0', y0, 1)
    s = s.replace('y1', y1, 1)
    s = s.strip('\n')
    s2 = s
    # Step 3: 
    s = s3
    for b in s.find_all('blockquote'):
        b.unwrap() 
    for p in s.find_all('p', attrs={'class':['ps','p','p1','pc','tc']}):
        if clean:
            if 'class' in p.attrs:
                del p.attrs['class']
        p.wrap(s.new_tag('blockquote'))
        p.wrap(s.new_tag('span'))
        p.unwrap()
    if clean:
        # align all blockquote groups to left 
        for b in s.find_all('blockquote'):
            b.attrs['align'] = 'left'
        # clean all tags inside word definitions:
        for t in s.find_all(class_=True):
            del t.attrs['class']
    s = str(s)
    s = re.sub(r'\n+', '\n', s)
    if not s:
        s = 'Definition missing'
    s = '<div>'+s+'</div>'
    s3 = s
    # Step 4:
    s = '<idx:entry scriptable="yes">' + '\n' + s1 + s2 + s3 + '\n' + '</idx:entry>'
    # remove unwanted header (introduced if using the xml parser)
    h = '<?xml version="1.0" encoding="utf-8"?>'
    s = s.replace(h, '')
    if verbose:
        print('Output below:\n')
    return s


def make_xml(frame, body):
    """
    Inserts a body inside a piece of html/xml code
    """
    if not isinstance(body, BeautifulSoup):
        body = BeautifulSoup(body)
    if not isinstance(frame, BeautifulSoup):
        frame = BeautifulSoup(frame)
    xml = frame.insert(1, body)
    return xml 

