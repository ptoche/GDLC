""" 
Splits dictionary entry into three parts:

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
>>> soup = BeautifulSoup(html, features='lxml')
>>> s1, s2, s3 = split_entry(soup)

The first element of the return tuple, s1, is used to make a label:
>>> print(s1)
<p class="rf">-&gt;AAA<sup class="calibre32">1</sup></p>

The second element of the return tuple, s2, is used to make a heading:
>>> print(s2)
<p class="df"><code class="calibre22"><sup class="calibre23">■</sup><strong class="calibre13">AAA -bb</strong></code><sup class="calibre23">1</sup></p>

The third element of the return tuple, s3, is used to make a definition
>>> print(s3)
<blockquote class="calibre27">
<p class="ps">Definition here.</p>
<p class="p">More details here.</p>
<p class="p">Even more details here.</p>
</blockquote>

"""
