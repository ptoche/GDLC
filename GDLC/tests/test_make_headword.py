""" 
Make headword for definition: Takes the second element s2 returned by `split_entry()`

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

>>> print(make_headword(s1))
<div><span><b>->AAA</b></span></div><span><p>-&gt;AAA</p>.</span>

"""
