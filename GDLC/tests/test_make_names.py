""" 
Make a list of files to be processed:
>>> from GDLC.GDLC import *
>>> import os
>>> indir = os.path.join(os.path.sep, 'Users', 'PatrickToche', 'GDLC', 'source', 'GDLC_unpacked', 'mobi8', 'OEBPS', 'Text')
>>> filepath = os.path.join(os.path.sep, indir, 'part0000.xhtml')
>>> filelist = make_names(filepath)
>>> print(filelist[16:17])
['/Users/PatrickToche/GDLC/source/GDLC_unpacked/mobi8/OEBPS/Text/part0016.xhtml']

"""
