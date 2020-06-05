"""
This file tests a patch on the bs4.BeautifulSoup method extract().
The patch adds a `strip` argument with default value `False`. 
If `strip=True`, empty lines near the point of extraction are removed.
However, the extraction process still leaves more white space than desired.
A workaround is to filter the page as string and remove excess white spaces.

>>> from GDLC.GDLC import *
>>> html = '''
... <html>
... <head>
...   <title>Unknown</title>
... </head>
...   <body>
...     <div>Some <b>bold</b> statement.</div>
...     <div>Very <b>bold</b>.</div>
...   </body>
... </html>'''
>>> soup = BeautifulSoup(html, features='lxml')
>>> def test_extract(soup):
...     f = soup.find_all('b')
...     if f is not None:
...         for b in f:
...             b.extract(strip=True)
...     return soup
>>> print(test_extract(soup))
<html>
<head>
<title>Unknown</title>
</head>
<body>
<div>Some  statement.</div>
<div>Very .</div>
</body>
</html>

"""
