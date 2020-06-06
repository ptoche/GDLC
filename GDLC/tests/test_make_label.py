""" 
Extract label from word definition: Takes the first element s1 returned by `split_defn()`

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

>>> print(make_label(s1))
<idx:orth value="<p class="rf">AAA<sup class="calibre32">1</sup></p>">
      <idx:infl>
        <idx:iform name="" value="<p class="rf">AAA<sup class="calibre32">1</sup></p>"/>
      </idx:infl>
    </idx:orth>

"""
