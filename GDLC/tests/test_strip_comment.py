""" 
Remove comments from BeautifulSoup object:

An html page with comments:
>>> from GDLC.GDLC import *
>>> html = '''
... <?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml">
... <head>
... <title>Unknown</title>
... <!-- Need to come up with a title! -->
... </head>
... <body>
... <!-- Need to come up with better text! -->
... BODY text that includes ■ and ñ 
... </body>
... </html>
... '''
>>> soup = BeautifulSoup(html, features='lxml')

Strip comments from a BeautifulSoup object by extracting:
>>> print(strip_comment(soup))
<?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Unknown</title>
<BLANKLINE>
</head>
<body>
<BLANKLINE>
BODY text that includes ■ and ñ 
</body>
</html>

"""
