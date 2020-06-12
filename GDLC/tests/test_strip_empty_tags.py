"""
Remove empty tags.

>>> from GDLC.GDLC import *
>>> dml = '''<html>
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
>>> soup = BeautifulSoup(dml, features='lxml')

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
