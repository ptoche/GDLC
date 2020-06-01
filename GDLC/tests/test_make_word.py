""" 
Extracts header from word definition: Takes the second element s2 returned by `split_defn()`

>>> from GDLC.GDLC import *
>>> html = '''<p class="df"><code class="calibre22"><sup class="calibre23">■</sup><strong class="calibre13">AAA -bb</strong></code><sup class="calibre23">1</sup></p>'''
>>> soup = BeautifulSoup(html, features = 'lxml')
>>> print(make_word(soup))
<div><span><b>AAA</b></span></div><span><p class="df"><code class="calibre22"><strong class="calibre13">AAA -bb</strong></code></p>.</span>

"""
