#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gran Diccionari de la llengua catalana

Functions to edit the xhtml source code for the GDLC (Kindle edition).

Written for the 'Gran diccionari de la llengua catalana' published by Institut d'Estudis Catalans in 2013, purchased from Amazon for 6 euros and downloaded in the `mobi` format. 

After conversion to the azw format via the Calibre plugin KindleUnpack, the dictionary entries appear as well-formed blocks of document markup language code. 

The code loops through the blocks and formats them one at a time. The code may hopefully be adapted to other dictionaries, but almost certainly will not work without alterations. 

Example:
    A dictionary entry may be converted to a lookup dictionary definition with

        $ GDLC.make_entry(string)

    make_entry() calls the following functions:
        split_entry()
            make_label()
            make_headword()
            make_definition()
    and concatenates label, headword, and definition into a dictionary entry.

    For examples of usage see inside `run.py`.
    The core code of module GDLC is in `GDLC.py`.
    A test suite for the module is in the `tests` directory. See `tests/tests.py` for details. 
    Log files are saved in the `logs` directory.  See `logs/logs.py` for details. 
    Elements involving interaction with the user are in the `queries` directory. See `queries/query.py` for details. 
    Future developments and work in progress are in the `future` directory. See `future/future.py` for details.
    There is no documentation for this project. Limited info may be found in the `docs` directory and inside docstrings. 

Args:
    verbose, clean, and features are common arguments of several functions. Their description is not repeated inside each function. 
    verbose (bool, optional): Set to True to print more information (useful for debugging).
    clean (bool, optional): Set to True to remove classes, ids, and other style-specific attributes: conforms more with the style of dictionary definitions seen in unpacked mobi files. Set to False to keep some of that information: conforms more with the style of dictionary definitions seen in unpacked azw files. 
    features (str, optional): Sets the parser to be used with BeautifulSoup. Defaults to 'lxml'. 

Returns:
    main_loop() reads the GDLC dictionary source files, edits them, and saves them into a format and directory structure that Amazon's KindleGen understands.
    make_entry() reads an entry from the GDLC dictionary text files and returns an entry conforming with the following template:

    <idx:entry scriptable="yes">
...   <idx:orth value="ABC">
...     <idx:infl>
...       <idx:iform name="" value="ABC"/>
...     </idx:infl>
...   </idx:orth><div><span><b>ABC</b></span></div><span><strong">ABC -xy</strong></code><sup class="calibre23">1</sup>.</span><div><blockquote class="calibre27" id="d34421">
    <blockquote><span>Definition here.</span></blockquote>
    </blockquote></div>
    </idx:entry> 

Created 3 May 2020

@author: patricktoche
"""
import os
import sys
import io
import pathlib
import re

import bs4
from bs4 import BeautifulSoup, Tag, NavigableString, Comment

import pprint
import progressbar  # !!  progressbar2 under the hood



def copy_dirtree(indir, outdir, onerror=None):
    """ 
    Copy the directory structure found in directory `indir` to directory `outdir`.

    Args:
        indir (str): the directory whose structure is to be copied
        outdir (str): the directory to which the structure will be copied
    Returns:
        [indir, outdir] ([str]): returns the input path strings
    Modules: 
        os
    """ 
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    base = len(indir) + len(os.path.sep)
    for root, dirs, files in os.walk(indir, onerror=onerror):
        for dirname in dirs:
            dirpath = os.path.join(outdir, root[base:], dirname)
            if os.path.exists(dirpath):
                print('Directory\n', dirpath, '\n already exists at destination\n')
            else:
                try:
                    os.mkdir(dirpath)
                    print('Directory\n', dirpath, '\n was copied to destination\n')
                except OSError as e:
                    if onerror is not None:
                        onerror(e)
    return [indir, outdir]


def copy_files(files=[], dir=None, source=None, mkdir=False):
    """ 
    Copy files in given list to selected directory. 
    Destination directory will be created if it does not exist. 

    Modules: 
        pathlib (Path), shutil (copy2), warnings (warn)
    Functions: 
        `default_copy()`
    """ 
    import sys
    if 'copy2' not in sys.modules:
        from shutil import copy2  # shutil.copy2 copies metadata+permissions
    if 'Path' not in sys.modules:
        from pathlib import Path, PosixPath
    if dir:
        dir = Path(dir).expanduser()
    # set up a default directory to copy the files to if none is supplied:
    if not dir:
        # get the user's home directory:
        home = Path.home()
        dir = home / 'tmp'
    # abort if the directory is invalid:
    if not dir.is_dir():
        return print('Aborting. The specified dir argument must be a valid directory.\nExample of usage: `copy_files(dir = "~/tmp")`\nIf the directory does not exist, it will be created if `mkdir=True`.')
    # abort if the directory does not exist:
    if not dir.exists():
        if not mkdir:
            return print('Aborting. No directory found at destination. To create directory, set `mkdir=True`.')
        else:
            Path(dir).mkdir(parents=True)
    # if no files given, get the default list:
    if not files:
        if not source:
            source = home / 'GDLC/source/GDLC_unpacked'
        files = default_copy(dir=source)
    # copy files to destination:
    print('\nThe following files are being copied:\n')
    copies = []
    for file in files:
        # ensure files are of type PosixPath:
        if not isinstance(file, PosixPath):
            file = Path(file).expanduser()
        # if a file does not exist, inform the user:
        if not file.is_file():
            print('The following file was not found:\n\n', file, '\n')
        copy = dir / file.name
        try:
            copy2(file, copy)
            print('\n', file, '\n\n copied to:\n\n', copy, '\n')
            copies.append(copy)
        except Exception as e:
            print("type error: " + str(e))
    return copies


def default_copy(dir=None):
    """
    Lists all files to be copied from source directory to destination.
    The file list is hard coded. Files may be added/removed as I understand file structure better.

    Usage:
        `default_copy(dir='~/GDLC/source/GDLC_unpacked')`
    Modules:
            pathlib (Path)
    Notes:
        The following directories remain empty: HDImages, mobi8/OEBPS/Fonts 
        An alternative is to copy the entire source directory!
    """
    # make sure the pathlib.Path module is imported:
    import sys
    if 'Path' not in sys.modules:
        from pathlib import Path
    if not dir:
        return print('Aborting. A directory for source files must be supplied')
    else:
        dir = Path(dir).expanduser()
    # build the file list incrementally:
    files, filez = [], []
    filez.append('mobi7/Images/author_footer.jpeg')
    filez.append('mobi7/Images/author_image.jpeg')
    filez.append('mobi7/Images/cover_image.jpeg')
    filez.append('mobi7/Images/cover_logo.jpeg')
    filez.append('mobi7/Images/cover_thumb.jpeg')
    filez.append('mobi8/mimetype')
    filez.append('mobi8/META-INF/container.xml')
    filez.append('mobi8/OEBPS/content.opf')
    filez.append('mobi8/OEBPS/toc.ncx')
    filez.append('mobi8/OEBPS/Styles/style0001.css')
    filez.append('mobi8/OEBPS/Styles/style0002.css')
    filez.append('mobi8/OEBPS/Styles/style0003.css')
    filez.append('mobi8/OEBPS/Images/author_footer.jpeg')
    filez.append('mobi8/OEBPS/Images/author_image.jpeg')
    filez.append('mobi8/OEBPS/Images/cover_image.jpeg')
    filez.append('mobi8/OEBPS/Images/cover_logo.jpeg')
    filez.append('mobi8/OEBPS/Text/cover_page.xhtml')
    for file in filez:
        f = dir / file
        if f.is_file():
            files.append(f)
        else:
            print('The following file was not found:\n', f)
    return files


def default_head():
    """Returns the default xml <head> tag"""
    return '''<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head>'''


def default_root():
    """Returns the default Amazon Kindle dictionary <root> tag"""
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


def destroy_tags(soup:BeautifulSoup, *args:str):
    """
    Suppress tag and tag content for tags that the kindle does not support.
    By default, removes <script> and <style>.

    Args: 
        soup (BeautifulSoup): html content with unsupported tags
        args (str): name of the tags to be destroyed
    Returns: 
        soup (BeautifulSoup): original soup with selected tags destroyed
    Usage: 
        destroy_tag(soup, 'code', 'script')
    Modules: 
        bs4 (BeautifulSoup)
    """
    # always destroy these tags:
    tagz = ['script', 'style']
    # add tags to list if found in args:
    if args:
        tagz.extend(args)
    for tag in tagz:
        for item in soup.find_all(tag):
            item.extract(strip=True)
    return soup


# PATCH for BeautifulSoup extract() method
from bs4 import PageElement
def extract_patched(self, _self_index=None, strip=False):
    """A patched version of the BeautifulSoup `.extract()` method. 
    Optional argument `strip=True` suppresses empty lines. 
    Notes: 
        Will be deprecated and replaced by proper use of method `.smooth()`.
    
    Original docstring below this line.

    Destructively rips this element out of the tree.

    :param _self_index: The location of this element in its parent's
       .contents, if known. Passing this in allows for a performance
       optimization.

    :return: `self`, no longer part of the tree.
    """
    if self.parent is not None:
        if _self_index is None:
            _self_index = self.parent.index(self)
        del self.parent.contents[_self_index]

        # ! PATCH STARTS HERE !
        # remove empty line introduced by extract():
        # check that nearby parent.contents is really empty before deleting
        if strip:
            try:
                for i in range(_self_index-1, _self_index+1):
                    if str(self.parent.contents[i]).strip() == '':
                        del self.parent.contents[i]
            except: 
                pass
        # ! PATCH ENDS HERE !
    
    #Find the two elements that would be next to each other if
    #this element (and any children) hadn't been parsed. Connect
    #the two.
    last_child = self._last_descendant()
    next_element = last_child.next_element

    if (self.previous_element is not None and
        self.previous_element is not next_element):
        self.previous_element.next_element = next_element
    if next_element is not None and next_element is not self.previous_element:
        next_element.previous_element = self.previous_element
    self.previous_element = None
    last_child.next_element = None

    self.parent = None
    if (self.previous_sibling is not None
        and self.previous_sibling is not self.next_sibling):
        self.previous_sibling.next_sibling = self.next_sibling
    if (self.next_sibling is not None
        and self.next_sibling is not self.previous_sibling):
        self.next_sibling.previous_sibling = self.previous_sibling
    self.previous_sibling = self.next_sibling = None

    return self
# ! APPLY PATCH !
PageElement.extract = extract_patched


def markup_handler(input, invalid_types=[], features='lxml'):
    """
    Directs input to BeautifulSoup parser based on input type. 

    Args:
        input (str, BeautifulSoup, Tag): path to file or actual content.
    Returns:
        soup (BeautifulSoup): BeautifulSoup object ready for further processing. 
    Modules: 
        bs4 (BeautifulSoup, Tag, NavigableString)
    """
    # if input is of invalid_type, raise an exception:
    if type(input) in invalid_types:
        print('Aborting. The input type was listed among the `invalid_types`.')
        return None
    # !all BeautifulSoup objects are also Tag objects, 
        # but not the converse, 
            # so check Beautifulsoup first!
    # import Path module to handle a file path as input:
    if 'Path' not in sys.modules:
        from pathlib import Path
    # set string variable to None:
    string = None
    # if no argument, return None:
    if not input:
        print('Function `markup_handler()` takes 1 argument. None detected.')
        return None
    # if argument is string, treat it as markup code:
    elif isinstance(input, str):
        string = input
    # if argument is a BeautifulSoup, keep it as such:
    elif isinstance(input, BeautifulSoup):
        soup = input
    # if argument is a Tag, convert it to a BeautifulSoup object:
    elif isinstance(input, Tag):
        string = str(input)
    # if argument is a NavigableString, get the string:
    elif isinstance(input, NavigableString):
        string = input.string
    # if argument is a path/to/file, read the file and make BeautifulSoup object:
    # set maximum path length to 260 characters, like Windows does.
    elif isinstance(input, str) and len(input)<260 and pathlib.Path(input).is_file():
        with open(input, encoding='utf8') as infile:
            soup = BeautifulSoup(infile, features=features)
    # if none of the above, try anyway:
    else:
        try:
            soup = BeautifulSoup(input, features=features)
        except:  # here for debugging purposes
            raise ValueError('A string, NavigableString, Tag, or BeautifulSoup object was expected.')
    # convert string to BeautifulSoup object:
    if string:
        soup = BeautifulSoup(string, features=features)
    # return a BeautifulSoup object:
    return soup


def get_body(dml, features='lxml'):
    """
    Wrapper for document markup language.

    Functions : 
        `markup_handler()`, `get_body_from_soup()`.
    """
    soup = markup_handler(dml, features=features)
    soup = get_body_from_soup(soup)
    return soup


def get_body_from_soup(soup:BeautifulSoup):
    """
    Extract <body> tag from a BeautifulSoup object.
    Also tries to suppress excess blank lines. 

    Args: 
        soup (BeautifulSoup): markup language as BeautifulSoup object
    Returns: 
        body (str): <body> of the page
    Modules: 
        bs4 (BeautifulSoup), re
    """
    body = soup.find('body')
    body = ''.join(['%s' % x for x in body])
    body = re.sub(r'\n+', '\n', body).strip()  # .strip() removes leading/trailing blankspaces/newlines
    return body


def get_doctype(dml, features='lxml'):
    """
    Wrapper for document markup language.

    Functions : 
        `markup_handler()`, `get_doctype_from_soup()`.
    """
    soup = markup_handler(dml, features=features)
    soup = get_doctype_from_soup(soup)
    return soup


def get_doctype_from_soup(soup):
    """
    Extract <!Doctype> declaration from a BeautifulSoup object.

    Modules: 
        bs4 (BeautifulSoup), bs4 (Doctype)
    """
    items = [item for item in soup.contents if isinstance(item, bs4.Doctype)]
    doctype = items[0] if items else None
    return  doctype


def get_duplicate_id(dml):
    """
    Wrapper for document markup language.

    Functions : 
        `get_sorted_id`.
    """
    id_sorted = get_sorted_id(dml)
    id_duplicate = id_sorted['duplicate']
    return id_duplicate


def get_function_name():
    """
    Return the name of the caller (function or method). 
    
    Modules: sys (_getframe)
    """
    if '_getframe' not in sys.modules:
        from sys import _getframe
    return sys._getframe().f_code.co_name


def get_head(dml, features='lxml'):
    """
    Wrapper for document markup language.

    Functions : 
        `markup_handler()`, `get_head_from_soup()`.
    """
    soup = markup_handler(dml, features=features)
    soup = get_head_from_soup(soup)
    return soup


def get_head_from_soup(soup:BeautifulSoup):
    """
    Extract the <head> tag from a BeautifulSoup object.

    Args: 
        input (BeautifulSoup): markup language as BeautifulSoup object
    Returns: 
        head (str): <head> of the page
    Modules: 
        bs4 (BeautifulSoup)
    """
    # get the head:
    head = soup.find('head')
    # convert to string:
    head = str(head).strip()
    return head


def get_headword(tag):
    """
    Extract the content of a BeautifulSoup element Tag object.

    Args:
        tag (Tag): a BeautifulSoup element tag, obtained by extracting from a soup
    Returns:
        short, long ([str]): short and long form of a word in dictionary definition
    Modules: 
        bs4 (BeautifulSoup)
    """
    if not isinstance(tag, Tag):
        print('`get_headword()` only accepts objects of type Tag')
    # check for existence of <p> tag:
    if tag.find_all('p'):
        text = tag.p
    else:
        text = tag
    # extract the headword:
    short = text.get_text()
    # extract first part:
    short = short.split(' ', 1)[0]
    # remove non-alphabetical characters, including black squares:
    regex = re.compile('[^a-zA-Z]')
    short = regex.sub('', short).strip('■')
    # extract whole headword string without tags:
    long = ''
    for child in text.children:
        long += str(child)
    return [short, long]


def get_html_attrs(dml, features='lxml'):
    """
    Wrapper for document markup language.

    Functions : 
        `markup_handler()`, `get_html_attrs_from_soup()`.
    """
    if type(dml) not in [str, BeautifulSoup]:
        print('Aborting. Only objects of type str and BeautifulSoup are expected to have <html> attributes.')
        return None
    soup = markup_handler(dml, features=features)
    soup = get_html_attrs_from_soup(soup)
    return soup


def get_html_attrs_from_soup(soup:BeautifulSoup):
    """
    Read an xhtml/xml/html file and extracts the <html> tag.

    Args: 
        soup (BeautifulSoup): markup language as BeautifulSoup object
    Returns: 
        attr (str): <processing instructions> of the page
    Modules: 
        bs4 (BeautifulSoup)
    """
    # get the <html> tag and attributes:
    attr = soup.find('html').attrs
    return attr


def get_pi(dml, features='lxml'):
    """
    Wrapper for document markup language.

    Functions : 
        `markup_handler()`, `get_pi_from_soup()`.
    """
    soup = markup_handler(dml, features=features)
    soup = get_pi_from_soup(soup)
    return soup


def get_pi_from_soup(soup:BeautifulSoup):
    """
    Extract the processing instructions from a BeautifulSoup object.

    Args: 
        soup (BeautifulSoup): markup language as BeautifulSoup object
    Returns: 
        pi (str): <processing instructions> of the page
    Modules: 
        bs4 (BeautifulSoup), bs4 (ProcessingInstruction)
    Notes:
        See `get_root()`
    """
    items = [item for item in soup if isinstance(item, bs4.element.ProcessingInstruction)]
    pi = items[0] if items else None
    return pi


def get_sorted_id(dml, features='lxml'):
    """
    Wrapper for document markup language.

    Functions : 
        `markup_handler()`, `get_sorted_id_from_soup()`.
    """
    soup = markup_handler(dml, features=features)
    id_sorted = get_sorted_id_from_soup(soup)
    return id_sorted


def get_sorted_id_from_soup(soup:BeautifulSoup):
    """
    Sorts unique and duplicated IDs in a dynamic markup language document.

    Args:
        soup (BeautifulSoup): markup language as BeautifulSoup object
    Returns:
        unique, duplicate ({}): two lists for unique and duplicated IDs
    Modules: 
        bs4 (BeautifulSoup)
    """
    unique, dupe = [], []
    for tag in soup.find_all(attrs={'id':True}):
        id = tag.get('id')
        if id not in unique:
            unique.append(id)
        else:
            dupe.append(id)
    sorted = {'unique': unique, 'duplicate': dupe}
    return sorted


def get_unique_id(dml):
    """
    Wrapper for document markup language.

    Functions : 
        `get_sorted_id`.
    """
    id_sorted = get_sorted_id(dml)
    id_unique = id_sorted['unique']
    return id_unique


def list_files_all(dir):
    """ 
    List files in the given directory.

    Args:
        dir (str): path to a directory
    Returns:
        lst ([str]): list of filenames in directory
    Modules: 
        os
    """
    lst = []
    for path, subdirs, files in os.walk(dir):
        for name in files:
            lst.append(os.path.join(path, name))
    return lst


def list_files_range(filename, first=None, last=None):
    """ 
    List files within a given range based on filenames of type `part0001.xhtml`.
    Designed for mobi files broken up into several numbered files. 

    Args:
        filename (str): path to a typical file (including extension)
        first (num): first file name to be included
        last (num): last file name to be included
    Returns:
        lst ([str]): list of selected filenames (including path) in directory
    Modules: 
        os, re
    """
    lst = []
    path = os.path.dirname(filename)
    name = os.path.basename(filename)
    base, ext = os.path.splitext(name)
    part = re.split(r'(\d+)', base)[0]
    init = int(re.split(r'(\d+)', base)[1])
    if first is not None:
        init = first
    else:
        init = 0
    i = init
    def new_name(i):
        nn = os.path.join(path, part) + str(i).zfill(4) + ext
        return nn
    n = new_name(i)
    if last is not None:
        while i < (last+1):
            i += 1
            lst.append(n)
            n = new_name(i)
    else:
        while os.path.exists(n):
            i += 1
            lst.append(n)
            n = new_name(i)
    return lst


def list_files_ignore(ignore_list, dir):
    """ 
    List files in the given directory.

    Args:
        ignore_list ([str]): list of filenames (excluding path) to be ignored
        dir (str): path to a directory
    Returns:
        lst ([str]): list of filenames (including path) to be ignored in directory
    Modules: 
        os
    """
    lst = []
    if not ignore_list:
        return lst
    else:
        for path, subdirs, files in os.walk(dir):
            for name in files:
                if name in ignore_list:
                    lst.append(os.path.join(path, name))
    return lst


def list_invalid_tags(soup, valid=[]):
    """
    Make a list of tags that the kindle does not support.

    Args: 
        soup (BeautifulSoup): html content with unsupported tags
        valid ([str]): list of valid tags. Defaults to list provided by Amazon
    Returns: 
        invalid ([str]): list of tags that are not in the lits of valid tags
    Modules: 
        bs4 (BeautifulSoup)
    Functions:
        `list_valid_tags()` 
    """
    # initiate lists:
    tags, invalid = [], []
    # set the list of valid/permitted tags:
    if not valid:
        valid = list_valid_tags()
    # list all unique tags found in soup:
    for tag in soup.find_all(): 
        if tag.name not in tags:
            tags.append(str(tag.name))
    # keep only the tags that are not in valid:
    invalid = [tag for tag in tags if tag not in valid]
    return invalid


def list_invalid_tags_kf8():
    """
    List of tags that are invalid and/or deprecated in Kindle Format 8.
    Reference: https://kdp.amazon.com/en_US/help/topic/GG5R7N649LECKP7U
    """
    return ['audio', 'base', 'big', 'canvas', 'center', 'command', 'datalist', 'eventsource', 'font', 'form', 'iframe', 'input', 'keygen', 'marquee', 'noscript', 'param', 'script', 'video']


def list_valid_tags():
    """
    List of tags permitted in book content.
    Reference: https://kdp.amazon.com/en_US/help/topic/G200673180
    """
    return ['a', 'b', 'big', 'blockquote', 'body', 'br', 'center', 'cite', 'dd', 'del', 'dfn', 'div', 'em', 'font', 'head', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'html', 'i', 'img', 'li', 'ol', 'p', 's', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'u', 'ul', 'var']


# TO DO: UNDER CONSTRUCTION/REPAIR
def main_loop(files, dir=None, tags=None, protected=None, classes=None, verbose=False, clean=False, features='lxml', progress=True):
    """
    Loop over all files in a given directory.

    Args:
        files ([str]): list of file names to be processed (full path/to/file).
        dir (str): path to output directory. Defaults to 'root/tmp'.
        tags ([str]): list of tag names that contain definitions to be processed. 
        protected([str]): list of tag names to be printed without changes.
        classes([str]): list of class names that contain definitions to be processed. 
        verbose (bool): if True, selected information is printed to the console. Used for debugging.
        clean (bool): if True, non-fundamental tags and classes are removed.
        features (str): specifies the parser used by BeautifulSoup. Defaults to 'lxml'.
        progress (bool, optional): progressbar depends on module progressbar2, can be turned off.
    Returns:
        None
    Modules: 
        os, pathlib (Path), bs4 (BeautifulSoup), GDLC (queries)
    Functions: 
        `query_yes_no()`, `get_head()`, `make_entry()`, `make_dml()`, `print_child_info()`
    Notes:
        UNDER REPAIR
    TO DO: 
        FIX progressbar, test arguments, add thorough test file, break up if possible.
    """ 
    # set up output directory. If default directory `tmp` does not exist, create it:
    if not dir:
        dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'tmp'))
        from pathlib import Path
        Path('tmp').mkdir(parents=True, exist_ok=True)
    print('\nYour output files will be saved in ', dir, '\n')
    print('Make sure a directory exists at the location.\n')
    print('Set `dir` in function `main_loop` to change the default directory.\n')
    print('WARNING: Destination files will be overwritten.\n')

    # ask user to validate a job that can take a while and overwrite files:
    from GDLC.queries.query import query_yes_no
    validate = query_yes_no('You are about to start processing multiple dictionary files.\n\nExisting files will be overwritten!\n\nDo you want to proceed?\n')
    if validate in ['no']:
        return print('Loop aborted by user!')
    
    # set up a progress bar for long jobs:
    # widgets = [progressbar.Percentage(), progressbar.Bar()]
    # bar = progressbar.ProgressBar(widgets=widgets, max_value=10)
    # initialize the progress bar:
    # bar.start()
    
    # set up a container to hold a list of files that raise an error:
    errors = []

    # set up tag/class to be processed and tags that are protected:
    # set up default lists:
    entry_tag_default = ['blockquote']
    entry_class_default = ['calibre27']
    protected_default = ['h1', 'h2', 'h3', '\n']
    # ignore defaults if set by user
    if not tags:
        tags = entry_tag_default
    if not classes:
        classes = entry_class_default
    if not protected:
        protected = protected_default

    # start the main loop:
    for file in files:
        # set up the full path to the output file based on the name of the input file:
        basename = os.path.basename(file)
        outfilename = os.path.join(dir, basename)
        # try to read input files and write to output files:
        try:
            print('\n\nPROCESSING FILE', file, ':\n')
            # open a source file to read the <head> tag:
            with open(file, encoding='utf8') as infile:
                # store the <head> tag for later:
                head = get_head(infile, features=features)
            # open a source file to read the content and a destination file to save the output:
            with open(file) as infile, open(outfilename, 'w') as outfile:
                # store the <body> from the source file:
                soup = BeautifulSoup(infile, features=features)
                body = soup.find('body')
                # process the children: 
                for child in body.findChildren(recursive=False):
                    # flush genuine progressbar to console:
                    # bar.update()
                    # flush fake progressbar to console:
                    print('■', end='', flush=True)
                    if verbose:  # print to debug:
                        print_child_info(child)
                    # print selected children as is: 
                    if child.name in protected:
                        print(child, file=outfile)
                    # process tags that contain dictionary definitions (defined above):
                    elif child.name in tags and any(c in child['class'] for c in classes):
                        #print('DEBUG: child.name = ', child.name, '\n')
                        #print('DEBUG: child = ', child, '\n')
                        # convert tag????? to soup, feed to `make_entry()`, and print to file:
                        soup = BeautifulSoup(str(child), features=features)
                        #print('DEBUG: type(soup) = ', type(soup), '\n')
                        #print('DEBUG: soup = ', soup, '\n')
                        s = make_entry(soup, verbose=False)
                        #print('DEBUG: type(post_make_entry) = ', type(s), '\n')
                        # remove xml header, if one was inserted by parser:
                        if features == 'xml':
                            s = strip_header(s)
                        # add empty line for clarity:
                        s = s + '\n'
                        print(s, file=outfile)
                    else:
                        # remove all other children: 
                        child.extract(strip=True)
                        if verbose:  # print to debug:
                            print('\nThis child was removed:\n', child)
                            print('\nCheck that this is desired behaviour.\nYou may adjust the lists of `tags`, `classes`, and `protected`.')
                # exit the loop after all the children have been processed
            # insert the <body> of the output file into the <head> of the input file: Note the 'r+' argument
            with open(outfilename, 'r+') as outfile:
                # read the <body> of the processed file:
                body = outfile.read()
                # combine <body> with the <head> stored earlier:
                html = make_dml(body=body, head=head, features=features)
                # go to the top of the file:
                outfile.seek(0)
                # write to the file:
                outfile.write(html)
                # make sure content is completely overwritten: 
                outfile.truncate()
        # if something goes wrong, log the error:
        except Exception as e:
            errors.append(file)
            print('\n\nCRITICAL ERROR! \n\nPROBLEM WITH:\n\n', file, '\n\nAN ERROR WAS LOGGED\n\n')
            import logging
            logging.error("Exception occurred: %s", e)
            import traceback
            trace = traceback.format_exc()
            logging.error(trace)
    print('\n\nALL FILES PROCESSED: CHECK THE LOGS FOR ANY ERRORS.')
    if not errors:
        print('\nNO EXCEPTIONS WERE RECORDED!')
    else:
        print('\nThe following files raised an exception:', errors)
    return print('■')


def make_definition(soup:Tag, clean=False):
    """
    Extracts definition from dictionary entry.

    Args:
        soup (Tag): extracted portion of a word definition
    Returns:
        defn (str): word definition reformatted to conform to desired html styles
    Modules: bs4 (BeautifulSoup)
    Functions: `get_body()`
    """
    # if definition inside <blockquote>, remove it:
    f = soup.find_all('blockquote')
    if f:
        for b in f:
            b.unwrap()
    f = soup.find_all('p', attrs={'class':['ps','p','p1','pc','tc']})
    if f:
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
    # get the content inside the <body> tag:
    s = get_body(soup)
    # remove excess blank lines, if any:
    s = re.sub(r'\n+', '\n', s)
    if not s:
        s = 'Definition missing'
    defn = '<div>'+s+'</div>'
    return defn


def make_dml(body, head, features='lxml'):
    """
    Inserts a body within the head of dml file.

    Args:
        body (str): body of a dml page
        head (str): head of a dml page
    Returns:
        dml (str): dml page with head and body
    """
    n = body.count('<body>')
    # if there are multiple <body> tags, return an error!
    if n > 1:
        raise ValueError('More than one body tags found inside body!')
    # if the body element is not tagged by <body>, add it:
    if n == 0:
        body = '<body>' + body + '</body>'
    body = BeautifulSoup(body, features=features).find('body')
    dml = BeautifulSoup(head, features=features)
    dml.head.insert_after(body)
    dml = str(dml)
    return dml


# TO DO: UNDER CONSTRUCTION/REPAIR
def make_entry(soup:BeautifulSoup, strip_tags=(), strip_attrs=None, strip_classes=None, strip_chars=None, strip_comments=True, verbose=False):
    """
    Takes a well-formed block of dml and formats it to conform with the Kindle dictionary structure. 

    Args:
        soup (BeautifulSoup): complete dictionary entry
    Returns:
        entry (str): refactored dictionary entry
    Functions: 
        `strip_tags()`, `strip_attrs()`, `strip_classes()`, `strip_chars()`, `strip_comments()`, `split_entry()`, `make_label()`, `make_headword()`, `make_definition()`
    Notes:
        UNDER REPAIR
    TO DO: 
        add thorough test file, break up if possible.
    """
    # Emtpy or malformed definitions return None, in this case return the empty string:
    if not soup:
        return ''
    # trim dictionary entry:
    #strip_tags = list(strip_tags)
    #soup = strip_tags(soup, *strip_tags)
    #soup = strip_attrs(soup, args=strip_attrs)
    #soup = strip_classes(soup, args=strip_classes)
    #soup = strip_chars(soup, args=strip_chars)
    #if strip_comments:
    #    soup = strip_comments(soup)
    # Split dictionary entry into parts:
    s1, s2, s3 = split_entry(soup)
    if verbose:  # print to debug:
        print_type(s1, s2, s3)
    # Extract label value for dictionary entry:
    s1 = make_label(s1)
    # Extract first word for word header:
    s2 = make_headword(s2)
    # Extract the dictionary definition:
    s3 = make_definition(s3)
    # Concatenate label, word, definition, and tag group:
    entry = '<idx:entry scriptable="yes">' + '\n' + s1 + s2 + s3 + '\n' + '</idx:entry>'
    if verbose:  # print to debug:
        print_output(entry)
    return entry


def make_headword(soup:Tag):
    """
    Extracts short and long header from dictionary entry and tag appropriately. 

    Args:
        soup (Tag): dictionary entry
    Returns:
        word (str): word used as the header of the dictionary entry
    Modules: 
        bs4 (BeautifulSoup)
    Functions: 
        `get_headword()`
    """
    # split headword into short and long forms:
    short, long = get_headword(soup)
    # Now substitute the words into:
    s = """
    <div><span><b>short</b></span></div><span>long.</span>
    """
    s = s.replace('short', short, 1)
    s = s.replace('long', long, 1)
    headword = s.strip()
    return headword


def make_label(soup:Tag):
    """
    Extracts a label from dictionary entry. Uses first part of word definition.

    Args:
        soup (Tag): split dictionary entry
    Returns:
        label (str): label used to identify the dictionary entry
    Modules: 
        bs4 (BeautifulSoup)
    """
    # extract tag content:
    s = soup.get_text()
    label = ''.join(re.findall('[^\W\d_]', s))
    # Now substitute the label into:
    s = """
    <idx:orth value="label">
      <idx:infl>
        <idx:iform name="" value="label"/>
      </idx:infl>
    </idx:orth>
    """
    s = s.replace('label', label, 2)
    label = str(s).strip()
    return label


def print_children(soup:BeautifulSoup):
    """
    Print information about all children and descendents.

    Args: 
        soup (BeautifulSoup): dictionary entry
    """
    print('Number of children and descendants of main soup object:\n')
    print('No. children:   ', len(list(soup.children)))
    print('\nThe children are printed below:')
    print('\n', list(soup.children))
    print('\nNo. descendants:', len(list(soup.descendants)))
    print('\nThe descendants are printed below:')
    print('\n', list(soup.descendants))
    return print('\n')


def print_child_info(child):
    """
    Print information about each dictionary entry as a child of main soup.

    Args: 
        child (BeautifulSoup): child of dictionary entry
    """
    print('child.name =', child.name)
    print('child["class"]', child['class'])
    return print('\n')


def print_soup_info(soup, name=None):
    """
    Print information about a BeautifulSoup object for degugging purposes.

    Modules: bs4 (BeautifulSoup)
    """ 
    info = {'name': None, 'type': None, 'class': None, 'content': None, 'children': None}
    soup_name, soup_type, soup_class, soup_content, soup_children =  ([], ) * 5
    try:
        soup_name = soup.name
    except Exception:
        soup_name.append('NA')
    try:
        soup_type = type(soup)
    except Exception:
        soup_type.append('NA')
    try:
        soup_class = [i.text.strip() for i in soup.select('class')]
    except Exception:
        soup_class.append('NA')
    try:
        for si in soup.content:
            soup_content.append(si)
    except Exception:
        soup_content.append('NA')
    try:
        if soup.findChildren(recursive=False):
            soup_children = soup.findChildren(recursive=False)
    except Exception:
        soup_children.append('NA')
    # add information to dictionary:
    info.update({'name': soup_name, 'type': soup_type, 'content': soup_content, 'children': soup_children})
    # print to console:
    sep_line = '============================================================================='
    print('\n\n INFORMATION REQUESTED:\n', sep_line, '\n') 
    pprint.pprint(info, indent=0, width=80)
    print('\n', sep_line, '\n\n')
    # return the dictionary
    return info


def print_summary(docstring):
    """
    Prints a function's docstring.

    Args: 
        docstring (str): documentation
    """
    print('\n\nThe `verbose` flag was set to `True`\n')
    print('Summary of main function:\n')
    print(docstring)
    return print('\n')


def print_output(output:str):
    """
    Print output to screen surrounded by double lines (more visible, useful for debugging).

    Args: 
        output (str): any string
    """
    return print('\n\nOUTPUT PRINTOUT:\n================\n', output, '\n================\n\n')


def print_type(*args):
    """
    Print the type of the argument. 

    Args: 
        args (any type): tuple of any size
    Returns: 
        None
    """
    for idx, arg in enumerate(args, start=1):
        print('type of arg %s is %s' % (idx, type(arg)))
    return print('\n')


def replace_strings(text:str, *args:str, replace=''):
    """
    Replaces all occurrences of the second argument in the first argument with the third. 
    Default is to remove the given strings.
    
    Args: 
        text (str): string to replace from
        replace (str): string to use as replacement, defaults to string()
        *args (str): variable number of arguments
    Returns:
        text(str): string with given substrings(s) removed
    """
    for arg in args:
        text = text.replace(arg, replace)
    return text


def strip_arrows(text:str):
    """
    Remove arrows from text.

    Args:
        text (str): string containing arrows
    Returns: 
        text(str): argument with all arrows removed.
    Note: 
        Attempts two approaches found to work in different situtations.
    """
    # not worth checking for existence before attempting to replace:
    text = replace_strings(text, '->', '-&gt;', replace='')
    return text


def strip_attrs(soup:BeautifulSoup, *args:str):
    """
    Strip certain attributes from tags. 

    Args:
        soup (BeautifulSoup): A dictionary entry extracted from the GDLC azw dictionary
        args ([str]): A list of attributes to be stripped
    Returns:
        soup (BeautifulSoup): The dictionary entry with selected attributes removed
    """
    if not args:
        args = ['date', 'id']
    for arg in args:
        for tag in soup.find_all():
            if tag.has_attr(arg):
                del tag.attrs[arg]
    return soup


def strip_squares(soup:BeautifulSoup):
    """
    Remove special character '■' and associated tag from a dictionary definition. 

    Args:
        soup (BeautifulSoup): a dictionary definition processed as a BeautifulSoup object
    Returns:
        soup (BeautifulSoup): argument with all instances of <sup>■</sup> removed
    Modules: 
        bs4 (BeautifulSoup)
    """    
    for item in soup.find_all('sup'):
        if '■' in item.get_text():
            item.extract(strip=True)
            break
    return soup


def strip_chars(soup:BeautifulSoup, *args:str):
    """
    Strip given characters from a BeautifulSoup object. 

    Args:
        soup (BeautifulSoup): soup with unwanted characters
    Returns: 
        soup (BeautifulSoup): soup with given characters stripped
    Functions: 
        `strip_squares()`
    """ 
    if not args:
        args = ['squares']  # only option currently implemented (!)
    # delete selected characters from soup:
    if 'squares' in args:
        soup = strip_squares(soup)
    return soup


def strip_classes(soup:BeautifulSoup, *args:str):
    """
    Strip class from given tags in a BeautifulSoup object.

    Args:
        soup (BeautifulSoup): soup to clean
        args ([str]): A list of tags to be unclassed
    Returns:
        soup (BeautifulSoup)
    Modules: 
        bs4 (BeautifulSoup)
    """
    if not args:
        args = ['em', 'strong', 'sup']
    # delete classes associated with selected tags:
    for arg in args:
        for tag in soup.find_all(arg):
            if tag.has_attr('class'):
                del tag.attrs['class']
    return(soup)


def strip_spaces(item):
    """
    Strip excess white spaces from string or BeautifulSoup object.

    Args:
        item (str, BeautifulSoup, Tag, NavigableString)
    Returns:
        Wrapper around `strip_spaces_st()` and `strip_spaces_bs()`
    Modules: 
        bs4 (BeautifulSoup, Tag, NavigableString)
    """
    if isinstance(item, str):
        return strip_spaces_st(item)
    elif isinstance(item, (BeautifulSoup, Tag, NavigableString)):
        return strip_spaces_bs(item)
    else:  # here for debugging purposes
        raise ValueError('function strip_spaces() expects a string, a BeautifulSoup object or a Tag')


def strip_spaces_bs(soup):
    """
    Strip excess white spaces from a BeautifulSoup object.

    Args:
        soup (BeautifulSoup, Tag, NavigableString): any soup
    Returns:
        soup (BeautifulSoup, Tag, NavigableString): with excess white spaces stripped out
    Modules: 
        bs4 (BeautifulSoup), re
    """
    _multiple_spaces = re.compile(r'\s+')
    for item in soup.find_all():
        if item.string:
            item.string.replace_with(item.string.strip())
            if re.search(_multiple_spaces, item.string):
                item.string.replace_with(re.sub(_multiple_spaces,  ' ', item.string))
            if re.search(' .', item.string):
                item.string.replace_with(item.string.strip(' .')+'.')
    return soup


def strip_spaces_st(html):
    """
    Strip extra spaces from a string.

    Args:
        html (str): any string
    Returns:
        html (str): with white spaces stripped out
    Modules: 
        re
    Note:
        Leaves undesired spaces in some cases. 
    """
    html = re.sub('\s{2,}', ' ', html)
    return html


def strip_comments(soup:BeautifulSoup):
    """
    Strip comment from BeautifulSoup object.

    Args:
        soup (BeautifulSoup): any soup
    Returns:
        soup (BeautifulSoup): with comments stripped out
    Modules: 
        bs4 (BeautifulSoup, Comment)
    """
    f = soup.find_all(text=lambda text:isinstance(text, Comment))
    for fi in f:
        fi.extract(strip=True)
    #[fi.extract(strip=True) for fi in f]  # alternative, equivalent way
    return soup


def strip_empty_tags(soup:BeautifulSoup, strip_lines=False):
    """
    Remove empty tags from a BeautifulSoup object.
    If `strip_lines=True`, empty lines are also removed. 
    Argument `strip_lines` is passed down to `extract(strip=strip_lines)`
    
    Args: 
        soup (BeautifulSoup): html content with empty tags
    Returns: 
        soup (BeautifulSoup): original soup with empty tags removed
    Modules: 
        bs4 (BeautifulSoup)
    Functions: 
        `patched extract()` from module GDLC
    """
    for item in soup.find_all():
        if len(item.get_text(strip=True)) == 0:
            item.extract(strip=strip_lines)
    return soup


def strip_header(dml:str, header='<?xml version="1.0" encoding="utf-8"?>'):
    """
    Remove <xml> header using the re module to make case-insensitive replacement.

    Args: 
        xml (str): an xml page
        header (str): a header, defaults to standard <xml> header.
    Returns:
        xml (str): an xml page with xml header removed
    Modules: 
        re
    """
    esc = re.escape(header) 
    dml = re.sub(esc, '', dml, flags=re.IGNORECASE | re.MULTILINE).strip()
    return dml


def strip_tags(soup:BeautifulSoup, *args:str):
    """
    Strip certain tags (but not content) from a BeautifulSoup object. 
    
    Args: 
        soup (BeautifulSoup): A BeautifulSoup object with tags
        args ([str]): A list of tags to be stripped  
    Returns:
        soup (BeautifulSoup): soup without specified tags
    Modules: 
        bs4 (BeautifulSoup)
    """
    if not args:
        args = ['a', 'code']
    for arg in args:
        f = soup.find_all(arg)
        for fi in f:
            fi.unwrap()
    return soup


def split_entry(soup:BeautifulSoup):
    """
    Splits dictionary entry into three parts. 

    Args:
        soup (BeautifulSoup): A complete dictionary definition
    Returns:
        s1, s2, s3: A 3-tuple of BeautifulSoup objects.
    Modules: 
        bs4 (BeautifulSoup)
    Functions: 
        patched `extract()` from module GDLC
    """
    # slice soup into chunks:
    s1, s2, s3 = '', '', '' 
    # slice s1: word label for lookup
    f = soup.find_all('p', attrs={'class':'rf'})
    if f:
        for p in f:
            s1 = soup.p.extract(strip=True)
    # slice s2: word long and short forms 
    f = soup.find_all('p', attrs={'class':'df'})
    if f:
        for p in f:
            s2 = soup.p.extract(strip=True)
    # slice s3: word definition
    # p tags with classes rf and df were removed above
    # save the part enclosed in blockquotes
    s3 = soup.find('blockquote')
    return s1, s2, s3


def validate_entry(soup, verbose=False):
    """
    Removes invalid dictionary entries.

    Args:
        soup (BeautifulSoup): A dictionary entry extracted from the GDLC azw dictionary

    Returns:
        soup (BeautifulSoup): Only valid dictionary entries
    Modules: 
        bs4 (BeautifulSoup)
    Functions: 
        `print_children()`
    """
    if verbose:  # print to debug:
        print_children(soup)
    # delete entries missing class 'rf' and/or 'df'
    p = soup.find_all('p', attrs={'class':'rf', 'class':'df'})
    if p:
        soup.p.extract(strip=True)
        if verbose:  # print to debug:
            print('Warning: ', len(p), ' entries with missing classes "rf" or "df" were removed.')
            print('Warning: These entries are missing an essential class:\n', p)
    return soup

