""" 
List files in a given directory:

>>> from GDLC.GDLC import *
>>> root = os.path.join(os.path.sep, 'Users', 'PatrickToche', 'GDLC', 'source', 'GDLC_unpacked', 'mobi8', 'OEBPS', 'Styles')

>>> pprint(list_files_all(root))
['/Users/PatrickToche/GDLC/source/GDLC_unpacked/mobi8/OEBPS/Styles/.DS_Store',
 '/Users/PatrickToche/GDLC/source/GDLC_unpacked/mobi8/OEBPS/Styles/style0001.css',
 '/Users/PatrickToche/GDLC/source/GDLC_unpacked/mobi8/OEBPS/Styles/style0002.css',
 '/Users/PatrickToche/GDLC/source/GDLC_unpacked/mobi8/OEBPS/Styles/style0003.css']

"""
