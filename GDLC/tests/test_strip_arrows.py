""" 
Strip arrows from a string:

>>> from GDLC.GDLC import *
>>> ml = '''<p class="rf">-&gt;ABC<sup class="calibre32">1</sup></p>'''

>>> print(strip_arrows(ml))
<p class="rf">ABC<sup class="calibre32">1</sup></p>

"""
