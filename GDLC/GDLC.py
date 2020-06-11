#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GDLC basic information

Functions to edit the xhtml source code for the GDLC (Kindle edition).

Written for the 'Gran diccionari de la llengua catalana' published by Institut d'Estudis Catalans in 2013, purchased from Amazon for 6 euros and downloaded in the `mobi` format. 

After conversion to the `azw` format via the `Calibre` plugin `KindleUnpack`, the dictionary entries appear as well-formed blocks of html code inside `blockquote` tags. 

The code loops through the blocks and formats them one at a time. The code may hopefully be adapted to other dictionaries, but almost certainly will not work without alterations. 

Example:
    A dictionary entry may be converted to a lookup dictionary definition with

        $ GDLC.make_entry(html_string)

    make_entry() calls the following functions:
        split_entry()
            make_label()
            make_headword()
            make_definition()
    and concatenates label, headword, and definition.

    For examples of usage see inside `run.py`.
    The core code of module GDLC is in `GDLC.py`.
    A test suite for the module is in the `tests` directory. See `tests/tests.py` for details. 
    Log files are saved in the `logs` directory.  See `logs/logs.py` for details. 
    Elements involving interaction with the user are in the `queries` directory. See `queries/query.py` for details. 
    Future developments and work in progress are in the `future` directory. See `future/future.py` for details.
    There is no documentation for this project. Limited info may be found in the `docs` directory. 

Args:
    verbose, clean, and features are common arguments of several functions. Their description is not repeated inside each function. 
    verbose (bool, optional): Set to True to print more information (useful for debugging).
    clean (bool, optional): Set to True to remove classes, ids, and other style-specific attributes: conforms more with the style of dictionary definitions seen in unpacked mobi files. Set to False to keep some of that information: conforms more with the style of dictionary definitions seen in unpacked azw files. 
    features (str, optional): Sets the parser to be used with BeautifulSoup. Defaults to 'lxml'. 

Created 3 May 2020

@author: patricktoche
"""
import os
import pathlib
import re

import bs4
from bs4 import BeautifulSoup, Tag, NavigableString, Comment

import pprint
import progressbar  # !!  progressbar2 under the hood



def default_head():
    return '''<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head>'''



def destroy_tags(soup:BeautifulSoup, *args:str):
    '''
    Remove tagged content for tags that the kindle does not support.

    Args: 
        soup (BeautifulSoup): html content with unsupported tags
        args (str): name of the tags to be destroyed
        usage: destroy_tag(soup, 'code', 'script')

    Returns: 
        soup (BeautifulSoup): original soup with selected tags destroyed
    
    Modules: bs4 (BeautifulSoup)
    '''
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
    """Destructively rips this element out of the tree.

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



def get_body(html, features='lxml'):
    """
    Extract the body from an xml file. 

    Args:
        html (str, BeautifulSoup, Tag): html page with head and body
    
    Returns:
        body (str): body of the html page
    
    Modules: bs4 (BeautifulSoup), re
    """
    # all BeautifulSoup objects are also Tag objects, but not the converse, so check Beautifulsoup first
    if isinstance(html, BeautifulSoup):
        soup = html
    elif isinstance(html, Tag):
        soup = BeautifulSoup(str(html), features=features)
    else:
        try:
            soup = BeautifulSoup(html, features=features)
        except:  # here for debugging purposes
            raise ValueError('function `get_body()` expects a string or a BeautifulSoup object')
    body = soup.find('body')
    body = ''.join(['%s' % x for x in body])
    body = re.sub(r'\n+', '\n', body).strip()  # .strip() removes leading/trailing blankspaces/newlines
    return body



def get_doctype(soup):
    '''
    Extracts doctype from a page. Must import the entire bs4 module.
    '''
    items = [item for item in soup.contents if isinstance(item, bs4.Doctype)]
    return items[0] if items else None



def get_head(file, features='lxml'):
    """
    Read an xhtml/xml/html file and extracts the head tag.

    Args: 
        file (str, BeautifulSoup, Tag): path to file or actual content
    Returns: 
        head (str)
    """
    # if no argument, return a default value:
    if not file:
        print('A path/to/file was not supplied. A default <head> string is returned.')
        return default_head()
    # if argument has a <head> tag, treat it as markup code:
    elif isinstance(file, str) and file.find('<head'):
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
    # get the head:
    head = soup.find('head')
    # convert to string:
    head = str(head).strip()
    return head



def get_headword(tag):
    """
    Extract the content of a BeautifulSoup object of type Tag

    Args:
        tag (Tag): a BeautifulSoup tag, obtained by extracting from a soup

    Returns:
        short, long ([str]): short and long form of a word in dictionary definition
    
    Modules: bs4 (BeautifulSoup)
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



def get_root(soup):
    '''
    Extracts root from a page. Must import the entire bs4 module.
    '''
    items = [item for item in soup if isinstance(item, bs4.element.ProcessingInstruction)]
    return items[0] if items else None



def list_files_all(dir):
    """ 
    List files in the given directory.

    Args:
        dir (str): path to a directory

    Returns:
        lst ([str]): list of filenames in directory
    
    Modules: os
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

    Modules: os, re
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
    
    Modules: os
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



def make_entry(soup:BeautifulSoup, strip_tags=(), strip_attrs=None, strip_classes=None, strip_chars=None, strip_comments=True, verbose=False):
    """
    Takes a well-formed block of html code and formats it to conform with the Kindle dictionary structure. 

    Args:
        soup (BeautifulSoup): complete dictionary entry

    Returns:
        s (str): refactored dictionary entry
    
    Functions: strip_tags(), strip_attrs(), strip_classes(), strip_chars(), strip_comments(), split_entry(), make_label(), make_headword(), make_definition()
    """
    # Emtpy or malformed definitions return None, in this case return the empty string:
    if not soup:
        return ''
    # trim dictionary entry:
    # STOPPED HERE 
    # TO DO: Check make_entry(), make_label(), make_headword()
    # TO DO: Pass a list to the vararg function
    #strip_tags = ()
    #strip_tags = list(strip_tags)
    #soup = strip_tags(soup, *strip_tags)
#    soup = strip_attrs(soup, args=strip_attrs)
#    soup = strip_classes(soup, args=strip_classes)
#    soup = strip_chars(soup, args=strip_chars)
#    if strip_comments:
#        soup = strip_comments(soup)
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
    s = '<idx:entry scriptable="yes">' + '\n' + s1 + s2 + s3 + '\n' + '</idx:entry>'
    if verbose:  # print to debug:
        print_output(s)
    return s



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
    
    Modules: os, pathlib (Path), bs4 (BeautifulSoup), GDLC (queries)

    Functions: query_yes_no(), get_head(), make_entry(), make_html()
    
    Debugging: print_child_info()
    """ 
    # ask user to validate a job that can take a while and overwrite files:
    from GDLC.queries.query import query_yes_no
    validate = query_yes_no('You are about to start processing multiple dictionary files, potentially overwriting existing files. Do you want to proceed?')
    if validate in ['no']:
        return print('Loop aborted by user!')
    else:
        print('\nOutput files will be saved in the following directory:\n\n', dir, '\n\nSet `dir` in function `main_loop` to change the default directory.\n\nWARNING: Destination files will be overwritten.\n\n')
    
    # set up a progress bar for long jobs:
    widgets = [progressbar.Percentage(), progressbar.Bar()]
    bar = progressbar.ProgressBar(widgets=widgets, max_value=10).start()

    # set up output directory. If default directory `tmp` does not exist, create it:
    if not dir:
        dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'tmp'))
        from pathlib import Path
        Path('tmp').mkdir(parents=True, exist_ok=True)
    else:
        print('Your output files will be saved in ', dir, '\nMake sure an empty directory exists at the location!')
    
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
                    if progress:
                        # flush genuine progressbar to console:
                        bar.update() 
                    else:
                        # flush fake progressbar to console:
                        print('■', end='', flush=True)
                    if verbose:  # print to debug:
                        print_child_info(child)
                    # print selected children as is: 
                    if child.name in protected:
                        print(child, file=outfile)
                    # process tags that contain dictionary definitions (defined above):
                    elif child.name in tags and any(c in child['class'] for c in classes):
                        print('DEBUG: child.name = ', child.name, '\n')
                        print('DEBUG: child = ', child, '\n')
                        # convert tag????? to soup, feed to `make_entry()`, and print to file:
                        soup = BeautifulSoup(str(child), features=features)
                        print('DEBUG: type(soup) = ', type(soup), '\n')
                        print('DEBUG: soup = ', soup, '\n')
                        s = make_entry(soup, verbose=verbose, clean=clean)
                        print('DEBUG: type(post_make_entry) = ', type(s), '\n')
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
                html = make_html(body=body, head=head, features=features)
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
    return None



def make_definition(soup:Tag, clean=False):
    """
    Extracts definition from dictionary entry.

    Args:
        soup (Tag): extracted portion of a word definition

    Returns:
        defn (str): word definition reformatted to conform to desired html styles
    
    Modules: bs4 (BeautifulSoup)

    Functions: get_body()
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



def make_headword(soup:Tag):
    """
    Extracts short and long header from dictionary entry and tag appropriately. 

    Args:
        soup (Tag): dictionary entry

    Returns:
        word (str): word used as the header of the dictionary entry

    Modules: bs4 (BeautifulSoup)

    Functions: get_headword()
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



def make_html(body, head, features='lxml'):
    """
    Inserts a body within the head in html/xml file.

    Args:
        body (str): body of an html page
        head (str): head of an html page

    Returns:
        html (str): html page with head and body
    """
    n = body.count('<body>')
    # if there are multiple <body> tags, return an error!
    if n > 1:
        raise ValueError('More than one body tags found inside body!')
    # if the body element is not tagged by <body>, add it:
    if n == 0:
        body = '<body>' + body + '</body>'
    body = BeautifulSoup(body, features=features).find('body')
    html = BeautifulSoup(head, features=features)
    html.head.insert_after(body)
    html = str(html)
    return html



def make_label(soup:Tag):
    """
    Extracts a label from dictionary entry. Uses first part of word definition.

    Args:
        soup (Tag): split dictionary entry

    Returns:
        label (str): label used to identify the dictionary entry

    Modules: bs4 (BeautifulSoup)
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

    Returns: 
        None
    """
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

    Args: 
        child (BeautifulSoup): child of dictionary entry

    Returns: 
        None
    """
    print('child.name =', child.name)
    print('child["class"]', child['class'])
    return None



def print_function_name():
    """
    Return the name of the caller (function or method). 
    
    Modules: sys (_getframe)
    """
    return sys._getframe().f_code.co_name



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

    Returns: 
        None
    """
    print('\n\nThe `verbose` flag was set to `True`\n')
    print('Summary of main function:\n')
    print(docstring, '\n')
    return None



def print_output(output:str):
    """
    Print output to screen surrounded by double lines (more visible, useful for debugging).

    Args: 
        output (str): any string

    Returns: 
        None
    """
    print('\n\nOUTPUT PRINTOUT:\n================\n', output, '\n================\n\n')
    return None



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
    return None



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
    
    Note: Two methods that apply in different cases.
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
    
    Modules: bs4 (BeautifulSoup)
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
    
    Functions: strip_squares()
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
    
    Modules: bs4 (BeautifulSoup)
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
    
    Modules: bs4 (BeautifulSoup, Tag, NavigableString)
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
    
    Modules: bs4 (BeautifulSoup), re
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
    
    Modules: re

    Note:
        Leaves undesired spaces in some cases. 
    """
    html = re.sub('\s{2,}', ' ', html)
    return html



def strip_comments(soup:BeautifulSoup):
    """
    Strip comment from BeautifulSoup object

    Args:
        soup (BeautifulSoup): any soup
    
    Returns:
        soup (BeautifulSoup): with comments stripped out

    Modules: bs4 (BeautifulSoup, Comment)
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

    Modules: bs4 (BeautifulSoup)

    Functions: patched extract() from module GDLC
    """
    for item in soup.find_all():
        if len(item.get_text(strip=True)) == 0:
            item.extract(strip=strip_lines)
    return soup



def strip_header(xml:str, header='<?xml version="1.0" encoding="utf-8"?>'):
    """
    Remove unwanted header introduced when using the `xml` parser
    using the re module to make case-insensitive replacement.

    Args: 
        xml (str): an xml page
        
    Returns:
        xml (str): an xml page with xml header removed
    
    Modules: re
    """
    esc = re.escape(header) 
    xml = re.sub(esc, '', xml, flags=re.IGNORECASE | re.MULTILINE).strip()
    return xml



def strip_tags(soup:BeautifulSoup, *args:str):
    """
    Strip certain tags (but not content) from a BeautifulSoup object. 
    
    Args: 
        soup (BeautifulSoup): A BeautifulSoup object with tags
        args ([str]): A list of tags to be stripped
        
    Returns:
        soup (BeautifulSoup): soup without specified tags
    
    Modules: bs4 (BeautifulSoup)
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
    
    Modules: bs4 (BeautifulSoup)

    Functions: patched extract() from module GDLC
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
    
    Modules: bs4 (BeautifulSoup)

    Functions: print_children()
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

