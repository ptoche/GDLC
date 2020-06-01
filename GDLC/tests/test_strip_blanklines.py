""" 
Remove blank lines from a string or a BeautifulSoup object and returns an object of the same type:
To Do: Fix bug: If there is a blank line before the closing `body` tag, it will not be removed.

>>> from GDLC.GDLC import *

An html page with an empty tag that will result in empty lines after `p.extract()`:
>>> html = '''
... <?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml">
... <head>
... <title>Unknown</title>
... </head>
... <body>
... <p></p>
... BODY text that includes ■ and ñ 
... </body>
... </html>
... '''

Strip blanklines from string:
>>> print(strip_blanklines(html))
<?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Unknown</title>
</head>
<body>
<p></p>
BODY text that includes ■ and ñ 
</body>
</html>

>>> soup = BeautifulSoup(html, features='lxml')
Create blank lines inside a BeautifulSoup object by extracting:
>>> p = soup.find_all('p')
>>> for pi in p:
...     pi.extract()
>>> print(strip_blanklines(soup))
<html><body><p>BODY text that includes ■ and ñ</p></body></html>

An html page without a body at all:
>>> html = '''<html><head></head></html>'''
>>> print(strip_blanklines(html))
<html><head></head></html>

"""
