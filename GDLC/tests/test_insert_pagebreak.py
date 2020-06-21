""" 
Insert <mbp:pagebreak\> self-closing tag:

>>> from GDLC.GDLC import *
>>> dml = '''<html><body><div>AAA</div><div>BBB</div></body></html>'''
>>> soup = BeautifulSoup(dml, features='lxml')
>>> insert_pagebreak(soup, tag = soup.find('div'))
>>> print(soup)
<html><body><div><mbp:pagebreak/>AAA</div><div>BBB</div></body></html>

"""
