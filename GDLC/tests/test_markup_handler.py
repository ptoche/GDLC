""" 
Attempts to convert input to a BeautifulSoup object. Raises an exception if input type is not supported.

>>> from GDLC.GDLC import *
>>> input = 'a string to test invalid_types=[str]'
>>> markup_handler(input, invalid_types=[str])
Aborting. The input type was listed among the `invalid_types`.

"""
