""" 
Get content from tag. 

>>> from GDLC.GDLC import *
>>> dml = '''\
... <idx:entry scriptable="yes">
...   <idx:orth value="ABC">
...     <idx:infl>
...       <idx:iform name="" value="ABC"/>
...     </idx:infl>
...   </idx:orth>
...     <div>
...       <span>
...         <b>ABC</b>
...       </span>
...     </div>
...     <span>
...       <strong>ABC -xy</strong><sup class="calibre23">1</sup>.
...     </span>
...     <div>
...       <blockquote align="left"><span>Definition here.</span></blockquote>
...       </blockquote align="left"><span>More details here.</span></blockquote>
...       </blockquote align="left"><span>Even more details here.</span></blockquote>
...     </div>
... </idx:entry>'''
>>> soup = BeautifulSoup(dml, features='lxml')

>>> print(get_content(soup, tag='idx:entry'))
{'idx:entry': ['\n', <idx:orth value="ABC">
<idx:infl>
<idx:iform name="" value="ABC"></idx:iform>
</idx:infl>
</idx:orth>, '\n', <div>
<span>
<b>ABC</b>
</span>
</div>, '\n', <span>
<strong>ABC -xy</strong><sup class="calibre23">1</sup>.
    </span>, '\n', <div>
<blockquote align="left"><span>Definition here.</span></blockquote>
<span>More details here.</span>
<span>Even more details here.</span>
</div>, '\n']}

"""
