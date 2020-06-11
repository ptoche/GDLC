""" 
Splits dictionary entry into three parts:

>>> from GDLC.GDLC import *
>>> ml = '''
... <blockquote class="calibre27">
... <p class="rf">HEADWORD: SHORT FORM</p>
... <p class="df">HEADWORD: LONG FORM</p>
... <p class="ps">PRIMARY DEFINITION</p>
... <p class="p">SECONDARY DEFINITION</p>
... </blockquote>
... '''
>>> soup = BeautifulSoup(ml, features='lxml')
>>> s1, s2, s3 = split_entry(soup)

The first element of the return tuple, s1, is used to make a label:
>>> print(s1)
<p class="rf">HEADWORD: SHORT FORM</p>

The second element of the return tuple, s2, is used to make a heading:
>>> print(s2)
<p class="df">HEADWORD: LONG FORM</p>

The third element of the return tuple, s3, is used to make a definition
>>> print(s3)
<blockquote class="calibre27">
<p class="ps">PRIMARY DEFINITION</p>
<p class="p">SECONDARY DEFINITION</p>
</blockquote>

"""
