""" 
Strip tags from a BeautifulSoup object:

>>> from GDLC.GDLC import *
>>> dml = '''<html>
... <head>
...   <title>Unknown</title>
...   <script>This text is inside an invalid tag</script>
... </head>
...   <body>
...     <p>This text is inside a valid tag</p><style>Invalid!</style><invalid>Invalid!</invalid>
...   </body>
... </html>'''
>>> soup = BeautifulSoup(dml, features = 'lxml')
>>> print(destroy_tags(soup))
<html>
<head>
<title>Unknown</title>
</head>
<body>
<p>This text is inside a valid tag</p><invalid>Invalid!</invalid>
</body>
</html>

>>> print(destroy_tags(soup, 'invalid'))
<html>
<head>
<title>Unknown</title>
</head>
<body>
<p>This text is inside a valid tag</p></body>
</html>

"""
