""" 
Strip special character '■' and container tag from a BeautifulSoup object:

>>> from GDLC.GDLC import *
>>> ml = '''<p class="df"><code><sup>■</sup><strong>ABC -xy</strong></code><sup>1</sup></p>'''
>>> soup = BeautifulSoup(ml, features='lxml')

>>> print(strip_squares(soup))
<html><body><p class="df"><code><strong>ABC -xy</strong></code><sup>1</sup></p></body></html>

"""
