""" 
Strip tags from a BeautifulSoup object:

>>> from GDLC.GDLC import *
>>> html = '''
... <blockquote class="calibre27">
... <p class="rf">-&gt;AAA<sup class="calibre32">1</sup></p>
... <p class="df"><code class="calibre22"><sup class="calibre23">■</sup><strong class="calibre13">AAA -bb</strong></code><sup class="calibre23">1</sup></p>
... <p class="ps">Definition here.</p>
... <p class="p">More details here.</p>
... <p class="p">Even more details here.</p>
... </blockquote>
... '''
>>> soup = BeautifulSoup(html, features = 'lxml')
>>> print(strip_tag(soup, 'code', 'sup'))
<html><body><blockquote class="calibre27">
<p class="rf">-&gt;AAA<sup class="calibre32">1</sup></p>
<p class="df"><sup class="calibre23">■</sup><strong class="calibre13">AAA -bb</strong><sup class="calibre23">1</sup></p>
<p class="ps">Definition here.</p>
<p class="p">More details here.</p>
<p class="p">Even more details here.</p>
</blockquote>
</body></html>

"""
