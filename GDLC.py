#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created 3 May 2020

@author: patricktoche

Functions to edit the xhtml source code for the GDLC (Kindle edition).

Written for the 'Gran diccionari de la llengua catalana' published by Institut d'Estudis Catalans in 2013, purchased from Amazon for 6 euros and downloaded in the `mobi` format. 

After conversion to the `azw` format via the `Calibre` plugin `KindleUnpack`, the dictionary entries appear as well-formed blocks of html code inside `blockquote` tags. 

The code loops through the blocks and formats them one at a time. 

The code below may hopefully be adapted to other dictionaries, but almost certainly will not work without alterations. 

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
    # slice s1: word label for lookup
    f = soup.find_all('p', attrs={'class':'rf'})
    if f is not None:
        for p in f:
            s1 = soup.p.extract()
    # slice s2: word long and short forms 
    f = soup.find_all('p', attrs={'class':'df'})
    if f is not None:
        for p in f:
            s2 = soup.p.extract()
    # slice s3: word definition
    f = soup.find_all('p', attrs={'class':['rf','df']})
    if f is not None:
        # remove p tags with classes rf and df 
        for p in f:
            #p.decompose()
            p.extract()
        # extract the body as BeautifulSoup object
        s3 = soup.find('body')
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
    f = soup.find_all('blockquote')
    if f is not None:        
        for b in f:
            b.unwrap()
    else:
        print('Problem: definition not contained in a blockquote tag!')
        soup.wrap(Tag(name="blockquote"))
    f = soup.find_all('p', attrs={'class':['ps','p','p1','pc','tc']})
    if f is not None:
        for p in f:
            if clean:
                if 'class' in p.attrs:
                    del p.attrs['class']
            p.wrap(Tag(name="blockquote"))
            p.wrap(Tag(name="span"))
            p.unwrap()
    if clean:
        # align all blockquote groups to left:
        for b in soup.find_all('blockquote'):
            b.attrs['align'] = 'left'
        # clean all tags inside word definitions:
        for t in soup.find_all(class_=True):
            del t.attrs['class']
    # remove unwanted tags:
    s = get_body(soup)
    # remove empty lines:
    s = re.sub(r'\n+', '\n', s)
    if not s:
        s = 'Definition missing'
    s = '<div>'+s+'</div>'
    return s



def dictionarize(item, verbose=False, clean=False, parser='xml'):
    """
    Takes a well-formed block of html code and formats it to conform with the Kindle dictionary structure. 
    """
    if verbose:
        print_todo()
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



def print_summary(docstring):
    """
    Prints a function docstring.
    Returns None.
    """
    print('\n\nThe `verbose` flag has been set to `True`\n')
    print('Summary of main function:\n')
    print(docstring, '\n')
    return None



def print_todo():
    """ 
    Prints information about outstanding issues.
    Returns None.
    """ 
    print('\n\nTO DO LIST:\n================\n')
    print('check if all definitions are in blockquote with class calibre27')
    print('Make list of children to print as is, e.g. <h2>')
    print('Test find_all instead of findChildren')
    print('Test body.descendants instead of children\n')
    print('\n================\n\n')
    return None



def print_children(soup):
    """
    Print information about all children and descendents.
    Returns None.
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



def print_child_info(child):
    """
    Print information about each dictionary entry as a child of main soup.
    Returns None.
    """
    print('child.name =', child.name)
    print('child["class"]', child['class'])
    return None



def print_types(s1, s2, s3):
    """
    Print information about types. Accepts a tuple s1, s2, s3
    Returns None.
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
    Print output to screen (useful for debugging).
    Returns None.
    """
    print('\n\nOUTPUT PRINTOUT:\n================\n', s, '\n================\n\n')
    return None



def remove_header(xml):
    """
    Remove unwanted header introduced when using the `xml` parser
    using the re module to make case insensitive replacement.
    Accepts a string. Returns a string.
    """
    import re
    h = re.escape('<?xml version="1.0" encoding="utf-8"?>') # re.escape ? and .
    r = re.sub(h, '', xml, flags=re.IGNORECASE | re.MULTILINE)
    return r



def clean_tags(soup):
    """
    Remove certain tags: '<a', 'id', 'class' from BeautifulSoup object.
    Accepts BeautifulSoup object. Returns BeautifulSoup object. 
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
    Accepts strings. Returns a string.
    """
    n = body.count('<body>')
    if n > 1:
        raise ValueError('More than one body tags found inside body!')
    if n == 0:
        body = '<body>' + body + '</body>'
    # the body element should be tagged by <body></body>
    body = BeautifulSoup(body, parser=parser).find('body')
    html = BeautifulSoup(head, parser=parser)
    html.head.insert_after(body)
    html = str(html)
    return html



def get_head(html, parser='xml'):
    """
    Extract the head from an html/xml file. 
    Accepts a string. Returns a string. 
    """
    html = BeautifulSoup(html, parser=parser)
    body = html.find('body')
    body.decompose()
    html = str(html)
    return html



def get_body(html, parser='xml'):
    """
    Extract the body from an html/xml file. 
    Accepts a string. Returns a string. 
    """
    # works only for bare body tags <body> and </body>
    if isinstance(html, str):
        r1, r2 = '^.*<body>', '^.*>ydob/<'
        body = re.sub(r2, '', re.sub(r1, '', html, flags=re.DOTALL)[::-1], flags=re.DOTALL)[::-1]
    # more general, should work if body tag has class or id
    elif isinstance(html, Tag):
        soup = BeautifulSoup(str(html), parser=parser)
        body = soup.find('body')
        body = ''.join(['%s' % x for x in soup.body.contents])
    # not currently used but kept for reference
    elif isinstance(html, BeautifulSoup):
        soup = html
        body = soup.find('body')
        body = ''.join(['%s' % x for x in soup.body.contents])
    else:
        raise ValueError('function get_body() expects either a string or a BeautifulSoup object')
    body = re.sub(r'\n+', '\n', body)
    return body




# List files to be processed
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



# Loop over all files in a given directory
def loop_away(filelist, outdir, verbose=False, clean=False, parser='xml'):
    print('PROCESSING')
    for file in filelist:
        filename = os.path.basename(file)
        outpath = os.path.join(outdir, filename)
        # hard-coded names and classes of tags that contain definitions:
        names = ['blockquote']
        classes = ['calibre27']
        # get the header from the source file
        with open(file, encoding='utf8') as infile:
            head = get_head(infile, parser=parser)
        # get the body from the source file and make it into dictionary
        with open(file) as infile, open(outpath, 'w') as outfile:
            soup = BeautifulSoup(infile, parser=parser)
            body = soup.find('body')
            for child in body.findChildren(recursive=False):
                print('■', end='', flush=True)
                if verbose:
                    print_child_info(child)
                # selected tags are printed as is
                if child.name in ['h1', 'h2', 'h3', '\n', 'link', 'table']:
                    print(child, file=outfile)
                # tags that contain dictionary definitions are processed
                elif child.name in names and any(c in child['class'] for c in classes):
                    #print('debug loop_away: check this blockquote child:', child)
                    s = str(child)
                    s = dictionarize(s, verbose=verbose, clean=clean, parser=parser)
                    s = s + '\n' # add blank line for clarity in debugging
                    print(s, file=outfile)
                else:
                    if verbose:
                        print('This child was removed:\n', child)
                    child.extract()
                    print('End.')
        # get the body from the target file and insert it into the head
        with open(outpath, 'r+') as outfile:
            body = outfile.read()
            html = make_html(body=body, head=head, parser=parser)
            outfile.seek(0)
            outfile.write(html)
            outfile.truncate()
    print('\nDONE.')
    return html
