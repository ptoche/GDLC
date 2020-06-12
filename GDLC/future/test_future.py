""" 
Extract the root tag (processing instructions) from a html/xhtml/xml page.

>>> from GDLC.GDLC import *
>>> dml = '''<?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml">
... <head>
... <title>TITLE</title>
... </head>
... <body>
... BODY
... </body>
... </html>'''

# From a string:
>>> print(future.get_root(dml))
<?xml version="1.0" encoding="UTF-8"?>

# From a BeautifulSoup object:
>>> soup = BeautifulSoup(dml, features='lxml')
>>> print(future.get_root(soup))
<?xml version="1.0" encoding="UTF-8"?>

# From a Tag object:
>>> soup = BeautifulSoup(dml, features='lxml')
>>> tag = soup.find('head')
>>> print(future.get_root(tag))
<?xml version="1.0" encoding="UTF-8"?>

"""
