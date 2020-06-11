""" 
Extracts content from objects of type <bs4.element.Tag>

>>> from GDLC.GDLC import *
>>> ml = '''<p class="df"><code class="calibre22"><sup class="calibre23">■</sup><strong class="calibre13">ABC -xy</strong></code><sup class="calibre23">1</sup></p>'''
>>> soup = BeautifulSoup(ml, features = 'lxml')
>>> tag = soup.find('p', attrs={'class':'df'})

>>> print(get_headword(tag))
['ABC', '<code class="calibre22"><sup class="calibre23">■</sup><strong class="calibre13">ABC -xy</strong></code><sup class="calibre23">1</sup>']

>>> from GDLC.GDLC import *
>>> ml = '<p class="df"><strong class="calibre13"><sup class="calibre23">3</sup>H</strong><sup class="calibre23">2</sup></p>'
>>> soup = BeautifulSoup(ml, features = 'lxml')
>>> tag = soup.find('p', attrs={'class':'df'})

>>> print(get_headword(tag))
['H', '<strong class="calibre13"><sup class="calibre23">3</sup>H</strong><sup class="calibre23">2</sup>']

"""
