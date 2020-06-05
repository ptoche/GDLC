""" 
Extracts content from objects of type <bs4.element.Tag>

>>> from GDLC.GDLC import *
>>> html = '''<p class="df"><code class="calibre22"><sup class="calibre23">■</sup><strong class="calibre13">AAA -bb</strong></code><sup class="calibre23">1</sup></p>'''
>>> soup = BeautifulSoup(html, features = 'lxml')
>>> tag = soup.find('p', attrs={'class':'df'})
>>> print(get_headword(tag))
['AAA', '<code class="calibre22"><strong class="calibre13">AAA -bb</strong></code>']

>>> from GDLC.GDLC import *
>>> html = '<p class="df"><strong class="calibre13"><sup class="calibre23">3</sup>H</strong><sup class="calibre23">2</sup></p>'
>>> soup = BeautifulSoup(html, features = 'lxml')
>>> tag = soup.find('p', attrs={'class':'df'})
>>> print(get_headword(tag))
['H', '<strong class="calibre13">H</strong>']

"""
