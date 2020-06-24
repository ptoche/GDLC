""" 
Strip anchor id and href while keeping content. 

>>> from GDLC.GDLC import *
>>> dml = '''\
... <body>
...   <div>
...     <blockquote align="left" id="id9999"><span>Definition here.</span></blockquote>
...     <blockquote align="left"><span>More details here.</span></blockquote>
...     <blockquote align="left"><span>More details and an anchor</a>.</span></blockquote>
...   </div>
...   <div>
...     <blockquote align="left" id=""><span>Definition here.</span></blockquote>
...     <blockquote align="left"><span>More details here.</span></blockquote>
...     <blockquote align="left"><span>More details and an anchor</a>.</span></blockquote>
...   </div>
... </body>'''

# Make an anchor in first <blockquote> tag:
>>> soup = BeautifulSoup(dml, features='lxml')
>>> print(make_anchor(soup, tags=['blockquote']))


"""
