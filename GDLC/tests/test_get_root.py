""" 
Extract the root tag (processing instructions) from a html/xhtml/xml page.

>>> from GDLC.GDLC import *
>>> ml = '''<?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml">
... <head>
... <title>TITLE</title>
... </head>
... <body>
... BODY
... </body>
... </html>'''

# From a string:
>>> print(get_root(ml))
<?xml version="1.0" encoding="UTF-8"?>

# From a BeautifulSoup object:
>>> soup = BeautifulSoup(ml, features='lxml')
>>> print(get_root(soup))
<?xml version="1.0" encoding="UTF-8"?>

# From a Tag object:
>>> soup = BeautifulSoup(ml, features='lxml')
>>> tag = soup.find('head')
>>> print(get_root(tag))
<?xml version="1.0" encoding="UTF-8"?>

"""
