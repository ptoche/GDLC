""" 
Extract the body from an html page, whether the page is formatted as string or BeautifulSoup object or Tag.

>>> from GDLC.GDLC import *
>>> html = '''
... <?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml">
... <head>
... <title>Unknown</title>
... </head>
... <body>
... BODY
... </body>
... </html>'''

From a string (the default):
>>> print(get_body(html))
BODY

From a BeautifulSoup object:
>>> soup = BeautifulSoup(html, features='lxml')
>>> print(get_body(soup))
BODY

From a Tag object: 
>>> print(get_body(BeautifulSoup(html, features='lxml').find('body')))
BODY

"""
