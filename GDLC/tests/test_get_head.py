""" 
Extract the head from an html page formatted as string.

>>> from GDLC.GDLC import *
>>> html = '''<?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml"><head><title>Unknown</title><meta content="text/html; charset=utf-8" http-equiv="Content-Type"/><link href="../Styles/style0001.css" rel="stylesheet" type="text/css"/><link href="../Styles/style0002.css" rel="stylesheet" type="text/css"/></head><body>BODY</body></html>'''
>>> print(get_head(html))
<?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml"><head><title>Unknown</title><meta content="text/html; charset=utf-8" http-equiv="Content-Type"/><link href="../Styles/style0001.css" rel="stylesheet" type="text/css"/><link href="../Styles/style0002.css" rel="stylesheet" type="text/css"/></head></html>

"""
