"""
This file is used for debugging doctest: Fill in with your own content

>>> from GDLC.GDLC import *
>>> html = '<p class="df"><strong class="calibre13"><sup class="calibre23">3</sup>H</strong><sup class="calibre23">2</sup></p>'
>>> soup = BeautifulSoup(html, features = 'lxml')
>>> tag = soup.find('p', attrs={'class':'df'})
>>> print(get_tag_content(tag))
['H', '<strong class="calibre13">H</strong>']

"""
