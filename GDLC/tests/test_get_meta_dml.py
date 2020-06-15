""" 
Extract meta information from dml files and return a dictionary of {tag:content}.

>>> from GDLC.GDLC import *
>>> # from pprint import pprint  # pprint already imported by GDLC.GDLC
>>> dir = Path.home() / 'GDLC/output/GDLC_processed/mobi8/OEBPS/Text'
>>> with open(file, encoding='utf8') as infile:
>>>     soup = BeautifulSoup(infile, features='lxml')

Extract the default list of tags:
>>> pprint(get_meta_dml(dir))


Extract a given list of tags:
>>> pprint(get_meta_dml(dir, tags=['title', 'language']))


Extract a single tag:
>>> pprint(get_meta_dml(dir, tags='title'))


"""
