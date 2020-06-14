""" 
List all tags in soup that are not supported by Kindle ebooks.

>>> from GDLC.GDLC import *
>>> dml = '''<?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml">
... <head>
... <title>TITLE</title>
... </head>
... <body>
... <h1>A valid h1 tag <script>with an invalid script tag</script>.</h1>
... <div><script>An invalid script tag inside a valid div tag.</script></div>
... </body>
... </html>'''
>>> soup = BeautifulSoup(dml, features='lxml')

>>> list_invalid_tags(soup)
['title', 'script']

>>> list_invalid_tags(soup, valid=['h1', 'div'])
['html', 'head', 'title', 'body', 'script']

"""
