#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created 3 May 2020

@author: patricktoche

Main function to edit the xhtml source code for the GDLC (Kindle edition).
"""

# Make sure you have the appropriate parser libraries installed, e.g.
# conda install html5lib or pip install lxml, etc.

from bs4 import BeautifulSoup, Tag

def dictionarize(item, verbose=False, pretty=False):
    """docstring"""
    # type checks
    if not isinstance(item, (BeautifulSoup, Tag)):
        #soup = BeautifulSoup(item, 'html.parser')
        soup = BeautifulSoup(item, 'xml')  # revert to html.parser if problem
    else:
        soup = item
    # input is intended to be a string, but allows BeautifulSoup and Tag 
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
    # Remove special character <sup>■</sup>
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
        if 'class' in p.attrs:
            del p.attrs['class']
        p.wrap(s.new_tag('blockquote'))
        p.wrap(s.new_tag('span'))
        p.unwrap()
    for b in s.find_all('blockquote'):
        b.attrs['align'] = 'left'
    # clean all tags inside word definitions:
    for t in s.find_all(class_=True):
        del t.attrs['class']
    s = str(s)
    s = s.strip('\n')
    if not s:
        s = 'Definition missing'
    s = '<div>'+s+'</div>'
    s3 = s
    # Step 4:
    s = '<idx:entry scriptable="yes">' + '\n' + s1 + s2 + s3 + '\n' + '</idx:entry>'
    # remove unwanted header (introduced if using the xml parser)
    h = '<?xml version="1.0" encoding="utf-8"?>'
    s = s.replace(h, '')
    s = BeautifulSoup(s, 'xml')  # features="xml" allows self-closing tags
    if pretty:
        s = s.prettify() 
    if verbose:
        print('Output below:\n')
    return s


# Import html file
import os
base = os.path.join(os.path.sep, 'Users', 'PatrickToche', 'KindleDict', 'GDLC-Kindle-Lookup','Python','tests')
name0 = 'test4.html'
name1 = 'junk.html'
with open(os.path.join(base, name0)) as infile, open(os.path.join(base, name1), 'w') as outfile:
    soup = BeautifulSoup(infile)
    body = soup.find('body')
    for h in body:
        e = body.find('h2')
        if e:
            outfile.write(str(e))
            e.decompose()
    b = body.findChildren(recursive=False)
    for x in b:
        s = str(dictionarize(str(x)))
        h = '<?xml version="1.0" encoding="utf-8"?>'
        s = s.replace(h, '')
        outfile.write(s)
