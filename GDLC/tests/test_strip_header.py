""" 
Strip header from an xml string:

>>> from GDLC.GDLC import *

# Strip the default header:
>>> dml = '''\
... <?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml">
... <head>
...   <title>TITLE</title>
... </head>
... <body>
...   BODY
... </body>
... </html>'''

>>> print(strip_header(dml))
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>TITLE</title>
</head>
<body>
  BODY
</body>
</html>

Strip a custom header:
>>> dml = '''\
... <?xml version="1.0" encoding="UTF-16" standalone="no"?><html xmlns="http://www.w3.org/1999/xhtml">
... <head>
...   <title>TITLE</title>
... </head>
... <body>
...   BODY
... </body>
... </html>'''

>>> print(strip_header(dml, header='<?xml version="1.0" encoding="UTF-16" standalone="no"?>'))
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>TITLE</title>
</head>
<body>
  BODY
</body>
</html>

"""
