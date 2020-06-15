""" 
Test `dir_handler()`: set given directory or set default directory and/or create directory.

>>> from GDLC.GDLC import *
>>> dir_handler()
Aborting. No directory given. To create a directory, set `mkdir=True`.

>>> dir_handler('~/tmp')
PosixPath('/Users/patricktoche/tmp')

>>> dir_handler('~/tmp/tmp', mkdir=False)
Aborting. No directory found at destination. The specified dir argument must be a valid directory. To create the directory, set `mkdir=True`.

Example of usage: `copy_files(dir="~/tmp", mkdir=True)`

>>> dir_handler('~/tmp/tmp', mkdir=True)
PosixPath('/Users/patricktoche/tmp/tmp')

"""
