""" 
Makes a list of the files to be copied from source to destination.

Notes: Couldn't make this doctest work, so useful only as a visual test.

>>> from GDLC.GDLC import *

# Copy a list of files to the default directory:
>>> default_copy(dir='~/GDLC/source/GDLC_unpacked') # doctest:+ELLIPSIS
[PosixPath('.../mobi7/Images/author_footer.jpeg'),
 PosixPath('.../mobi7/Images/author_image.jpeg'),
 PosixPath('.../mobi7/Images/cover_image.jpeg'),
 PosixPath('.../mobi7/Images/cover_logo.jpeg'),
 PosixPath('.../mobi7/Images/cover_thumb.jpeg'),
 PosixPath('.../mobi8/mimetype'),
 PosixPath('.../mobi8/META-INF/container.xml'),
 PosixPath('.../mobi8/OEBPS/content.opf'),
 PosixPath('.../mobi8/OEBPS/toc.ncx'),
 PosixPath('.../mobi8/OEBPS/Styles/style0001.css'),
 PosixPath('.../mobi8/OEBPS/Styles/style0002.css'),
 PosixPath('.../mobi8/OEBPS/Styles/style0003.css'),
 PosixPath('.../mobi8/OEBPS/Images/author_footer.jpeg'),
 PosixPath('.../mobi8/OEBPS/Images/author_image.jpeg'),
 PosixPath('.../mobi8/OEBPS/Images/cover_image.jpeg'),
 PosixPath('.../mobi8/OEBPS/Images/cover_logo.jpeg'),
 PosixPath('.../mobi8/OEBPS/Text/cover_page.xhtml')]

"""
