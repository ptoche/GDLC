""" 
Remove excess white spaces around punctuation marks:

# An html page with too many white spaces:
>>> from GDLC.GDLC import *
>>> dml = '''\
... <?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml">
... <head>
...   <title>TITLE</title>
... </head>
... <body>
...   <blockquote>
...     <p>White space preceding a period .</p>
...     <p>White space preceding a comma ,</p>
...     <p>White space preceding a question mark ?</p>
...     <p>White space preceding an exclamation mark !</p>
...   </blockquote>
... </body>
... </html>'''

# Strip white spaces from a BeautifulSoup object:
>>> soup = BeautifulSoup(dml, features='lxml')
>>> print(strip_spacing_from_soup(soup, strip=False))

>>> print(strip_spacing_from_soup(soup, strip=True))


"""
