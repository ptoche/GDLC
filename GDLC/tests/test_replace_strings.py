""" 
Replace (or remove) special characters in a string:

>>> from GDLC.GDLC import *
>>> string = '''■ and -&gt; \n\nand ■ and -&gt;'''

>>> print(replace_strings(string, '■', '-&gt;', replace='BANANA'))
BANANA and BANANA 
<BLANKLINE>
and BANANA and BANANA

"""
