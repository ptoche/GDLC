""" 
Strip given tag attributes from a BeautifulSoup object:

>>> from GDLC.GDLC import *
>>> ml = '''<?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml">
... <head>
... <title>Unknown</title>
... <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
... <link href="../Styles/style0001.css" rel="stylesheet" type="text/css"/>
... <link href="../Styles/style0002.css" rel="stylesheet" type="text/css"/>
... </head>
... <body>
... <blockquote class="calibre27" id="d34421">
... <p class="rf">-&gt;ABC<sup class="calibre32">1</sup></p>
... <p class="df"><code class="calibre22"><sup class="calibre23">■</sup><strong class="calibre13">ABC -xy</strong></code><sup class="calibre23">1</sup></p>
... <p class="ps">Definition <em class="calibre24">here</em>.</p>
... <p class="p">More details <span class="v1">here</span>.</p>
... <p class="p">Even more details <a class="calibre17" href="part0120.xhtml#d34479">here</a>.</p>
... </blockquote>
... </body>
... </html>'''
>>> soup = BeautifulSoup(ml, features='lxml')

>>> print(strip_attrs(soup, 'class', 'id'))
<?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Unknown</title>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
<link href="../Styles/style0001.css" rel="stylesheet" type="text/css"/>
<link href="../Styles/style0002.css" rel="stylesheet" type="text/css"/>
</head>
<body>
<blockquote>
<p>-&gt;ABC<sup>1</sup></p>
<p><code><sup>■</sup><strong>ABC -xy</strong></code><sup>1</sup></p>
<p>Definition <em>here</em>.</p>
<p>More details <span>here</span>.</p>
<p>Even more details <a href="part0120.xhtml#d34479">here</a>.</p>
</blockquote>
</body>
</html>

"""
