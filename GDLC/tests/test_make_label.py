""" 
Extract label from word definition: Takes the first element s1 returned by `split_defn()`

>>> from GDLC.GDLC import *
>>> dml = '''<p class="rf">-&gt;ABC<sup class="calibre32">1</sup></p>'''
>>> soup = BeautifulSoup(dml, features='lxml')
>>> tag = soup.find('p')

>>> print(make_label(tag))
<idx:orth value="ABC">
      <idx:infl>
        <idx:iform name="" value="ABC"/>
      </idx:infl>
    </idx:orth>

"""
