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
    * Check case of missing or malformed tags, e.g. with missing word or line-ending slash
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


def set_metadata_language(dir):
    """
    Set the language code in the metadata <dc:language> tag by going recursively over every metadata.opf file in the Calibre library.

    Some Catalan ebooks have the language metadata incorrectly coded as:

        <dc:language>cat</dc:language>
    
    in the content.opf file. This is changed to

        <dc:language>ca</dc:language>

    and the calibre "polish books" plugin is then run on Catalan language books exclusively (by filtering by language) with "update metadata in the book file".
    """
    from pathlib import Path
    import fileinput
    # origin/destination strings:
    s0 = '<dc:language>cat</dc:language>' 
    s1 = '<dc:language>ca</dc:language>'
    # list all the candidate files in the Calibre library:
    extension = '.opf'
    files = Path(dir).rglob(f'*{extension}')
    # read each file and search for matching string, then replace in-place:
    r, i = [], 0
    for file in files:
        for line in fileinput.input(file, inplace=True):
            if line.find(s0):
                r.append(str(file))
                i += 1
                #line.replace(s0, s1)
    print(f'{i} replacements were made!')
    print('The following files were modified:\n', r)
    return r

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









# IN PROGRESS
def make_anchor(soup: BeautifulSoup, tags=[]) -> BeautifulSoup:
    """
    Loop through selected tags and create unique IDs for each.
    """
    if not tags:
        print('Aborting. You must specify a list of tags in which to place the anchor.')
        return soup
    for tag in tags:
        for item in soup.find_all(tag):
            if item.has_attr('id'):
                print('1: has id')
                if not item['id'].strip():
                    print('2: has empty id')
                    del item['id']
                else:
                    id = str(item['id'])
                    print('3: Skipping. Found tag with id attribute', id)
                    pass
        for i, j in enumerate(tags):
            print('i = ', i)
            print('j = ', j)
            item.attrs['id'] = i+1
    return soup

soup = BeautifulSoup(dml, features='lxml')
print(make_anchor(soup, tags=['blockquote']))



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


# IN PROGRESS:

def strip_spacing_from_soup(soup: BeautifulSoup, strip=False, verbose=None) -> BeautifulSoup:
    """
    Strip excess white spaces near punctuation marks, e.g. fix ' .' and ' ,'

    Args:
        soup (BeautifulSoup, Tag, NavigableString): any soup
    Returns:
        soup (BeautifulSoup, Tag, NavigableString): with excess white spaces stripped out
    Modules: 
        bs4 (BeautifulSoup), re
    """
    if verbose is None:
        if not strip:
            verbose=True
    _punctuation_spaces = re.compile(r'\s([?.!,;"](?:\s|$))')
    for item in soup.find_all():
        if item.string:
            s = re.search(_punctuation_spaces, item.string)
            if s:
                if verbose:
                    print(s)
                if strip:
                    item.string.replace_with(re.sub(_punctuation_spaces,  r'\1', item.string))
    return soup
    