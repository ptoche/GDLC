""" 
Copy the directory tree from a directory.

>>> from GDLC.GDLC import *

>>> indir = os.path.join(os.path.sep, 'Users', 'PatrickToche', 'GDLC', 'source', 'GDLC_unpacked')
>>> outdir = os.path.join(os.path.sep, 'Users', 'PatrickToche', 'GDLC', 'tmp', 'dirtree_test')
>>> print(copy_dirtree(indir, outdir))
Directory
 /Users/PatrickToche/GDLC/tmp/dirtree_test/mobi8 
 was copied to destination

Directory
 /Users/PatrickToche/GDLC/tmp/dirtree_test/mobi7 
 was copied to destination

Directory
 /Users/PatrickToche/GDLC/tmp/dirtree_test/HDImages 
 was copied to destination

Directory
 /Users/PatrickToche/GDLC/tmp/dirtree_test/mobi8/META-INF 
 was copied to destination

Directory
 /Users/PatrickToche/GDLC/tmp/dirtree_test/mobi8/OEBPS 
 was copied to destination

Directory
 /Users/PatrickToche/GDLC/tmp/dirtree_test/mobi8/OEBPS/Images 
 was copied to destination

Directory
 /Users/PatrickToche/GDLC/tmp/dirtree_test/mobi8/OEBPS/Styles 
 was copied to destination

Directory
 /Users/PatrickToche/GDLC/tmp/dirtree_test/mobi8/OEBPS/Text 
 was copied to destination

Directory
 /Users/PatrickToche/GDLC/tmp/dirtree_test/mobi8/OEBPS/Fonts 
 was copied to destination

Directory
 /Users/PatrickToche/GDLC/tmp/dirtree_test/mobi7/Images 
 was copied to destination

['/Users/PatrickToche/GDLC/source/GDLC_unpacked', '/Users/PatrickToche/GDLC/tmp/dirtree_test']

"""
