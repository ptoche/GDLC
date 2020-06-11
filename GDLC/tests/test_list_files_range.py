""" 
Make a list of files to be processed:

>>> from GDLC.GDLC import *
>>> import os
>>> indir = os.path.join(os.path.sep, 'Users', 'PatrickToche', 'GDLC', 'source', 'GDLC_unpacked', 'mobi8', 'OEBPS', 'Text')
>>> filename = os.path.join(os.path.sep, indir, 'part0000.xhtml')
>>> filelist = list_files_range(filename)

>>> filelist[16:17]
['/Users/PatrickToche/GDLC/source/GDLC_unpacked/mobi8/OEBPS/Text/part0016.xhtml']

"""
