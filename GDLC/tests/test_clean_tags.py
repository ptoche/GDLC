""" 
Remove certain tags from BeautifulSoup object:

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

>>> soup = BeautifulSoup(html, features='lxml')
>>> print(clean_tags(soup)) 
<?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Unknown</title>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
<link href="../Styles/style0001.css" rel="stylesheet" type="text/css"/>
<link href="../Styles/style0002.css" rel="stylesheet" type="text/css"/>
</head>
<body>
<blockquote class="calibre27">
<p class="rf">-&gt;AAA<sup>1</sup></p>
<p class="df"><code class="calibre22"><sup>■</sup><strong>AAA -bb</strong></code><sup>1</sup></p>
<p class="ps">Definition here.</p>
<p class="p">More details here.</p>
<p class="p">Even more details here.</p>
</blockquote>
</body>
</html>

"""
