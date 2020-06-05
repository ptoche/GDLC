"""
This file tests a patch on the bs4.BeautifulSoup method extract()

>>> from GDLC.GDLC import *
>>> html = '''<html>
... <head>
...   <title>Unknown</title>
... </head>
...   <body>LOOSE TEXT
...     <a></a>
...     <p></p>
...     <div>BODY</div>
...     <b></b>
...     <i></i> # COMMENT
...   </body>
... </html>'''
>>> soup = BeautifulSoup(html, features='lxml')
>>> print(strip_empty_tags(soup, strip_lines=True))
<html>
<head>
<title>Unknown</title>
</head>
<body>LOOSE TEXT
    <div>BODY</div> # COMMENT
  </body>
</html>

"""
