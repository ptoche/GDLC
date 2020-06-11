""" 
# TO DO: Experiment with different parsers

# Output similar to Real Acadamia Española azw format:
>>> test = '''<blockquote class="calibre27">
    <p class="rf">-&gt;ABC<sup class="calibre32">1</sup></p>
    <p class="df"><code class="calibre22"><sup class="calibre23">■</sup><strong class="calibre13">ABC -xy</strong></code><sup class="calibre23">1</sup></p>
    <p class="ps">Definition here.</p>
    <p class="p">More details here.</p>
    <p class="p">Even more details here.</p>
  </blockquote>'''
# 
# Using parser 'html.parser' 
>>> print(make_entry(test, clean=True, features='html.parser'))
<idx:entry scriptable="yes">
    <idx:orth value="ABC">
      <idx:infl>
        <idx:iform name="" value="ABC"/>
      </idx:infl>
    </idx:orth>
        <div><span><b>ABC</b></span></div><span><strong>ABC -xy</strong><sup>1</sup>.</span>
    <div>
<blockquote align="left"><span>Definition here.</span></blockquote>
<blockquote align="left"><span>More details here.</span></blockquote>
<blockquote align="left"><span>Even more details here.</span></blockquote>
</div>
</idx:entry>
# 
# Using parser 'lxml'
>>> print(make_entry(test, clean=True,, features='lxml'))
<idx:entry scriptable="yes">
    <idx:orth value="ABC">
      <idx:infl>
        <idx:iform name="" value="ABC"/>
      </idx:infl>
    </idx:orth>
        <div><span><b>ABC</b></span></div><span><strong>ABC -xy</strong><sup>1</sup>.</span>
    <div>
<blockquote align="left"><span>Definition here.</span></blockquote>
<blockquote align="left"><span>More details here.</span></blockquote>
<blockquote align="left"><span>Even more details here.</span></blockquote>
</div>
</idx:entry>
# 
# Using parser 'html5lib'
>>> print(make_entry(test, clean=True,, features='html5lib'))
<idx:entry scriptable="yes">
    <idx:orth value="ABC">
      <idx:infl>
        <idx:iform name="" value="ABC"/>
      </idx:infl>
    </idx:orth>
        <div><span><b>ABC</b></span></div><span><strong>ABC -xy</strong><sup>1</sup>.</span>
    <div>
<blockquote align="left"><span>Definition here.</span></blockquote>
<blockquote align="left"><span>More details here.</span></blockquote>
<blockquote align="left"><span>Even more details here.</span></blockquote>
</div>
</idx:entry>
"""

