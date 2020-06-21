""" 
Extract the HTML attributes from a html/xhtml/xml page.

>>> from GDLC.GDLC import *
>>> dml = '''\
... <?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml">
... <head>
...   <title>TITLE</title>
... </head>
... <body>
...   BODY
... </body>
... </html>'''

# From a string:
>>> print(get_html_attrs(dml))
{'xmlns': 'http://www.w3.org/1999/xhtml'}

# From a BeautifulSoup object:
>>> soup = BeautifulSoup(dml, features='lxml')
>>> print(get_html_attrs(soup))
{'xmlns': 'http://www.w3.org/1999/xhtml'}

# From a Tag object:
>>> soup = BeautifulSoup(dml, features='lxml')
>>> tag = soup.find('head')
>>> print(get_html_attrs(tag))
Aborting. Only objects of type str and BeautifulSoup are expected to have <html> attributes.
None

"""
