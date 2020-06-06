""" 
Turn a mobi dictionary entry into a lookup dictionary entry.

Typical structure of a dictionary entry:
>>> from GDLC.GDLC import *
>>> html = '''
... <?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml">
... <head>
... <title>Unknown</title>
... <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
... <link href="../Styles/style0001.css" rel="stylesheet" type="text/css"/>
... <link href="../Styles/style0002.css" rel="stylesheet" type="text/css"/>
... </head>
... <body>
... <blockquote class="calibre27">
... <p class="rf">-&gt;AAA<sup class="calibre32">1</sup></p>
... <p class="df"><code class="calibre22"><sup class="calibre23">■</sup><strong class="calibre13">AAA -bb</strong></code><sup class="calibre23">1</sup></p>
... <p class="ps">Definition here.</p>
... <p class="p">More details here.</p>
... <p class="p">Even more details here.</p>
... </blockquote>
... </body>
... </html>
... '''

>>> print(make_entry(html))
<idx:entry scriptable="yes">
<idx:orth value="<p class="rf">AAA<sup class="calibre32">1</sup></p>">
      <idx:infl>
        <idx:iform name="" value="<p class="rf">AAA<sup class="calibre32">1</sup></p>"/>
      </idx:infl>
    </idx:orth><div><span><b>AAA</b></span></div><span><strong class="calibre13">AAA -bb</strong>.</span><div><blockquote class="calibre27">
<blockquote><span>Definition here.</span></blockquote>
<blockquote><span>More details here.</span></blockquote>
<blockquote><span>Even more details here.</span></blockquote>
</blockquote></div>
</idx:entry>

"""

