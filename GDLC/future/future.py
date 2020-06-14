#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GDLC Development

Untested functions and features. Work in progress.

Notes:
PageElement.extract() removes a tag or string from the tree. It returns the tag or string that was extracted:
Tag.decompose() removes a tag from the tree, then completely destroys it and its contents:
The behavior of a decomposed Tag or NavigableString is not defined and you should not use it for anything.

To Do:
    * Check code for parsers other than lxml
    * Check if all definitions are in blockquote with class calibre27
    * Check case of missing or malformed tags, e.g. with missing word or line-ending slash
    * Test spacing near punctuation marks: eliminate instances of ' .' and ' ,'
    * Make the following functions:
    * get_word_class(): verb, noun, etc.
    * get_word_inflection(): tall, taller, tallest
    * get_word_pronunciation(): International Phonetic Alphabet 
    * get_word_tag(): whether words are tagged with ■ or untagged

Created 9 June 2020

@author: patricktoche
"""

import os
import re
import bs4


# IN PROGRESS
def clean_xml(xml, indent=4, method=None):
    """
    Take an xml file and return indented formatting. 
    
    Args:
        xml (str): a correctly formatted, but not indented xml page
        indent (num): size of the indent, defaults to 4
        method (str): name of the module used, one of
            'minidom': Uses minidom module from xml.dom library.
            'etree': Uses etree module from lxml library.
            'lxml': Uses the BeautifulSoup module from bs4 library and the lxml parser. 

    Return:
        xml (str): an indented xml page
    
    Modules: bs4 (BeautifulSoup)
    
    Modules: A wrapper around several modules, written to help selecting method and for debugging xml code.
    """
    if method == 'minidom':
        return clean_xml_dom_minidom(xml, indent=indent)
    if method == 'etree':
        return clean_lxml_etree(xml)
    if method == 'lxml':
        return clean_bs4_lxml(xml)
    return print('`clean_xml()` is a wrapper around several methods based on different libraries. No default method selected. Current choices are:  "minidom", "etree", "lxml"\n')


# IN PROGRESS
def clean_xml_dom_minidom(xml, indent=4):
    """
    Take an xml file and return indented formatting. 

    Modules: xml.dom (minidom)
    """
    from xml.dom import minidom
    from xml.etree.cElementTree import Element, tostring
    root = Element('root')
    xml = minidom.parseString(tostring(root)).toprettyxml(indent=' '*indent)
    return xml


# IN PROGRESS
def clean_lxml_etree(xml):
    """
    Take an xml file and return indented formatting. 

    Modules: lxml (etree)
    """
    from lxml import etree
    parser = etree.XMLParser(resolve_entities=False, strip_cdata=False)
    etree.set_default_parser(parser)
    xml = etree.fromstring(xml)
    xml = parse(xml, parser)
    xml = parser.write(xml, pretty_print=True, xml_declaration=True, encoding='utf-8')
    return xml


# IN PROGRESS
def clean_bs4_lxml(xml, indent=4):
    """
    Take an xml file and return indented formatting. 

    Modules: bs4 (BeautifulSoup), lxml
    """
    # from bs4 import BeautifulSoup  # already imported
    for line in xml: 
        print(BeautifulSoup(line, features='lxml').prettify())
    return xml

# IN PROGRESS
def validate_xml(xml:str):
    """
    XHTML is a markup language that is designed by combining XML and HTML. 
    XHTML can be seen as a cleaner version of HTML, which is also stricter than HTML. 
    XHTML is a W3C recommendation. 

    Modules: lxml, StringIO
    """
    from lxml import etree
    from StringIO import StringIO
    etree.parse(StringIO(xml), etree.HTMLParser(recover=False))



# Clean selected xml files:
files = outfilelist[149:150]
for file in files:
    base, ext = os.path.splitext(file)
    out = base+'_cleaned'+ext
    with open(file, 'r') as infile, open(out, 'w') as outfile:
        dml = clean_xml(infile, method='lxml')
        print(dml, file=outfile)
        #outfile.write(dml)
        #print(dml, file=outfile)

# Clean xml files inside Text directory:
dir = '/Users/PatrickToche/GDLC/output/GDLC_processed/mobi8/OEBPS/Text'
for root, dirs, files in os.walk(dir):
    for file in files:
        if file.endswith('.xhtml'):
            base, ext = os.path.splitext(file)
            out = base+'_cleaned'+ext
            dml = clean_xml(os.path.join(root, file), method='lxml')
            with open(out, 'w') as outfile:
                    outfile.write(str(dml))






# IN PROGRESS: TO DO
def clean_anchors(xml):
    """
    Take an xml file and recode anchor locations.
    Anchors with hyphens can cause errors. 
    Modules: 
    STEPS:
    Make a list of every anchor in directory files. 
    Make unique.
    Make a list of replacement anchors.
    Replace.
    return xml

    """

def make_id(text):
    """
    Loop through the entire dictionary and create unique IDs for each dictionary entry.
    """
    # TO DO
    return text




def get_root(dml, features='lxml'):
    """
    Wrapper for document markup language.

    Functions : 
        `markup_handler()`, `get_root_from_soup()`.
    """
    soup = markup_handler(dml, features=features)
    soup = get_root_from_soup(soup)
    return soup



def get_root_from_soup(soup:BeautifulSoup):
    """
    Read an xhtml/xml/html file and extracts the root tag. 

    Args: 
        soup (BeautifulSoup): markup language as BeautifulSoup object
    Returns: 
        root (str): <root> of the page
    Modules: 
        bs4 (BeautifulSoup)
    Note:
        See also: `get_pi()`
    """
    # list of root tags:
    root_tags = ['html', 'xhtml', 'xml'] 
    # get the root:
    tags = soup.find_all(root_tags)
    if not tags:
        return ''
    for t in tags:
        ''.join(str(t.contents))
    # TO DO : FIX THIS!
    # 'xml' not found
    # 'html' is the whole document
    # soup_find('html').attrs yields a list instead of properly formed tag ...
    return root








###### 6 June 2020

# IN PROGRESS: run a clean_xml action on the directory, clean_anchors

# TO DO: MAKE FUNCTION TO SELECT PAGES TO PROCESS
skip = [0:16]+[276:278]

def make_range(arg*):
    arg = map(int, arg.split(":"))
    r = list(range(0,10000))
    print ary[arg[0]:arg[1]]

r = list(range(0,16))

# Skip files 000-015 and 276-277
f = filelist[16:277]
f = filelist[16:277]

# Copy files 000-015 and 276-277 from source
f = filelist[0:16] + filelist[276:278]
import shutil
for file in f:
    shutil.copy(file, outdir)






if 'warn' not in sys.modules:
    from warnings import warn


# IN PROGRESS:
def make_kindle():
    """ 
    Invoke kindlegen to build ebook from files.

    /Users/patricktoche/kindlegen/KindleGen_Mac_i386_v2_9/kindlegen 

    """ 





>>> from GDLC.GDLC import *
>>> dml = '''<?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml">
... <head>
... <title>TITLE</title>
... </head>
... <body>
... <h1>A valid h1 tag <script>with an invalid script tag</script>.</h1>
... <div><script>An invalid script tag inside a valid div tag.</script></div>
... </body>
... </html>'''
>>> soup = BeautifulSoup(dml, features='lxml')




# IN PROGRESS
>>> soup = BeautifulSoup(dml, features='lxml')

>>> soup.find('html').attrs

>>> from bs4 import NavigableString as ns
>>> namespaces = {}
>>> for attr in soup.find('html').attrs:
>>>     if attr.startswith("xmlns") or ":" in attr:
            namespaces[attr] = soup.find('html')[attr].split(" ")

>>> [tag.attrs for tag in soup.find_all('html') if not ns]


soup.find_all(['h{}'.format(i) for i in range(1,7)])

