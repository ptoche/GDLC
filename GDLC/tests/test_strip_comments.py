""" 
Strip comments from BeautifulSoup object:

An xml page with comments:
>>> from GDLC.GDLC import *
>>> ml = '''<?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml">
... <head>
... <!-- Comment 1 -->
... <title>TITLE surrounded by comments</title>
... <!-- Comment 2 -->
... </head>
... <!-- Comment 3 -->
... <body>
... <!-- Comment 4 -->
... BODY surrounded by comments
... <!-- Comment 5 -->
... </body>
... <!-- Comment 6 -->
... </html>'''
>>> soup = BeautifulSoup(ml, features='lxml')

>>> print(strip_comments(soup))
<?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>TITLE surrounded by comments</title>
</head>
<body>
BODY surrounded by comments
</body>
</html>

"""
