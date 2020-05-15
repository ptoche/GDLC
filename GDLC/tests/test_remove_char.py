""" 
Remove special characters from a string:

>>> from GDLC.GDLC import *
>>> test = '''<p class="df"><code class="calibre22"><sup class="calibre23">■</sup><strong class="calibre13">AAA -bb</strong></code><sup class="calibre23">1</sup></p>'''
>>> print(remove_char(test, '■', '-&gt;'))
<p class="df"><code class="calibre22"><sup class="calibre23"></sup><strong class="calibre13">AAA -bb</strong></code><sup class="calibre23">1</sup></p>

"""
