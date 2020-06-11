""" 
Extract the dictionary definition: Takes the third element s3 returned by `split_entry()`

>>> from GDLC.GDLC import *
>>> ml = '''
... <blockquote class="calibre27">
... <p class="ps">Definition here.</p>
... <p class="p">More details here.</p>
... <p class="p">Even more details here.</p>
... </blockquote>'''
>>> soup = BeautifulSoup(ml, features='lxml')
>>> tag = soup.find('body')

>>> print(make_definition(tag))
<div><blockquote><span>Definition here.</span></blockquote>
<blockquote><span>More details here.</span></blockquote>
<blockquote><span>Even more details here.</span></blockquote></div>

"""
