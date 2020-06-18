""" 
Process a dictionary written in document markup language.

>>> from GDLC.GDLC import *
>>> file = Path('~/GDLC/source/GDLC_unpacked/mobi8/OEBPS/Text/part0150.xhtml').expanduser()
>>> tags = ['blockquote']
>>> classes = ['calibre27']
>>> protected = ['h1', 'h2', 'h3', 'h4', 'h5', '\n']
>>> with open(file, encoding='utf8') as infile:
...     soup = BeautifulSoup(infile, features='lxml')
...     dico = make_dictionary(soup.body, tags=tags, protected=protected, classes=classes)
>>> print(dico)

"""

