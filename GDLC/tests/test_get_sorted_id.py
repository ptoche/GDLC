""" 
Get a list of duplicated IDs in a dynamic markup document.

>>> from GDLC.GDLC import *
>>> dml = '''
... <?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml">
... <head>
... <title>TITLE</title>
... </head>
... <body>
... <blockquote class="calibre27" id="d12345"><p>First occurrence of id="d12345"</p></blockquote>
... <blockquote class="calibre27" id="d67890"><p>A single occurrence of id="d67890"</p></blockquote>
... <blockquote class="calibre27" id="d12345"><p>Second occurrence of id="d12345"</p></blockquote>
... </body>
... </html>
... '''

From a string:
>>> print(get_sorted_id(dml))
{'unique': ['d12345', 'd67890'], 'duplicate': ['d12345']}

From a BeautifulSoup object:
>>> soup = BeautifulSoup(dml, features='lxml')
>>> print(get_sorted_id(soup))
{'unique': ['d12345', 'd67890'], 'duplicate': ['d12345']}

From a Tag object: 
>>> tag = soup.find('body')
>>> print(get_sorted_id(tag))
{'unique': ['d12345', 'd67890'], 'duplicate': ['d12345']}

List unique IDs only:
>>> get_unique_id(dml)
['d12345', 'd67890']

List duplicate IDs only:
>>> get_duplicate_id(dml)
['d12345']

"""
