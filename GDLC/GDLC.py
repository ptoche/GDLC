#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GDLC basic information

Functions to edit the xhtml source code for the GDLC (Kindle edition).

Written for the 'Gran diccionari de la llengua catalana' published by Institut d'Estudis Catalans in 2013, purchased from Amazon for 6 euros and downloaded in the `mobi` format. 

After conversion to the `azw` format via the `Calibre` plugin `KindleUnpack`, the dictionary entries appear as well-formed blocks of html code inside `blockquote` tags. 

The code loops through the blocks and formats them one at a time. The code may hopefully be adapted to other dictionaries, but almost certainly will not work without alterations. 

Example:
    A word definition may be converted to a lookup dictionary definition with

        $ GDLC.dictionarize(html_string)

    For more examples, see inside `run.py`

Args:
    verbose, clean, and features are common arguments of several functions. Their description is not repeated inside each function. 
    verbose (bool, optional): Set to True to print more information (useful for debugging).
    clean (bool, optional): Set to True to remove classes, ids, and other style-specific attributes: conforms more with the style of dictionary definitions seen in unpacked mobi files. Set to False to keep some of that information: conforms more with the style of dictionary definitions seen in unpacked azw files. 
    features (str, optional): Sets the parser to be used with BeautifulSoup. Defaults to 'lxml'. Other 

To Do:
    * Check code for parsers other than lxml
    * Check if all definitions are in blockquote with class calibre27
    * Check case of missing or malformed tags, e.g. with missing word or line-ending slash
    * Test find_all instead of findChildren
    * Make the following functions:
    * get_word_class(): verb, noun, etc.
    * get_word_inflection(): tall, taller, tallest
    * get_word_pronunciation(): International Phonetic Alphabet 
    * get_word_tag(): whether words are tagged with ■ or something else

Created 3 May 2020

@author: patricktoche
"""
import os
import re
import pprint

from bs4 import BeautifulSoup, Tag
from bs4 import NavigableString, Comment


def clean_tags(soup):
    """
    Remove certain tags: '<a', 'id', 'class' from BeautifulSoup object.

    Args:
        soup (bs4.BeautifulSoup): soup to clean

    Returns:
        soup (bs4.BeautifulSoup)
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



def dictionarize(item, verbose=False, clean=False, features='lxml'):
    """
    Takes a well-formed block of html code and formats it to conform with the Kindle dictionary structure. 

    Args:
        item (str): word definition in html format

    Returns:
        s (str)
    """
    # Trim & Clean dictionary entry:
    soup = trim_entry(item, verbose=verbose, clean=clean, features=features)
    # Emtpy or malformed definitions return None, return empty string if None
    if not soup:
        return ''
    # Split dictionary entry into parts:
    s1, s2, s3 = split_entry(soup, verbose=verbose, clean=clean, features=features)
    if verbose:
        print_type(s1, s2, s3)
    # Extract label value for dictionary entry: 
    s1 = make_label(s1)
    # Extract first word for word header: 
    s2 = make_headword(s2)
    # Extract the dictionary definition:
    s3 = make_definition(s3, verbose=verbose, clean=clean)
    # Concatenate label, word, definition, and tag group:
    s = '<idx:entry scriptable="yes">' + '\n' + s1 + s2 + s3 + '\n' + '</idx:entry>'
    if features == 'xml':
        s = strip_header(s)
    if verbose:
        print_output(s)
    return s



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
        html (str, bs4.BeautifulSoup, bs4.element.Tag): html page with head and body
    
    Returns:
        body (str): body of the html page
    """
    # all BeautifulSoup objects are also Tag objects, but not the converse, so check Beautifulsoup first
    # if isinstance(html, Tag): intended to work even if body tag has class or id.
    if isinstance(html, str):
        soup = BeautifulSoup(html, features=features)
    elif isinstance(html, BeautifulSoup):
        soup = html
    elif isinstance(html, Tag):
        soup = BeautifulSoup(str(html), features=features)
    else:  # here for debugging purposes
        raise ValueError('function get_body() expects a string, BeautifulSoup object or tag')
    body = soup.find('body')
    body = ''.join(['%s' % x for x in body])
    body = re.sub(r'\n+', '\n', body).strip()  # .strip() removes leading/trailing blankspaces/newlines
    return body



def get_head(html, features='lxml'):
    """
    Extract the head from an xml file. 

    Args:
        html (str, bs4.BeautifulSoup, bs4.element.Tag): html page with head and body

    Returns:
        head (str): head of the html page
    """
    if isinstance(html, str):
        soup = BeautifulSoup(html, features=features)
    elif isinstance(html, (BeautifulSoup, Tag)):
        soup = html
    else:  # here for debugging purposes
        raise ValueError('function get_head() expects a string, BeautifulSoup object or tag')
    body = soup.find('body')
    body.decompose()
    head = str(soup).strip()
    return head



def get_headword(tag):
    """
    Extract the content of a BeautifulSoup object of type bs4.element.Tag

    Args:
        tag (bs4.element.Tag): a BeautifulSoup tag, obtained by extracting from a soup

    Returns:
        y0, y1 ([str]): short and long form of a word in dictionary definition
    """
    if not isinstance(tag, Tag):
        print('get_headword() only accepts objects of type `Tag`')
    # suppress superscripts:
    for sup in tag.find_all('sup'):
        sup.decompose()
    # extract headword(s):
    y0 = tag.get_text()
    # extract first part without tags:
    y0 = y0.split(' ', 1)[0]
    # extract whole headword string without tags:
    y1 = ''
    for child in tag.children:
        y1 += str(child)
    # keep only content inside the <body> tag:
    y1 = get_body(y1)
    return [y0, y1]



def list_files_all(dir):
    """ 
    List files in the given directory.

    Args:
        dir (str): path to a directory

    Returns:
        lst ([str]): list of filenames in directory
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



def loop_away(filelist, outdir=os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'tmp')), verbose=False, clean=False, features='lxml'):
    """
    Loop over all files in a given directory.

    Args:
        filelist ([str]): list of filenames (including path) to be processed
        outdir (str): path to output directory

    Returns:
        None
    """ 
    print('\nOutput files will be saved in the following directory:\n\n', outdir, '\n\nSet `outdir` in function `loop_away` to change the default directory.')
    # if directory `tmp` does not exist, create it:
    from pathlib import Path
    Path('tmp').mkdir(parents=True, exist_ok=True)
    # container to hold list of files that raise an error
    errors = []
    for file in filelist:
        filename = os.path.basename(file)
        outpath = os.path.join(outdir, filename)
        # hard-coded names and classes of tags that contain definitions:
        names = ['blockquote']
        classes = ['calibre27']
        # get the header from the source file:
        try:
            print('\n\nPROCESSING FILE', filename, ':\n')
            with open(file, encoding='utf8') as infile:
                head = get_head(infile, features=features)
            # open an infile to process input and an outfile to save the output:
            with open(file) as infile, open(outpath, 'w') as outfile:
                # get the body from the source file:
                soup = BeautifulSoup(infile, features=features)
                body = soup.find('body')
                # process the children:
                for child in body.findChildren(recursive=False):
                    print('■', end='', flush=True)
                    if verbose:
                        print_child_info(child)
                    # selected tags are printed as is: 
                    if child.name in ['h1', 'h2', 'h3', '\n']:
                        print(child, file=outfile)
                    # tags that contain dictionary definitions are processed:
                    # (`names` and `classes` are hard-coded lists defined above)
                    elif child.name in names and any(c in child['class'] for c in classes):
                        # convert to string, feed to `dictionarize()`, and print:
                        s = str(child)
                        s = dictionarize(s, verbose=verbose, clean=clean, features=features)
                        s = s + '\n' # add empty line for clarity
                        print(s, file=outfile)
                    else:
                        # remove all other children: 
                        if verbose:
                            print('\nThis child was removed:\n', child)
                            print('\nCheck that this is desired behaviour. If not, add to the hard-coded list of `names` and `classes`.')
                        child.extract(strip=True)
                # exit the loop after all the children have been processed
            # insert the body of the output file into the head of the input file: Note the 'r+' argument
            # (this process reads the outfile, adds the head, and overwrites it with the complete html page)
            with open(outpath, 'r+') as outfile:
                body = outfile.read()
                html = make_html(body=body, head=head, features=features)
                outfile.seek(0)
                outfile.write(html)
                outfile.truncate()
        # if something goes wrong, log the error:
        except Exception as e:
            errors.append(filename)
            print('\n\nCRITICAL ERROR! \n\nPROBLEM WITH:\n\n', file, '\n\nAN ERROR WAS LOGGED\n\n')
            import logging
            logging.error("Exception occurred: %s", e)
            import traceback
            trace = traceback.format_exc()
            logging.error(trace)
    print('\n\nALL FILES PROCESSED, BUT CHECK THE LOGS FOR ANY ERRORS.')
    if not errors:
        print('\nGREAT NEWS: NO EXCEPTIONS RAISED!')
    else:
        print('\nThe following files raised an exception:', errors)
    return None



def make_definition(soup, verbose=False, clean=False):
    """
    Extracts definition from dictionary entry.

    Args:
        soup (bs4.BeautifulSoup): extracted portion of a word definition

    Returns:
        defn (str): word definition reformatted to conform to desired html styles
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
    # remove blank lines:
    s = re.sub(r'\n+', '\n', s)
    if not s:
        s = 'Definition missing'
    defn = '<div>'+s+'</div>'
    return defn



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
    if n > 1:
        raise ValueError('More than one body tags found inside body!')
    if n == 0:
        body = '<body>' + body + '</body>'
    # the body element should be tagged by <body></body>
    body = BeautifulSoup(body, features=features).find('body')
    html = BeautifulSoup(head, features=features)
    html.head.insert_after(body)
    html = str(html)
    return html



def make_label(soup):
    """
    Extracts a label from dictionary entry. Uses first part of word definition.

    Args:
        soup (bs4.BeautifulSoup): dictionary entry

    Returns:
        label (str): label used to identify the dictionary entry
    """
    x = soup.find('body')
    x = str(x)
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
    label = str(s).strip()
    return label



def make_headword(tag):
    """
    Extracts short and long header from dictionary entry and tag appropriately. 

    Args:
        tag (bs4.element.Tag): dictionary entry

    Returns:
        word (str): word used as the header of the dictionary entry
    
    Examples of tag:
        <p class="df"><strong class="calibre13">hepatectomia</strong></p>
        <p class="df"><strong class="calibre13"><sup class="calibre23">3</sup>H</strong><sup class="calibre23">2</sup></p>
    """
    # print_soup_info(soup)  # debugging
    y0, y1 = get_headword(tag)
    # Now substitute the words into:
    s = """
    <div><span><b>y0</b></span></div><span>y1.</span>
    """
    s = s.replace('y0', y0, 1)
    s = s.replace('y1', y1, 1)
    headword = s.strip()
    return headword



def print_children(soup):
    """
    Print information about all children and descendents.

    Args: 
        soup (bs4.BeautifulSoup): dictionary entry

    Returns: 
        None
    """
    print('Function trim_entry() creates a BeautifulSoup object from a string\n')
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
        child (bs4.BeautifulSoup): child of dictionary entry

    Returns: 
        None
    """
    print('child.name =', child.name)
    print('child["class"]', child['class'])
    return None


def print_soup_info(soup, name=None):
    """
    Print information about a BeautifulSoup object for degugging purposes.
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
    Prints a function docstring.

    Args: 
        docstring (str): documentation

    Returns: 
        None
    """
    print('\n\nThe `verbose` flag has been set to `True`\n')
    print('Summary of main function:\n')
    print(docstring, '\n')
    return None



def print_output(output):
    """
    Print output to screen surrounded by double lines (more visible, useful for debugging).

    Args: 
        input (str): any string

    Returns: 
        None
    """
    print('\n\nOUTPUT PRINTOUT:\n================\n', output, '\n================\n\n')
    return None



def print_type(*args):
    """
    Print information about types. 

    Args: 
        tuple (any type): tuple of any size

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
    for s in args:
        text = text.replace(s, replace)
    return text



def strip_black_square(soup):
    """
    Remove special character '■' and associated tag from a dictionary definition. 

    Args:
        soup (bs4.BeautifulSoup): a dictionary definition processed as a BeautifulSoup object

    Returns:
        soup (bs4.BeautifulSoup): argument with all instances of <sup>■</sup> removed 
    """    
    for x in soup.find_all('sup'):
        if '■' in x.get_text():
            x.extract(strip=True)
            break
    return soup



def strip_spaces(html):
    """
    Strip extra spaces from web page content.

    Args:
        soup (str, BeautifulSoup, Tag, NavigableString)
    Returns:
        Wrapper around `strip_spaces_st()` and `strip_spaces_bs()`
    """
    if isinstance(html, str):
        return strip_spaces_st(html)
    elif isinstance(html, (BeautifulSoup, Tag, NavigableString)):
        return strip_spaces_bs(html)
    else:  # here for debugging purposes
        raise ValueError('function strip_spaces() expects a string, a BeautifulSoup object or a Tag')



def strip_spaces_bs(soup):
    """
    Strip extra spaces from a BeautifulSoup object.

    Args:
        soup (BeautifulSoup, Tag, NavigableString): any soup
    
    Returns:
        soup (BeautifulSoup, Tag, NavigableString): with white spaces stripped out
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
    
    Note:
        Leaves undesired spaces in some cases. 
    """
    html = re.sub('\s{2,}', ' ', html)
    return html



def strip_comment(soup):
    """
    Strip comment from BeautifulSoup object

    Args:
        soup (bs4.BeautifulSoup): any soup
    
    Returns:
        soup (bs4.BeautifulSoup): with comments stripped out
    """
    f = soup.find_all(text=lambda text:isinstance(text, Comment))
    [fi.extract(strip=True) for fi in f]
    return soup



def strip_empty_tags(soup, strip_lines=False):
    """
    Remove empty tags from a BeautifulSoup object.
    If `strip_lines=True`, empty lines are also removed. 
    Argument `strip_lines` is passed down to `extract(strip=strip_lines)`
    
    Args: 
        soup (bs4.BeautifulSoup): html content with empty tags

    Returns: 
        soup (bs4.BeautifulSoup): original soup with empty tags removed

    """
    for item in soup.find_all():
        if len(item.get_text(strip=True)) == 0:
            item.extract(strip=strip_lines)
    return soup



def strip_header(xml, header='<?xml version="1.0" encoding="utf-8"?>'):
    """
    Remove unwanted header introduced when using the `xml` parser
    using the re module to make case-insensitive replacement.

    Args: 
        xml (str): an xml page
        
    Returns:
        xml (str): an xml page with xml header removed
    """
    esc = re.escape(header) 
    xml = re.sub(esc, '', xml, flags=re.IGNORECASE | re.MULTILINE).strip()
    return xml



def strip_tag(soup:BeautifulSoup, *args:str):
    """
    Remove tag from BeautifulSoup object
    
    Args: 
        soup (bs4.BeautifulSoup): any soup with tags
        args (str): name of the tags to be removed
        usage: strip_tag(soup, 'sup', 'sub')
        
    Returns:
        soup (bs4.BeautifulSoup): soup without tags
    """
    for arg in args:
        f = soup.find_all(arg)
        [fi.unwrap() for fi in f]
        break
    return soup



def split_entry(soup):
    """
    Splits dictionary entry into three parts. 

    Args:
        soup (bs4.BeautifulSoup): A word definition processed by trim_entry()

    Returns:
        s1, s2, s3: A 3-tuple of BeautifulSoup objects.
    """
    # slice soup into chunks:
    s1, s2, s3 = '', '', '' 
    # slice s1: word label for lookup
    f = soup.find_all('p', attrs={'class':'rf'})
    if f is not None:
        for p in f:
            s1 = soup.p.extract(strip=True)
    # slice s2: word long and short forms 
    f = soup.find_all('p', attrs={'class':'df'})
    if f is not None:
        for p in f:
            s2 = soup.p.extract(strip=True)
    # slice s3: word definition
    f = soup.find_all('p', attrs={'class':['rf','df']})
    if f is not None:
        # remove p tags with classes rf and df 
        for p in f:
            p.extract(strip=True)
        # save the part enclosed in blockquotes
        s3 = soup.find('blockquote')
    return s1, s2, s3



def trim_entry(item, verbose=False, clean=False, features='lxml'):
    """
    Takes a single dictionary definition and checks for validity. 
    Also trims certain tags and formatting. 

    Args:
        item (str): A word definition extracted from the GDLC azw dictionary.
        verbose (bool, optional)
        clean (bool, optional)
        features (str, optional)

    Returns:
        BeautifulSoup or string()

    Raises:
        Exception: If item is not a string
    """
    try:
        soup = BeautifulSoup(item, features=features)
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
    # clean further upon request
    if clean:
        clean_tags(soup)
    return soup


