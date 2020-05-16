""" 
Extract label from word definition: Takes the first element s1 returned by `split_defn()`

>>> from GDLC.GDLC import *
>>> html = '''<p class="rf">-&gt;AAA<sup class="calibre32">1</sup></p>'''
>>> soup = BeautifulSoup(html, features = 'lxml')
>>> print(make_label(soup))
<idx:orth value="<body><p class="rf">-&gt;AAA<sup class="calibre32">1</sup></p></body>">
      <idx:infl>
        <idx:iform name="" value="<body><p class="rf">-&gt;AAA<sup class="calibre32">1</sup></p></body>"/>
      </idx:infl>
    </idx:orth>

"""
