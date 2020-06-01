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

Todo:
    * Check code for parsers other than lxml
    * Check if all definitions are in blockquote with class calibre27
    * Check case of missing or malformed tags, e.g. with missing word or line-ending slash
    * Make function to list children to skip and print as is, e.g. <h1>
    * Test find_all instead of findChildren and check robustness of extract body code
    * Test body.descendants instead of body.children
    * Break code into smaller pieces so utility functions may have wider applicability

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
        soup (BeautifulSoup object): soup to clean

    Returns:
        soup (BeautifulSoup object)
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
    soup = trim_defn(item, verbose=verbose, clean=clean, features=features)
    # Emtpy or malformed definitions return None, return empty string if None
    if not soup:
        return ''
    # Split dictionary entry into parts:
    s1, s2, s3 = split_defn(soup, verbose=verbose, clean=clean, features=features)
    # Extract label value for dictionary entry: 
    s1 = make_label(s1)
    # Extract first word for word header: 
    s2 = make_word(s2)
    # Extract the dictionary definition:
    s3 = make_defn(s3, verbose=verbose, clean=clean)
    # Concatenate label, word, definition, and tag group:
    s = '<idx:entry scriptable="yes">' + '\n' + s1 + s2 + s3 + '\n' + '</idx:entry>'
    if features == 'xml':
        s = strip_header(s)
    if verbose:
        print_output(s)
    return s


def get_body(html, features='lxml'):
    """
    Extract the body from an html/xml file. 

    Args:
        html (str, BeautifulSoup, Tag): html page with head and body
    
    Returns:
        body (str): body of the html page
    """
    # string-based approach below works only for bare body tags <body> and </body>
    if isinstance(html, str):
        r1, r2 = '^.*<body>', '^.*>ydob/<'
        body = re.sub(r2, '', re.sub(r1, '', html, flags=re.DOTALL)[::-1], flags=re.DOTALL)[::-1]
    # all BeautifulSoup objects are also Tag objects, but not the reverse, so check Beautifulsoup first
    # if BeautifulSoup: intended to work on any BeautifulSoup object:
    elif isinstance(html, BeautifulSoup):
        soup = html
        body = soup.find('body')
        body = ''.join(['%s' % x for x in body])
    # if Tag: intended to work if body tag has class or id:
    elif isinstance(html, Tag):
        soup = BeautifulSoup(str(html), features=features)  # essentially re-doing previous step... ugly
        body = ''.join(['%s' % x for x in soup.body.contents])  # ? soup.find('body') equivalent to soup.body.contents
    else:
        raise ValueError('function get_body() expects either a string or a BeautifulSoup object')
    body = re.sub(r'\n+', '\n', body).strip()  # .strip() removes leading/trailing blankspaces/newlines
    return body



def get_head(html, features='lxml'):
    """
    Extract the head from an html/xml file. 
    Args:
        html (str): html page with head and body

    Returns:
        head (str): head of the html page
    
    To do: allow BeautifulSoup object and Tag, similar to get_body()
    """
    html = BeautifulSoup(html, features=features)
    body = html.find('body')
    body.decompose()
    head = str(html).strip()
    return head



def loop_away(filelist, outdir=os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'tmp')), verbose=False, clean=False, features='lxml'):
    """ Loop over all files in a given directory""" 
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
            print('\n\nPROCESSING FILE:\n')
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
                        s = s + '\n' # add blank line for clarity in debugging
                        print(s, file=outfile)
                    else:
                        # remove all other children: 
                        if verbose:
                            print('\nThis child was removed:\n', child)
                            print('\nCheck that this is desired behaviour. If not, add to the hard-coded list of `names` and `classes`.')
                        child.extract()  # a blank line will be introduced at extraction locus
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
    return html



def make_defn(soup, verbose=False, clean=False):
    """
    Extracts definition from dictionary entry.

    Args:
        soup (BeautifulSoup object): extracted portion of a word definition

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



def make_names(filepath, first=None, last=None):
    """ 
    List files to be processed 

    Args:
        filepath (str): path to the file including file name and extension
        first (num): first file name to be included
        last (num): last file name to be included

    Returns:
        r ([str]): list of selected filenames in directory
    """
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



def make_label(soup):
    """
    Extracts a label from dictionary entry. Uses first part of word definition.

    Args:
        soup (BeautifulSoup object): dictionary entry

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
    s = str(s)
    label = s.strip('\n')
    return label



def get_tag_content(tag):
    if not isinstance(tag, Tag):
        print('get_tag_content() only accepts objects of type `Tag`')
    # Suppress superscripts:
    for sup in tag.find_all('sup'):
        sup.decompose()
    # Extract words:
    y0 = tag.get_text()
    # Extract first part of words:
    y0 = y0.split(' ', 1)[0]
    # Extract all words without superscripts:
    y1 = ''
    for child in tag.children:
        y1 += str(child)
    y1 = get_body(y1)
    return [y0, y1]


def make_word(tag):
    """
    Extracts header from dictionary entry. Uses second part of word definition. 

    Args:
        tag (bs4.element.Tag): dictionary entry

    Returns:
        word (str): word used as the header of the dictionary entry
    
    Examples of tag:
        <p class="df"><strong class="calibre13">hepatectomia</strong></p>
        <p class="df"><strong class="calibre13"><sup class="calibre23">3</sup>H</strong><sup class="calibre23">2</sup></p>
    """
    # print_soup_info(soup)  # debugging
    y0, y1 = get_tag_content(tag)
    # Now substitute the words into:
    s = """
    <div><span><b>y0</b></span></div><span>y1.</span>
    """
    s = s.replace('y0', y0, 1)
    s = s.replace('y1', y1, 1)
    word = s.strip('\n')
    return word



def print_children(soup):
    """
    Print information about all children and descendents.

    Args: 
        soup (BeautifulSoup object): dictionary entry

    Returns: 
        None
    """
    print('Function trim_defn() creates a BeautifulSoup object from a string\n')
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
        child (BeautifulSoup object): child of dictionary entry

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



def strip_blanklines(item, verbose=False, features='lxml'):
    """
    Remove blank lines from string or BeautifulSoup object.

    Args: 
        item (str, BeautifulSoup): 

    Returns: 
        item (str, BeautifulSoup): returns same type as argument
    """
    if not isinstance(item, (str, BeautifulSoup, Tag)):
        print('strip_blanklines() only accepts objects of type `str`, `BeautifulSoup`, `Tag`')
    try:
        # strip from string:
        if isinstance(item, str):
            return item.strip()
            #return re.sub(r'\n+', '\n', item)
        # strip from bs:
        if isinstance(item, (BeautifulSoup, Tag)):
            return strip_blanklines_bs(item, verbose=verbose, features=features)
    except Exception as e:
        return e



def strip_blanklines_bs(soup, verbose=False, features='lxml'):
    """
    Removes blank lines from a BeautifulSoup object
    """
    try:
        # check if the soup has a body
        b = soup.find('body')
        if str(b).strip('\n'):
            # look inside each body element
            try:
                for bi in b:
                    # check if the body elements has children
                    c = bi.findChildren(recursive=False)
                    for ci in c:
                        # strip from each element of the child
                        if str(ci):
                            f = ci.contents
                            # `if str(x).strip()` removes empty list items:
                            r = ''.join(['%s' % x for x in f if str(x).strip('\n')])
            except:
                # if the body elements have no children, strip from each body element content
                f = b.contents
                r = ''.join(['%s' % x for x in f if str(x).strip('\n')]).strip()
        else:
            # if the body has no child, strip lines from body.contents
            r = soup.body.contents.strip()
            print('CRUCIAL STEP')
            #r = re.sub(r'\n+', '\n', ''.join(soup.body.contents))
        if not str(r).strip('\n'):
            pass
        else:
            soup = BeautifulSoup(r, features=features)
    except:
        # if the soup has no body, pass
        if verbose:
            print('No body found in BeautifulSoup body: pass')
        pass
    return soup



def strip_comment(soup):
    """
    Strip comment from BeautifulSoup object

    Args:
        soup (BeautifulSoup object): any soup
    
    Returns:
        soup (BeautifulSoup object): with comments stripped out
    """
    f = soup.find_all(text=lambda text:isinstance(text, Comment))
    [fi.extract() for fi in f]
    return soup



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



def strip_header(xml):
    """
    Remove unwanted header introduced when using the `xml` parser
    using the re module to make case-insensitive replacement.

    Args: 
        xml (str): an xml page
        
    Returns:
        r (str): an xml page with xml header removed

    To do: pass the header as a default, second argument, in case there are situations with different version or encoding.
    """
    h = re.escape('<?xml version="1.0" encoding="utf-8"?>') # re.escape ? and .
    r = re.sub(h, '', xml, flags=re.IGNORECASE | re.MULTILINE)
    return r



def strip_tag(soup:BeautifulSoup, *args:str):
    """
    Remove tag from BeautifulSoup object
    
    Args: 
        soup (BeautifulSoup object): any soup with tags
        
    Returns:
        soup (BeautifulSoup object): soup without tags
    """
    for arg in args:
        f = soup.find_all(arg)
        [fi.unwrap() for fi in f]
        break
    return soup



def split_defn(soup, verbose=False, clean=False, features='lxml'):
    """
    Splits dictionary entry into three parts. 

    Args:
    soup (BeautifulSoup): A word definition processed by trim_defn()
    verbose (bool, optional)
    clean (bool, optional)
    features (str, optional)

    Returns:
        A 3-tuple of BeautifulSoup objects.
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
        s3 = soup.find('blockquote')
        # remove unwanted blank lines introduced by p.extract()
        # 'bs4.element.Tag'
        s3 = strip_blanklines_bs(s3)
    if verbose:
        print_type(s1, s2, s3)
    return s1, s2, s3



def trim_defn(item, verbose=False, clean=False, features='lxml'):
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
        Exception: If item is not a string.
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
    # Always remove special character <sup>■</sup>
    for x in soup.find_all('sup'):
        if '■' in x.get_text():  # replace_strings(html, '■')
            x.extract()
            break
    # clean further upon request
    if clean:
        clean_tags(soup)
    return(soup)

