""" 
Make headword for definition: Takes the second element s2 returned by `split_entry()`

>>> from GDLC.GDLC import *
>>> ml = '''<body>
... <p class="df"><code class="calibre22"><sup class="calibre23">■</sup><strong class="calibre13">ABC -xy</strong></code><sup class="calibre23">1</sup></p>
... </body>'''
>>> soup = BeautifulSoup(ml, features='lxml')
>>> tag = soup.find('body')

>>> print(make_headword(tag))
<div><span><b>ABC</b></span></div><span><code class="calibre22"><sup class="calibre23">■</sup><strong class="calibre13">ABC -xy</strong></code><sup class="calibre23">1</sup>.</span>

"""
