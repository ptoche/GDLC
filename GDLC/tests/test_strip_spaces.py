""" 
Remove excess white spaces from an html page:

An html page with too many white spaces:
>>> from GDLC.GDLC import *
>>> dml = '''\
... <?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml">
... <head>
...   <title>TITLE</title>
... </head>
... <body>
...   <blockquote>
...     <p>     Leading white space on this line.</p>
...     <p>Trailing white space on this line     .</p>
...     <p> White  spaces     everywhere     on  this  line .</p>
...   </blockquote>
... </body>
... </html>'''

Strip white spaces from a string:
>>> print(strip_spaces(dml))
<?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml">
<head> <title>TITLE</title>
</head>
<body> <blockquote> <p> Leading white space on this line.</p> <p>Trailing white space on this line .</p> <p> White spaces everywhere on this line .</p> </blockquote>
</body>
</html>

Strip white spaces from a BeautifulSoup object:
>>> soup = BeautifulSoup(dml, features='lxml')
>>> print(strip_spaces(soup))
<?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>TITLE</title>
</head>
<body>
<blockquote>
<p>Leading white space on this line.</p>
<p>Trailing white space on this line.</p>
<p>White spaces everywhere on this line.</p>
</blockquote>
</body>
</html>

"""
