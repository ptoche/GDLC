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
        return clean_from_soup_lxml(xml)
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
def clean_from_soup_lxml(xml, indent=4):
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




# IN PROGRESS
def make_entry_id(soup:BeautifulSoup):
    """
    Args:
    """
    tags = soup.find_all('idx:entry')
    for tag in tags:
        # if <idx:entry> has an id, suppress it:
        for attr in tag.attrs('id'):
            del tag.attr
        for i, j in enumerate(tags):
            tag.attrs['id'] = i
            tag.attrs.append(('id', i))
            TRY ON OF THESE
                













# IN PROGRESS
# TO DO: summarize the meta info in xhtml files
# Use a multi-level dictionary?
def get_meta_dml(dir, tags=[], encoding='utf8', features='lxml'):
    """
    Wrapper to read meta content of dynamic markup language (dml) file. 

    Args:
        dir(str, BeautifulSoup): directory to a dictionary written in dynamic markup language
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


def get_meta_dml_from_soup(soup:BeautifulSoup, tags=[]):
    """
    Make a dictionary of some relevant information stored in dml files.

    Args:
        soup (BeautifulSoup): dynamic markup language in BeautifulSoup format
        tags ([str]): list of tags of interest, e.g. tags=['title', 'language']
    Returns:
        content ({str:str}): a dictionary of tags and meta content stored in opf file
    """
    # extract and store meta tags
    content = {}
    if tags:
        for tag in tags:
            for item in soup.find_all(tag):
                content.update({tag: item.contents[0]})
    return content

get_meta_dml_from_soup(soup)



# IN PROGRESS
def check_content(dir, encoding='utf8', features='lxml'):
    """
    Check that various attributes stated in content.opf are internally consistent.
    Loops through all text files looking for inconsistencies with content.opf.

    Args:
        dir(str, BeautifulSoup): directory to a dictionary written in dynamic markup language
        encoding (str): encoding used, default is 'utf8'
        features (str): parser used, default is 'lxml'
    
    Returns:
        entry ({str:str}): a dictionary of entries where problems were detected 
    
    Notes: 
        The <idx:entry> tag can carry the name, scriptable, and spell attributes. The name attribute indicates the index to which the headword belongs. The value of the name attribute should be the same as the default lookup index name listed in the OPF. The scriptable attribute makes the entry accessible from the index. The only possible value for the scriptable attribute is "yes". The spell attribute enables wildcard search and spell correction during word lookup. The only possible value for the spell attribute is "yes". 
    Checks:
        name, scriptable, spell
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
        dir(str, BeautifulSoup): directory to a dictionary written in dynamic markup language.
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

# clean_href
href="Text/part0004.xhtml#aid-3Q281"