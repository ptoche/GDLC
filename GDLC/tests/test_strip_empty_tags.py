"""
Remove empty tags.

>>> from GDLC.GDLC import *
>>> dml = '''\
... <html>
... <head>
...   <title>TITLE</title>
... </head>
... <body>LOOSE TEXT
...   <div></div>
...   <p></p>
...   <div>MORE TEXT</div>
...   <div><b></b></div>
...   <p><i></i></p> # COMMENT
... </body>
... </html>'''
>>> soup = BeautifulSoup(dml, features='lxml')

>>> print(strip_empty_tags(soup, strip_lines=True))
<html>
<head>
<title>TITLE</title>
</head>
<body>LOOSE TEXT
  <div>MORE TEXT</div> # COMMENT
</body>
</html>

"""
