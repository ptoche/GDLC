""" 
Extract the dictionary definition: Takes the third element s3 returned by `split_defn()`

>>> from GDLC.GDLC import *
>>> html = '''
... <blockquote class="calibre27">
... <p class="ps">Definition here.</p>
... <p class="p">More details here.</p>
... <p class="p">Even more details here.</p>
... </blockquote>'''
>>> soup = BeautifulSoup(html, features='lxml')
>>> print(make_defn(soup))
<div><blockquote><span>Definition here.</span></blockquote>
<blockquote><span>More details here.</span></blockquote>
<blockquote><span>Even more details here.</span></blockquote></div>

"""
