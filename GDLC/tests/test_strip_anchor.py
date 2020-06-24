""" 
Strip anchor id and href while keeping content. 

>>> from GDLC.GDLC import *
>>> dml = '''\
... <body>
...   <div>
...     <blockquote align="left" id="id0001"><span>Definition here.</span></blockquote>
...     <blockquote align="left"><span>More details here.</span></blockquote>
...     <blockquote align="left"><span>More details and an <a class="calibre17" href="part1234.xhtml#id1234">anchor</a>.</span></blockquote>
...   </div>
...   <div>
...     <blockquote align="left" id="id1234"><span>Definition here.</span></blockquote>
...     <blockquote align="left"><span>More details here.</span></blockquote>
...     <blockquote align="left"><span>More details and an <a class="calibre17" href="part0001.xhtml#id0001">anchor</a>.</span></blockquote>
...   </div>
... </body>'''

Strip the anchor in id:
>>> soup = BeautifulSoup(dml, features='lxml')
>>> print(strip_anchor_from_id(soup.body))
<body>
<div>
<blockquote align="left"><span>Definition here.</span></blockquote>
<blockquote align="left"><span>More details here.</span></blockquote>
<blockquote align="left"><span>More details and an <a class="calibre17" href="part1234.xhtml#id1234">anchor</a>.</span></blockquote>
</div>
<div>
<blockquote align="left"><span>Definition here.</span></blockquote>
<blockquote align="left"><span>More details here.</span></blockquote>
<blockquote align="left"><span>More details and an <a class="calibre17" href="part0001.xhtml#id0001">anchor</a>.</span></blockquote>
</div>
</body>

Strip the anchor in href:
>>> soup = BeautifulSoup(dml, features='lxml')
>>> print(strip_anchor_from_href(soup.body))
<body>
<div>
<blockquote align="left" id="id0001"><span>Definition here.</span></blockquote>
<blockquote align="left"><span>More details here.</span></blockquote>
<blockquote align="left"><span>More details and an anchor.</span></blockquote>
</div>
<div>
<blockquote align="left" id="id1234"><span>Definition here.</span></blockquote>
<blockquote align="left"><span>More details here.</span></blockquote>
<blockquote align="left"><span>More details and an anchor.</span></blockquote>
</div>
</body>

Strip the anchor in both id and href:
>>> soup = BeautifulSoup(dml, features='lxml')
>>> print(strip_anchor(soup.body))
<body>
<div>
<blockquote align="left"><span>Definition here.</span></blockquote>
<blockquote align="left"><span>More details here.</span></blockquote>
<blockquote align="left"><span>More details and an anchor.</span></blockquote>
</div>
<div>
<blockquote align="left"><span>Definition here.</span></blockquote>
<blockquote align="left"><span>More details here.</span></blockquote>
<blockquote align="left"><span>More details and an anchor.</span></blockquote>
</div>
</body>

"""
