""" 
Strip class attribute of given tags from a BeautifulSoup object:

>>> from GDLC.GDLC import *
>>> ml = '''<p class="df"><code class="calibre22"><sup class="calibre23">■</sup><strong class="calibre13">ABC -xy</strong></code><sup class="calibre23">1</sup></p>'''
>>> soup = BeautifulSoup(ml, features='lxml')

>>> print(strip_chars(soup, 'squares'))
<html><body><p class="df"><code class="calibre22"><strong class="calibre13">ABC -xy</strong></code><sup class="calibre23">1</sup></p></body></html>

"""
