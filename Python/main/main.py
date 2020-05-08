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


def trim_definition(item, verbose=False, clean=False, parser='xml'):
    """
    Takes a single dictionary definition and checks for validity. 
    Also trims certain tags and formatting. 
    Accepts a string. Returns a soup object or the empty string.
    """
    try:
        soup = BeautifulSoup(item, parser=parser)
    except Exception as ex:
        print("Warning: function expects a string.\n\n")
        er = RuntimeError("An exception was raised!")
        raise er from ex
    if verbose:
        print_children(soup)
    # delete entries that lack classes 'rf' and/or 'df'
    p = soup.find_all('p', attrs={'class':'rf'})
    if not p:
        return None
    p = soup.find_all('p', attrs={'class':'df'})
    if not p:
        return None
    # delete all code tags
    soup.code.unwrap()
    # Always remove special character <sup>■</sup>
    for x in soup.find_all('sup'):
        if '■' in x.get_text():
            x.extract()
            break
    # clean further upon request
    if clean:
        clean_tags(soup)
    return(soup)



def split_definition(soup, verbose=False, clean=False, parser='xml'):
    """
    Splits dictionary entry into three parts. 
    Accepts a BeautifulSoup object. Returns a 3-tuple of BS objects.
    """
    # slice soup into chunks:
    s1, s2, s3 = '', '', '' 
    for p in soup.find_all('p', attrs={'class':'rf'}):
        s1 = soup.p.extract()
    for p in soup.find_all('p', attrs={'class':'df'}):
        s2 = soup.p.extract()
    for p in soup.find_all('p', attrs={'class':['rf','df']}):
        #p.decompose()
        p.extract()
    for p in soup.find_all('body'):
        s3 = soup.p.extract()
    if verbose:
        print_types(s1, s2, s3)
    return s1, s2, s3



def make_label(soup):
    """
    Extracts a label from dictionary entry. Uses first part of word or expression.
    Accepts a BeautifulSoup object. Returns a string. 
    To do: remove slashes inside label that occur in some cases
    """
    x = soup.contents[0]
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
    return s
    

def make_word(soup):
    """
    Extracts first word from dictionary entry.
    Accepts a BeautifulSoup object. Returns a string. 
    """
    y0 = soup.contents[0].contents[0].split(' ', 1)[0]
    # Extract all words:
    y1 = ''
    for child in soup.children:
        y1 += str(child)
    # Now substitute the words into:
    s = """
    <div><span><b>y0</b></span></div><span>y1.</span>
    """
    s = s.replace('y0', y0, 1)
    s = s.replace('y1', y1, 1)
    s = s.strip('\n')    
    return s



def make_definition(soup, verbose=False, clean=False):
    """
    Extracts definition from dictionary entry.
    Accepts a BeautifulSoup object. Returns a string. 
    """
    for b in soup.find_all('blockquote'):
        b.unwrap()
    for p in soup.find_all('p', attrs={'class':['ps','p','p1','pc','tc']}):
        if clean:
            if 'class' in p.attrs:
                del p.attrs['class']
        p.wrap(soup.new_tag('blockquote'))
        p.wrap(soup.new_tag('span'))
        p.unwrap()
    if clean:
        # align all blockquote groups to left 
        for b in soup.find_all('blockquote'):
            b.attrs['align'] = 'left'
        # clean all tags inside word definitions:
        for t in soup.find_all(class_=True):
            del t.attrs['class']
    s = str(soup)
    s = re.sub(r'\n+', '\n', s)
    if not s:
        s = 'Definition missing'
    s = '<div>'+s+'</div>'
    return s



def dictionarize(item, verbose=False, clean=False, parser='xml'):
    """
    Takes a well-formed block of html code and formats it to conform with the Kindle dictionary structure. Written for the 'Gran diccionari de la llengua catalana' published by Institut d'Estudis Catalans in 2013, purchased from Amazon for 6 euros and downloaded in the `mobi` format. After conversion to the `azw` format via the `Calibre` plugin `KindleUnpack` the dictionary entries appears as well-formed blocks of html code inside `blockquote` tags. The code loops through the blocks and formats them one at a time. The code below may hopefully be adapted to other dictionaries, but almost certainly will not work without alterations. My original plan was to make a lookup dictionary for Aranes and Occitan. I started with Catalan because I happen to own an electronic copy of the dictionary. I may never have time to do the same thing for other languages. The code has not been optimized and was written over two days without prior thoughts. It relies on the BeautifulSoup library, a library I had never used before. @author: Patrick Toche. 
    """
    if verbose:
        print('\n\nThe `verbose` flag has been set to `True`\n')
        print('Summary of main function:\n')
        print(dictionarize.__doc__, '\n')
    # Trim & Clean dictionary entry:
    soup = trim_definition(item, verbose=verbose, clean=clean, parser=parser)
    # Emtpy or malformed definitions return None, return empty string if None
    if not soup:
        return ''
    # Split dictionary entry into parts:
    s1, s2, s3 = split_definition(soup, verbose=verbose, clean=clean, parser=parser)
    # Extract label value for dictionary entry: 
    s1 = make_label(s1)
    # Extract first word for word header: 
    s2 = make_word(s2)
    # Extract the dictionary definition:
    s3 = make_definition(s3, verbose=verbose, clean=clean)
    # Concatenate label, word, definition, and tag group:
    s = '<idx:entry scriptable="yes">' + '\n' + s1 + s2 + s3 + '\n' + '</idx:entry>'
    if parser == 'xml':
        s = remove_header(s)
    if verbose:
        print_output(s)
    return s



def print_children(soup):
    """
    print information about children and descendents
    """
    print('Function trim_definition() creates a BeautifulSoup object from a string\n')
    print('Number of children and descendants of main soup object:\n')
    print('No. children:   ', len(list(soup.children)))
    print('\nThe children are printed below:')
    print('\n', list(soup.children))
    print('\nNo. descendants:', len(list(soup.descendants)))
    print('\nThe descendants are printed below:')
    print('\n', list(soup.descendants))
    print('\n')
    return None



def print_types(s1, s2, s3):
    """
    print information about types. Accepts a tuple s1, s2, s3
    """
    print('Function split_definition() outputs a tuple s1, s2, s3 of type:\n')
    print('type(s1) =', type(s1))
    print('\n')
    print('type(s2) =', type(s2))
    print('\n')
    print('type(s3) =', type(s3))
    print('\n')
    return None


        
def print_output(s):
    """
    print output to screen (useful for debugging)
    """
    print('\n\nOUTPUT PRINTOUT:\n================\n', s, '\n================\n\n')
    return None



def remove_header(xml):
    """
    remove unwanted header introduced when using the `xml` parser
    using the re module to make case insensitive replacement
    """
    import re
    h = re.escape('<?xml version="1.0" encoding="utf-8"?>') # re.escape ? and .
    r = re.sub(h, '', xml, flags=re.IGNORECASE | re.MULTILINE)
    return r



def clean_tags(soup):
    """
    remove certain tags: '<a', 'id', 'class' from BeautifulSoup object
    """
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
    return(soup)



def make_html(body, head, parser='xml'):
    """
    Inserts a body within the head in html/xml file.
    Accepts strings.
    """
    n = body.count('<body>')
    if n > 1:
        raise ValueError('More than one body tags found inside body!')
    if n == 0:
        body = '<body>' + body + '</body>'
    body = BeautifulSoup(body, parser=parser)
    head = BeautifulSoup(head, parser=parser)
    htm = head.insert(1, body)
    #head.head.append(body)
    return htm



def get_head(html, parser='xml'):
    """
    Extract the head from an html/xml file. 
    Accepts a string. Outputs a string. 
    """
    html = BeautifulSoup(html, parser=parser)
    body = html.find('body')
    body.decompose()
    html = str(html)
    return html

