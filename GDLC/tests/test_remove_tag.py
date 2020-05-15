""" 
Remove tags from a BeautifulSoup object:
>>> test = BeautifulSoup('''<blockquote class="calibre27">
    <p class="rf">-&gt;AAA<sup class="calibre32">1</sup></p>
    <p class="df"><code class="calibre22"><sup class="calibre23">■</sup><strong class="calibre13">AAA -bb</strong></code><sup class="calibre23">1</sup></p>
    <p class="ps">Definition here.</p>
    <p class="p">More details here.</p>
    <p class="p">Even more details here.</p>
  </blockquote>''', features = 'lxml')
>>> print(remove_tag(test, 'code', 'sup'))
<html><body><blockquote class="calibre27">
<p class="rf">-&gt;AAA1</p>
<p class="df">■<strong class="calibre13">AAA -bb</strong>1</p>
<p class="ps">Definition here.</p>
<p class="p">More details here.</p>
<p class="p">Even more details here.</p>
</blockquote></body></html>
"""
