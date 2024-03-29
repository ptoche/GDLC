#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GDLC - Gran Diccionari de la llengua catalana

Functions to edit the xhtml source code for the GDLC (Kindle edition). 

Gran Diccionari de la Llengua Catalana. Editor: Enciclopedia Catalana, SAU. ISBN: 978-8441227903. ASIN: B00DZWFUG4.

Written for the 'Gran Diccionari de la llengua catalana' published by Institut d'Estudis Catalans in 2013, purchased from Amazon for 6 euros and downloaded in the `mobi` format. 

After conversion to the azw format via the Calibre plugin KindleUnpack, the dictionary entries appear as well-formed blocks of document markup language code. written in the document markup language (GDLC source files are written in xhtml) 

The code loops through the blocks and formats them one at a time. The code may hopefully be adapted to other dictionaries, but almost certainly will not work without significant alterations. 

Usage:
    A dictionary entry may be converted to a lookup dictionary definition with:

        $ GDLC.make_entry(dml)

    make_entry() calls the following functions:
        split_entry()
            make_label()
            make_headword()
            make_definition()
    and concatenates label, headword, and definition into a dictionary entry.

    A dictionary page

    For examples of usage see inside `run.py`.
    The core code of module GDLC is in `GDLC.py`.
    Companion modules include:
        - test module. See `tests/tests.py` for details. 
        - logs module. Log files are saved in the `logs/logfiles` directory. See `logs/logs.py` for details. 
        - debug module. See `debug/debug.py` for details. 
        - query module. Sets up elements involving interaction with the user. See `query/query.py` for details. 
        - future module. Future developments and work in progress. See `future/future.py` for details.
    There is no proper documentation for this project. Limited information may be found in the `docs` directory and inside function docstrings. As the project evolves, some information may have become obsolete, beware. 

Args:
    verbose, clean, and features are common arguments of several functions. Their description is not repeated inside each function. 
    verbose (bool, optional): Set to True to print more information (useful for debugging).
    clean (bool, optional): Set to True to remove classes, ids, and other style-specific attributes: conforms more with the style of dictionary definitions seen in unpacked mobi files. Set to False to keep some of that information: conforms more with the style of dictionary definitions seen in unpacked azw files. 
    features (str, optional): Sets the parser to be used with BeautifulSoup. Defaults to 'lxml'. 

Returns:
    main_loop() reads the GDLC dictionary source files, edits them, and saves them into a format and directory structure that Amazon's KindleGen understands.
    make_entry() reads an entry from the GDLC dictionary text files and returns an entry conforming with the following template (with options to unclass tags):

    '''\
    ... <idx:entry name="Catalan" scriptable="yes" spell="yes">
    ...   <idx:orth value="ABC">
    ...     <idx:infl>
    ...       <idx:iform name="" value="ABC"/>
    ...       <idx:iform name="" value="ABC-"/>
    ...     </idx:infl>
    ...   </idx:orth>
    ...     <div>
    ...       <span>
    ...         <b>ABC</b>
    ...       </span>
    ...     </div>
    ...     <span>
    ...       <strong">ABC -xy</strong><sup>1</sup>.
    ...     </span>
    ...     <div>
    ...       <blockquote align="left" id="id0001"><span>Definition here.</span></blockquote>
    ...       </blockquote align="left><span>More details here.</span></blockquote>
    ...       <blockquote align="left"><span>More details and an <a class="calibre17" href="part1234.xhtml#id1234">anchor</a>.</span></blockquote>
    ...     </div>
    ... </idx:entry>\
    ...''' 

Created 3 May 2020

@author: patricktoche
"""
import sys
import os
from pathlib import Path, PosixPath
import io
import re
from shutil import copy2  # shutil.copy2 copies metadata+permissions

from bs4 import BeautifulSoup, Tag, NavigableString, Comment, PageElement, ProcessingInstruction
from typing import List, Set, Tuple, Dict, Iterable, Union, Any

from pprint import pprint
import progressbar  # !!  progressbar2 under the hood

import logging
import traceback


def copy_dirtree(indir, outdir, onerror=None) -> List[str]:
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


def dir_handler(dir=None, mkdir=False) -> Union[os.PathLike, str, bytes]:
    """
    Checks existence of a given directory and creates it upon request.

    Args:
        dir (str): path to directory
        mkdir (bool): if True, create the directory
    Returns:
        None
    Modules: 
        pathlib (Path)
    """
    if dir:
        dir = Path(dir).expanduser()
        # abort if the directory does not exist:
        if not dir.is_dir():
            # abort if no directory given and mkdir set to False:
            if not mkdir:
                return print('Aborting. No directory found at destination. The specified dir argument must be a valid directory. To create the directory, set `mkdir=True`.\n\nExample of usage: `copy_files(dir="~/tmp", mkdir=True)`')
            else:
                Path(dir).mkdir(parents=True)
    # if no directory is given, set up a default location:
    else:
        # get the user's home directory:
        home = Path.home()
        dir = home / 'tmp'
        if not mkdir:
            return print('Aborting. No directory given. To create a directory, set `mkdir=True`.')
        else:
            Path(dir).mkdir(parents=True)
    return dir


def copy_files(files=[], dir=None, source=None, mkdir=False) -> List[str]:
    """ 
    Copy files in given list to selected directory. 
    Destination directory will be created if it does not exist.

    Args:
        files ([str]): list of files to be copied
        dir (str): a destination directory
        source (str): a source directory may be given instead of a list of file paths
        mkdir (bool): if True, create the specified directory
    Modules: 
        shutil (copy2)
    Functions: 
        `template_copy()`, `dir_handler()`
    """
    # set or create a destination directory
    dir = dir_handler(dir, mkdir=mkdir)
    # if no files given, get the default list:
    if not files:
        if not source:
            home = Path.home()
            source = home / 'GDLC/source/GDLC_unpacked'
        files = template_copy(dir=source)
    # copy files to destination:
    print('\nGetting ready to copy files to destination directory.\n')
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


def template_copy(dir=None) -> List[str]:
    """
    Lists all files to be copied from source directory to destination.
    The file list is hard coded. Files may be added/removed as I understand file structure better.

    Usage:
        `template_copy(dir='~/GDLC/source/GDLC_unpacked')`
    Modules:
            pathlib (Path)
    Notes:
        The following directories remain empty: HDImages, mobi8/OEBPS/Fonts 
        An alternative is to copy the entire source directory!
    """
    # make sure the directory exists:
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


def destroy_tags(soup:BeautifulSoup, *args:str) -> BeautifulSoup:
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
# import PageElement if it has not been imported already
if 'PageElement' not in sys.modules:
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


def markup_handler(input, invalid_types=[], features='lxml') -> BeautifulSoup:
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


def get_content(soup:BeautifulSoup, tag: str=None): # -> dictionary
    """
    Make a dictionary of some relevant information stored in selected tags.

    Args:
        soup (BeautifulSoup): document markup language in BeautifulSoup format
        tag (str): tag of interest, e.g. tag='title'
    Returns:
        content ({str:str}): a dictionary of tags and meta content stored in opf file
    """
    # extract and store meta tags
    content = {}
    if not tag:
        print('Aborting. Argument tag must be given as a string, e.g. `tag="title"`.')
        return None
    tags = soup.find_all(tag)
    for item in tags:
        content.update({str(item.name): item.contents})
    return content


def get_doctype(dml, features='lxml'):
    """
    Wrapper for document markup language.

    Functions : 
        `markup_handler()`, `get_doctype_from_soup()`.
    """
    soup = markup_handler(dml, features=features)
    soup = get_doctype_from_soup(soup)
    return soup


def get_doctype_from_soup(soup:BeautifulSoup):
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
    # An obscure import, so keeping it inside the function
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


def get_meta_opf(dir, tags=[], encoding='utf8', features='lxml'):
    """
    Wrapper to read meta content of open package format (opf) file. 

    Args:
        dir(str, BeautifulSoup): directory to a dictionary written in document markup language
        tags ([str]): list of tags of interest, e.g. tags=['title', 'language']
        encoding (str): encoding used, default is 'utf8'
        features (str): parser used, default is 'lxml'
    Functions : 
        `dir_handler()`, `get_meta_opf_from_soup()`.
    Notes:
        content.opf lists the content of an epub/modi file, instructing KindleGen about the order in which the files are to be compiled.
    """ 
    # set up source directory:
    if not dir:
        home = Path.home()
        dir = home / 'GDLC/output/GDLC_processed'       
    dir = dir_handler(dir, mkdir=False)
    # read content from content.opf:
    file = dir / 'mobi8/OEBPS/content.opf'  # this part of tree is fixed
    if not file.exists():
        return print('Aborting. The following file was not found:\n\n', file)
    # list of meta tags of interest:
    if tags and not isinstance(tags, list):  # allow tags='list'
        tags = [tags]
    if not tags:
        tags = ['title', 'language', 'identifier', 'creator', 'publisher']
    # get attributes from the opf file:
    with open(file, encoding=encoding) as infile:
        soup = BeautifulSoup(infile, features=features)
        content = get_meta_opf_from_soup(soup, tags=tags)
    return content


def get_meta_opf_from_soup(soup:BeautifulSoup, tags=[]):
    """
    Make a dictionary of some relevant information stored in content.opf file.

    Args:
        soup(BeautifulSoup): document markup language in BeautifulSoup format
        tags ([str]): list of tags of interest, e.g. tags=['title', 'language']
    Returns:
        content ({str:str}): a dictionary of tags and meta content stored in opf file
    """
    # extract and store meta tags
    content = {}
    if tags:
        for tag in tags:
            meta = 'dc:'+tag
            for item in soup.find_all(meta):
                content.update({tag: item.contents[0]})
    return content


def get_pi(dml, features='lxml'):
    """
    Wrapper for document markup language.

    Functions : 
        `markup_handler()`, `get_pi_from_soup()`.
    """
    soup = markup_handler(dml, invalid_types=[Tag, NavigableString], features=features)
    if not soup:
        return None
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
    """
    if 'PageElement' not in sys.modules:
        from bs4 import ProcessingInstruction
    items = [item for item in soup if isinstance(item, ProcessingInstruction)]
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
    Sorts unique and duplicated IDs in a document markup language document.

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


def insert_frameset(soup: BeautifulSoup) -> None:
    """Insert an <mbp:frameset> tag."""
    new_tag = soup.new_tag('mbp:frameset')
    b = soup.find('body')
    b.wrap(new_tag)
    return None


def insert_pagebreak(soup: BeautifulSoup, tag: Tag) -> None:
    """Insert an <mbp:pagebreak> tag."""
    soup = BeautifulSoup(str(soup), features = 'xml')
    tag.insert(0, soup.new_tag('mbp:pagebreak'))
    return None


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


def list_invalid_tags(soup:BeautifulSoup, valid=[]):
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


def make_dictionary(dml, tags=[], protected=[], classes=[], clean=False, features='lxml', progress=True, verbose=False):
    """
    Process several dictionary definitions from a document markup language.

    Args:
        dml (Tag): BeautifulSoup Tag
        protected ([str]): protected tags are returned untouched
    Returns:
        dic ({str}): a dictionary of definitions
    Modules:
        progressbar
    Functions:
        `version_check()`, `debug.print_child_info()`, `make_entry`, `strip_header()`
    """ 
    # definitions will be stored in an order-preserving dictionary:
    version_check()  # abort if Python < 3.6
    # dictionary values will be joined at the end:
    dic = {}
    children = dml.findChildren(recursive=False)
    n = len(children)+1
    if verbose:  # print to debug:
        from GDLC.debug.debug import print_dictionary_info
        print_dictionary_info(n)
    # initialize a counter:
    i = 0
    if progress:
        widgets = [progressbar.Percentage(), progressbar.Bar(marker='■')]
        bar = progressbar.ProgressBar(widgets=widgets, max_value=n).start()
    for child in children:
        # update a counter and progressbar:
        i += 1
        if progress:
            bar.update(i+1)
        # flush fake progressbar to console:
        # print('■', end='', flush=True)
        if verbose:  # print to debug:
            from GDLC.debug.debug import print_child_info
            print_child_info(child)
        # print protected tags as is: 
        if child.name in protected:
            dic.update({str(i): str(child)})
        # process tags that contain dictionary definitions (defined above):
        elif child.name in tags and any(c in child['class'] for c in classes):
            soup = BeautifulSoup(str(child), features=features)
            entry = make_entry(soup)
            # remove <xml> header, in case one was inserted by parser:
            entry = strip_header(entry)
            # add empty line for clarity:
            entry = entry + '\n'
            dic.update({str(i): entry})
        else:
            # remove all other children: 
            child.extract(strip=True)
            if verbose:  # print to debug:
                from GDLC.debug.debug import print_child_extract
                print_child_extract(child)
    if progress:
        bar.finish()
    return dic


def main_loop(files, dir=None, tags=[], protected=[], classes=[], clean=False, features='lxml', progress=True, query=True, verbose=False):
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
        os, pathlib (Path), bs4 (BeautifulSoup), GDLC (query)
    Functions: 
        `main_loop_query()`, `get_head_from_soup()`, `make_dictionary()`, `debug.print_log_error()`
    TO DO: 
        use **kwargs
    """ 
    # set up output directory and ask user to validate.
    dir = main_loop_query(dir, query)
    if not dir:  # at this point, user declined to proceed
        return None
    # set up a container to hold a list of files that raise an error:
    errors = []
    # set up tags to be processed / tags that are protected:
    entry_tag_default = ['blockquote']
    entry_class_default = ['calibre27']
    protected_default = ['h1', 'h2', 'h3', 'h4', 'h5', '\n']
    # ignore defaults if set by user
    if not tags:
        tags = entry_tag_default
    if not classes:
        classes = entry_class_default
    if not protected:
        protected = protected_default
    # start the main loop:
    for file in files:
        filepath = Path(file)
        # set up the full path to the output file:
        outfilename = dir.joinpath(filepath.name)
        # try to read input files and write to output files:
        try:
            print('\n\nPROCESSING FILE', file, ':\n')
            # open a source file to read the content and a destination file to save the output:
            with open(file, encoding='utf8') as infile, open(outfilename, 'w') as outfile:
                # convert document markup language to BeautifulSoup object:
                soup = BeautifulSoup(infile, features=features)
                # insert a <mbp:frameset> tag:
                insert_frameset(soup)
                # process the body to return formatted dictionary entries:
                body = soup.find('body')  # returns a BeautifulSoup Tag
                dico = make_dictionary(body, tags=tags, protected=protected, classes=classes, features=features, progress=progress, verbose=verbose)
                body = '\n'.join(dico.values())
                # create a dml page with <html> and <head> tags:
                body = BeautifulSoup(body, features=features)
                page = make_dml_from_soup(body, features=features)
                # write to the file:
                print(page, file=outfile)
        # if something goes wrong, log the error:
        except Exception as error:
            if verbose:
                from GDLC.debug.debug import print_log_error
                print_log_error(item=file, error=error, record=errors)
            else:
                print(str(error))
    print('\n\nALL FILES PROCESSED: CHECK THE LOGS FOR ANY ERRORS.')
    if not errors:
        print('\nNO EXCEPTIONS WERE RECORDED!')
    else:
        print('\nThe following files raised an exception:', errors)
    return print('■')


def main_loop_query(dir, query=True):
    """
    Print warning and request user confirmation before proceeding.

    Args:
        dir (str): path to destination directory.
        query (bool): always answer 'yes' if False
    Returns: stop/continue
    Modules: 
        pathlib (Path), query (query_yes_no)
    """
    if dir:
        print('\nYour output files will be saved in ', dir, '\n')
    # ask user to validate long job and overwrite files:
    if query:
        # do not add to namespace if no query:
        from GDLC.query.query import query_yes_no
        validate = query_yes_no('\nWARNING!\n\nYou are about to start processing multiple dictionary files.\n\nFor a typical dictionary, this could take a few minutes.\n\nExisting files will be overwritten!\n\nDo you want to proceed?\n')
        if validate in ['no']:
            print('\nLoop aborted by user!')
            return None
    if not dir:
        dir = Path(__file__).resolve().parent.parent.joinpath('tmp')
        print('\nWARNING!\n\nAs no directory was given, files will be saved in the default location:\n\n', dir, '\n')
        print('Set `dir` in function `main_loop()` to save to another directory.\n')
        # ask user to validate the directory:
        if query:
            validate = query_yes_no('\nDo you want to proceed?\n')
            if validate in ['no']:
                print('\nLoop aborted by user!')
                return None
        Path(dir).mkdir(parents=True, exist_ok=True)
    return dir


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


def make_dml(soup: BeautifulSoup, features='lxml'):
    """Wrapper for `make_dml_from_soup()`"""
    return make_dml_from_soup(soup, features=features)


def make_dml_from_soup(soup: BeautifulSoup, features='lxml'):
    """
    Builds a document markup language page from string components.

    Args:
        soup (BeautifulSoup): body of dml page
    Returns:
        dml (str): dml page with body, head, and root tags
    """
    # convert <head> into BeautifulSoup Tag:
    head = BeautifulSoup(template_head(), features=features).find('head')
    # insert the <body> after the <head>
    soup.find('body').insert_before(head)
    # populate the <html> attributes:
    soup = template_html_insert(soup.find('html'))
    # convert element tag to soup object to insert <xlm> declaration:
    soup = BeautifulSoup(str(soup), features=features)
    # convert <xml> into BeautifulSoup object:
    xml = BeautifulSoup(template_xml(), features=features)
    # insert the <xml> tag at the top of the page:
    soup.insert(0, xml)
    # return page as a string:
    dml = str(soup)
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
        add thorough test file
        work out what to put into id
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
        from GDLC.debug.debug import print_type
        print_type(s1, s2, s3)
    # Extract label value for dictionary entry:
    s1 = make_label(s1)
    # Extract first word for word header:
    s2 = make_headword(s2)
    # Extract the dictionary definition:
    s3 = make_definition(s3)
    # Concatenate label, word, definition, and tag group:
    entry = make_entry_idx() + '\n' + s1 + s2 + s3 + '\n' + '</idx:entry>'
    if verbose:  # print to debug:
        from GDLC.debug.debug import print_output
        print_output(entry)
    return entry


def make_entry_idx(name='Catalan', scriptable='yes', spell='yes'):
    """
    Pass values for name, scriptable, spell attributes to the idx entry tag.
    Args:
        name (str), scriptable (str), spell (str): <idx:entry> attributes
    Returns:
        <idx:entry> tag with attributes.
    Notes:
        A sequential 'id' attribute will be added separately to <idx:entry>.
    """
    attrs = [name, scriptable, spell]
    entry = '<idx:entry name="{0}" scriptable="{1}" spell="{2}">'.format(*attrs)
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


def strip_anchor(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Loop through every anchor and strip it, without editing content. 

    Args:
        soup (BeautifulSoup): A BeautifulSoup object
    Returns:
        Wrapper around `strip_anchor_href()` and `strip_anchor_id()`
    Modules: 
        bs4 (BeautifulSoup), re (compile)
    """
    # For each anchor found in "id", search the anchor in "href":
    for tag_id in soup.find_all(attrs={'id':True}):
        id = str(tag_id['id'])
        for tag_a in soup.find_all('a', href=re.compile(id)):
            tag_a.unwrap()
        del tag_id['id']
    return soup


def strip_anchor_from_href(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Loop through every href anchor and strip it, without editing content.

    Strip <a> tags such as
        <a class="calibre17" href="part0017.xhtml#d00401">absolutisme</a>
    Args:
        soup (BeautifulSoup): A BeautifulSoup object
    """
    tags = soup.find_all('a')
    for tag in tags:
        tag.unwrap()
    return soup


def strip_anchor_from_id(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Loop through every id anchor and strip it, without editing content.

    Strip <id> attributes such as
        <h2 class="centrat2" id="aid-F8901">A</h2>
    Args:
        soup (BeautifulSoup): A BeautifulSoup object
    """
    for tag in soup.find_all(attrs={'id':True}):
        del tag['id']
    return soup


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


def strip_spaces(item):
    """
    Strip excess white spaces from string or BeautifulSoup object.

    Args:
        item (str, BeautifulSoup, Tag, NavigableString)
    Returns:
        Wrapper around `strip_spaces_from_string()` and `strip_spaces_from_soup()`
    Modules: 
        bs4 (BeautifulSoup, Tag, NavigableString)
    """
    if isinstance(item, str):
        return strip_spaces_from_string(item)
    elif isinstance(item, (BeautifulSoup, Tag, NavigableString)):
        return strip_spaces_from_soup(item)
    else:  # here for debugging purposes
        raise ValueError('function strip_spaces() expects a string, a BeautifulSoup object or a Tag')


def strip_spaces_from_soup(soup:BeautifulSoup):
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


def strip_spaces_from_string(html):
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


def template_head() -> str:
    """Returns the default GDLC <head> tag and attributes."""
    return '''\
<title>Gran Diccionari de la llengua catalana</title> 
<meta content="text/html; charset=utf-8" http-equiv="Content-Type"/> 
<link href="../Styles/style0001.css" rel="stylesheet" type="text/css"/> 
<link href="../Styles/style0002.css" rel="stylesheet" type="text/css"/>'''


def template_html() -> str:
    """Returns the default Amazon Kindle dictionary <root> tag"""
    return '''\
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
xmlns:idx="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"> \
</html>'''


def template_html_insert(tag: Tag) -> Tag:
    """Inserts the default Amazon Kindle dictionary attributes to existing <html> tag."""
    tag.attrs.clear()  # clear existing attributes, if any
    tag['xmlns:math'] = 'http://exslt.org/math'
    tag['xmlns:svg'] = 'http://www.w3.org/2000/svg'
    tag['xmlns:tl'] = 'https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf'
    tag['xmlns:saxon'] = 'http://saxon.sf.net/'
    tag['xmlns:xs'] = 'http://www.w3.org/2001/XMLSchema'
    tag['xmlns:xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
    tag['xmlns:cx'] = 'https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf'
    tag['xmlns:dc'] = 'http://purl.org/dc/elements/1.1/'
    tag['xmlns:mbp'] = 'https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf'
    tag['xmlns:mmc'] = 'https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf'
    tag['xmlns:idx'] = 'https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf'
    return tag


def template_xml() -> str:
    """Returns an <xml> tag with attributes"""
    return '<?xml version="1.0" encoding="UTF-8"?>'


def validate_entry(soup:BeautifulSoup, verbose=False):
    """
    Removes invalid dictionary entries.

    Args:
        soup (BeautifulSoup): A dictionary entry extracted from the GDLC azw dictionary

    Returns:
        soup (BeautifulSoup): Only valid dictionary entries
    Modules: 
        bs4 (BeautifulSoup)
    Functions: 
        `debug.print_children()`
    """
    if verbose:  # print to debug:
        from GDLC.debug.debug import print_children
        print_children(soup)
    # delete entries missing class 'rf' and/or 'df'
    p = soup.find_all('p', attrs={'class':'rf', 'class':'df'})
    if p:
        soup.p.extract(strip=True)
        if verbose:  # print to debug:
            from GDLC.debug.debug import print_warn_missing
            print_warn_missing(p)
    return soup


def version_check(raise_exception=True):
    """
    Checks Python version and raises exception if incompatibility detected.
    """
    if not sys.version_info >= (3, 6):
        if raise_exception:
            raise Exception('Aborting. This implementation of GDLC relies on the built-in ordering of ordinary dictionaries introduced in Python 3.6. In earlier versions of Python, dictionaries did not preserve order of insertion. For earlier versions of Python, an `OrderedDict` should be used instead. Changes to the code are required in `make_dictionary()`. Set `raise_exception=False` to proceed anyway.')
    return None
