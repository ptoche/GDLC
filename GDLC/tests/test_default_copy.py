""" 
Print the list of files to be copied by default if no file list is supplied.

>>> from GDLC.GDLC import *
>>> from pathlib import Path
>>> dir = Path.home() / 'GDLC/source/GDLC_unpacked'
>>> print(default_copy(dir))
[PosixPath('/Users/patricktoche/GDLC/source/GDLC_unpacked/mobi7/Images/author_footer.jpeg'), PosixPath('/Users/patricktoche/GDLC/source/GDLC_unpacked/mobi7/Images/author_image.jpeg'), PosixPath('/Users/patricktoche/GDLC/source/GDLC_unpacked/mobi7/Images/cover_image.jpeg'), PosixPath('/Users/patricktoche/GDLC/source/GDLC_unpacked/mobi7/Images/cover_logo.jpeg'), PosixPath('/Users/patricktoche/GDLC/source/GDLC_unpacked/mobi7/Images/cover_thumb.jpeg'), PosixPath('/Users/patricktoche/GDLC/source/GDLC_unpacked/mobi8/mimetype'), PosixPath('/Users/patricktoche/GDLC/source/GDLC_unpacked/mobi8/META-INF/container.xml'), PosixPath('/Users/patricktoche/GDLC/source/GDLC_unpacked/mobi8/OEBPS/content.opf'), PosixPath('/Users/patricktoche/GDLC/source/GDLC_unpacked/mobi8/OEBPS/toc.ncx'), PosixPath('/Users/patricktoche/GDLC/source/GDLC_unpacked/mobi8/OEBPS/Styles/style0001.css'), PosixPath('/Users/patricktoche/GDLC/source/GDLC_unpacked/mobi8/OEBPS/Styles/style0002.css'), PosixPath('/Users/patricktoche/GDLC/source/GDLC_unpacked/mobi8/OEBPS/Styles/style0003.css'), PosixPath('/Users/patricktoche/GDLC/source/GDLC_unpacked/mobi8/OEBPS/Images/author_footer.jpeg'), PosixPath('/Users/patricktoche/GDLC/source/GDLC_unpacked/mobi8/OEBPS/Images/author_image.jpeg'), PosixPath('/Users/patricktoche/GDLC/source/GDLC_unpacked/mobi8/OEBPS/Images/cover_image.jpeg'), PosixPath('/Users/patricktoche/GDLC/source/GDLC_unpacked/mobi8/OEBPS/Images/cover_logo.jpeg'), PosixPath('/Users/patricktoche/GDLC/source/GDLC_unpacked/mobi8/OEBPS/Text/cover_page.xhtml')]

"""
