""" 
Extract the body from an html page, whether the page is formatted as string or BeautifulSoup object or Tag.

>>> from GDLC.GDLC import *
>>> html = '''<?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml"><head><title>Unknown</title><meta content="text/html; charset=utf-8" http-equiv="Content-Type"/><link href="../Styles/style0001.css" rel="stylesheet" type="text/css"/><link href="../Styles/style0002.css" rel="stylesheet" type="text/css"/></head><body>BODY</body></html>'''

From a string (the default):
>>> print(get_body(html))
BODY

From a BeautifulSoup object:
>>> print(get_body(BeautifulSoup(html)))
BODY

From a Tag object: 
>>> print(get_body(BeautifulSoup(html).find('body')))
BODY

"""
