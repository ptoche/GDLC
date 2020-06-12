#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GDLC Development

Untested functions and features. Work in progress.

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

from bs4 import BeautifulSoup, Tag
from bs4 import NavigableString, Comment


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



def default_root():
    root = '''\
<html xmlns:math="http://exslt.org/math" \
xmlns:svg="http://www.w3.org/2000/svg" \
xmlns:tl="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf" \
xmlns:saxon="http://saxon.sf.net/" \
xmlns:xs="http://www.w3.org/2001/XMLSchema" \
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \
xmlns:cx="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf" \
xmlns:dc="http://purl.org/dc/elements/1.1/" \
xmlns:mbp="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf" \
xmlns:mmc="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf" \
xmlns:idx="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf">'''
    return root


def make_id(text):
    """
    Loop through the entire dictionary and create unique IDs for each dictionary entry.
    """
    # TO DO
    return text


# TEST THIS:
def print_function_name():
    """
    Return the name of the caller (function or method). 
    
    Modules: sys (_getframe)
    """
    if '_getframe' not in sys.modules:
        from sys import _getframe
    return sys._getframe().f_code.co_name




def get_html_attrs(dml, features='lxml'):
    """
    Wrapper for document markup language.

    Functions : 
        `markup_handler()`, `get_html_attrs_from_soup()`.
    """
    soup = markup_handler(dml, features=features)
    soup = get_html_attrs_from_soup(soup)
    return soup


def get_html_attrs_from_soup(soup:BeautifulSoup):
    '''
    Read an xhtml/xml/html file and extracts the <html> tag.

    Args: 
        soup (BeautifulSoup): markup language as BeautifulSoup object
    Returns: 
        attr (str): <processing instructions> of the page
    Modules: 
        bs4 (BeautifulSoup)
    '''
    # get the <html> tag and attributes:
    attr = soup.find('html').attrs
    return attr




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

