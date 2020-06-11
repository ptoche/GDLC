""" 
List files in a given directory:

>>> from GDLC.GDLC import *
>>> root = os.path.join(os.path.sep, 'Users', 'PatrickToche', 'GDLC', 'source', 'GDLC_unpacked', 'mobi8', 'OEBPS', 'Styles')
>>> ignore_list = ['style0003.css', 'style0004.css']

>>> list_files_ignore(ignore_list, dir=root)
['/Users/PatrickToche/GDLC/source/GDLC_unpacked/mobi8/OEBPS/Styles/style0003.css']

"""
