""" 
Insert <mbp:frameset> tags just after <body>:

>>> from GDLC.GDLC import *
>>> dml = '''<html><body><div>AAA</div><div>BBB</div></body></html>'''
>>> soup = BeautifulSoup(dml, features='lxml')
>>> insert_frameset(soup)
>>> print(soup)
<html><mbp:frameset><body><div>AAA</div><div>BBB</div></body></mbp:frameset></html>

"""
