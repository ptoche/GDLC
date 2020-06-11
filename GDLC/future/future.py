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


def get_root(file:str, features='lxml'):
    """
    Read an xhtml/xml/html file and extracts the root tag.

    Args: 
        file (str, BeautifulSoup, Tag): path to file or actual content
    Returns: 
        root (str)
    """
    # list of root tags:
    root_tags = ['html', 'xhtml', 'xml'] 
    # if no argument, return a default value:
    if not file:
        print('A path/to/file was not supplied. A default <root> string is returned.')
        return default_root()
    # if argument has a <root> tag, treat it as markup code:
    elif isinstance(file, str) and any(root in file for root in ['<' + i for i in root_tags]):
        string = file
    # if argument is a path/to/file, read the file and make BeautifulSoup object:
    elif pathlib.Path(str(file)).is_file():
        with open(file, encoding='utf8') as infile:
            soup = BeautifulSoup(file, features=features)
    # if argument is a BeautifulSoup Tag, convert it to a BeautifulSoup object:
    elif isinstance(file, Tag):
        string = str(file)
    # if argument is a BeautifulSoup, keep it as such
    elif isinstance(file, BeautifulSoup):
        soup = file
    # if none of the above, try anyway:
    else:
        soup = BeautifulSoup(file, features=features)
    # if not already done, convert string to BeautifulSoup object
    soup = BeautifulSoup(string, features=features)
    # get the root:
    root = soup.find(root_tags).name
    # convert to string:
    root = str(root).strip()
    return root


def make_id(text):
    """
    Loop through the entire dictionary and create unique IDs for each dictionary entry.
    """
    # TO DO
    return text


