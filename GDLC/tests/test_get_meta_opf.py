""" 
Extract meta information from content.opf and return a dictionary of {tag:content}.

>>> from GDLC.GDLC import *
>>> # from pprint import pprint  # pprint already imported by GDLC.GDLC
>>> dir = Path.home() / 'GDLC/output/GDLC_processed'

Extract the default list of tags:
>>> pprint(get_meta_opf(dir))
{'creator': "Institut d'Estudis Catalans",
 'identifier': 'B00DZWFUG4-LookUp-mobi8',
 'language': 'ca',
 'publisher': 'Gran Enciclopèdia Catalana',
 'title': 'Gran Diccionari de la Llengua Catalana'}

Extract a given list of tags:
>>> pprint(get_meta_opf(dir, tags=['title', 'language']))
{'language': 'ca', 'title': 'Gran Diccionari de la Llengua Catalana'}

Extract a single tag:
>>> pprint(get_meta_opf(dir, tags='title'))
{'title': 'Gran Diccionari de la Llengua Catalana'}

"""
