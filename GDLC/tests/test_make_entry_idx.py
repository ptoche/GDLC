""" 
Make an idx entry for an epub/mobi dictionary.

>>> from GDLC.GDLC import *
>>> print(make_entry_idx())
<idx:entry name="Catalan" scriptable="yes" spell="yes" id="">

>>> print(make_entry_idx(name="Singlish", scriptable="nope", spell="nein", id=999))
<idx:entry name="Singlish" scriptable="nope" spell="nein" id="999">

"""

