""" 
Print the list of files to be copied by default if no file list is supplied.

>>> from GDLC.GDLC import *
>>> from pathlib import Path
>>> dir = Path.home() / 'GDLC/source/GDLC_unpacked'
>>> print(template_copy(dir))
[PosixPath('/Users/patrick/GDLC/source/GDLC_unpacked/mobi7/Images/author_footer.jpeg'), PosixPath('/Users/patrick/GDLC/source/GDLC_unpacked/mobi7/Images/author_image.jpeg'), PosixPath('/Users/patrick/GDLC/source/GDLC_unpacked/mobi7/Images/cover_image.jpeg'), PosixPath('/Users/patrick/GDLC/source/GDLC_unpacked/mobi7/Images/cover_logo.jpeg'), PosixPath('/Users/patrick/GDLC/source/GDLC_unpacked/mobi7/Images/cover_thumb.jpeg'), PosixPath('/Users/patrick/GDLC/source/GDLC_unpacked/mobi8/mimetype'), PosixPath('/Users/patrick/GDLC/source/GDLC_unpacked/mobi8/META-INF/container.xml'), PosixPath('/Users/patrick/GDLC/source/GDLC_unpacked/mobi8/OEBPS/content.opf'), PosixPath('/Users/patrick/GDLC/source/GDLC_unpacked/mobi8/OEBPS/toc.ncx'), PosixPath('/Users/patrick/GDLC/source/GDLC_unpacked/mobi8/OEBPS/Styles/style0001.css'), PosixPath('/Users/patrick/GDLC/source/GDLC_unpacked/mobi8/OEBPS/Styles/style0002.css'), PosixPath('/Users/patrick/GDLC/source/GDLC_unpacked/mobi8/OEBPS/Images/author_footer.jpeg'), PosixPath('/Users/patrick/GDLC/source/GDLC_unpacked/mobi8/OEBPS/Images/author_image.jpeg'), PosixPath('/Users/patrick/GDLC/source/GDLC_unpacked/mobi8/OEBPS/Images/cover_image.jpeg'), PosixPath('/Users/patrick/GDLC/source/GDLC_unpacked/mobi8/OEBPS/Images/cover_logo.jpeg'), PosixPath('/Users/patrick/GDLC/source/GDLC_unpacked/mobi8/OEBPS/Text/cover_page.xhtml')]

"""
