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
# Summarize the meta info in xhtml files
# Use a multi-level dictionary?
def get_meta(dir, tags=[], encoding='utf8', features='lxml'):
    """
    Wrapper to read meta content of document markup language (dml) file. 

    Args:
        dir(str, BeautifulSoup): directory to a dictionary written in document markup language
        tags ([str]): list of tags of interest, e.g. tags=['title', 'language']
        encoding (str): encoding used, default is 'utf8'
        features (str): parser used, default is 'lxml'
    Functions : 
        `dir_handler()`, `get_meta_dml_from_soup()`.
    """ 
    # set up source directory:
    if not dir:
        home = Path.home()
        dir = home / 'GDLC/output/GDLC_processed'       
    dir = dir_handler(dir, mkdir=False)
    # read content from xhtml files:
    dir = dir / 'mobi8/OEBPS/Text'  # this part of tree is fixed
    files = [e for e in path.iterdir() if e.is_file()]
    file = dir /

    # list of meta tags of interest:
    if tags and not isinstance(tags, list):  # allow tags='list'
        tags = [tags]
    if not tags:
        tags = ['idx:entry', 'idx:orth', 'idx:infl', 'idx:iform']
        attr = ['name', 'scriptable', 'spell']

        tags = {'idx:entry': ['name', 'scriptable', 'spell'],
                'idx:orth': []}


    # get attributes from the opf file:
    with open(file, encoding=encoding) as infile:
        soup = BeautifulSoup(infile, features=features)
        content = get_meta_dml_from_soup(soup, tags=tags)
    return content



# IN PROGRESS
def check_content(dir, encoding='utf8', features='lxml'):
    """
    Check that various attributes stated in content.opf are internally consistent.
    Loops through all text files looking for inconsistencies with content.opf.

    Args:
        dir(str, BeautifulSoup): directory to a dictionary written in document markup language
        encoding (str): encoding used, default is 'utf8'
        features (str): parser used, default is 'lxml'
    
    Returns:
        entry ({str:str}): a dictionary of entries where problems were detected 
    
    Notes: 
        The <idx:entry> tag can carry the name, scriptable, and spell attributes. The name attribute indicates the index to which the headword belongs. The value of the name attribute should be the same as the default lookup index name listed in the OPF. The scriptable attribute makes the entry accessible from the index. The only possible value for the scriptable attribute is "yes". The spell attribute enables wildcard search and spell correction during word lookup. The only possible value for the spell attribute is "yes". 
    Checks:
        name, scriptable, spell
    To do:
        Check identifier X match in <package unique-identifier="X" and <dc:identifier id="X", as in below:
        <package version="2.0" xmlns="http://www.idpf.org/2007/opf" unique-identifier="uid">
        <dc:identifier id="uid">B00DZWFUG4-LookUp-mobi8</dc:identifier>
    """
    # set up the directory to content.opf
    dir = dir_handler(dir, mkdir=False)
    # get meta data from the opf file:
    meta_opf = get_meta_opf(dir)
    # get attributes from the dml files:
    meta_dml = get_meta_dml(dir)
    # store file names and meta tags if problem detected:
    d = {}
    # attribute "spell" only value is "yes"
    for item in meta_opf:
        if item.lower() != 'yes':
            
        for key, value in d.items():
            do stuff

    # check attributes in each entry in all dml files.
    for file in filelist:
        with open():
            for entry in entrylist:
                # check the name attribute:
                if attr == opf_attr:
                    lst.append(True)
                else:
                    lst.append(False)









# IN PROGRESS
def check_toc(dir, encoding='utf8'):
    """
    Check that various attributes stated in toc.ncx are internally consistent.
    Loops through all text files looking for inconsistencies with toc.ncx.

    Args:
        dir(str, BeautifulSoup): directory to a dictionary written in document markup language.
        encoding (str): encoding used, default is 'utf8'.
    
    Returns:
        entry ({str:str}): a dictionary of entries where problems were detected. 
    """
    if dir:
        dir = Path(dir).expanduser()
    else:
        home = Path.home()
        dir = home / 'GDLC/output/GDLC_processed'
    if not dir.is_dir():
        return print('Aborting. The following directory was not found:\n\n', dir)
    # get attributes from toc.ncx:
    get attributes from toc.ncx:
    file = dir / 'mobi8/OEBPS/toc.ncx'
    # TO DO











def make_anchor(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Loop through every <h1>, <h2> tag and insert an id designed to guide navigation.

    Convert elements such as
        <h2 class="centrat2" id="aid-F8901">A</h2>
    to
        <h2 class="centrat2" id="nav001">A</h2>
    """


        




# IN PROGRESS:
def make_entry_id(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Loop through the entire dictionary and create unique IDs for each dictionary entry.
    """
    # TO DO
    tags = soup.find_all('idx:entry')
    for tag in tags:
        # if <idx:entry> has an id, suppress it:
        for attr in tag.attrs('id'):
            del tag.attr
        for i, j in enumerate(tags):
            tag.attrs['id'] = i
            tag.attrs.append(('id', i))
            # ETC

def make_entry_id_from_name(soup: BeautifulSoup) -> BeautifulSoup:
    # TO DO
    for anchor in soup.html.find_all('a'):
        if anchor.has_attr('name'):
            anchor['id'] = anchor['name']
            del anchor['name']



# IN PROGRESS:
def make_kindle():
    """ 
    Invoke kindlegen to build ebook from files.

    /Users/patricktoche/kindlegen/KindleGen_Mac_i386_v2_9/kindlegen 
    """ 
