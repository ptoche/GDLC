""" 
Test `copy_files()`: copies files from source to destination.

>>> from GDLC.GDLC import *
>>> files = ['~/GDLC/source/GDLC_unpacked/mobi8/META-INF/container.xml', '~/GDLC/source/GDLC_unpacked/mobi8/OEBPS/content.opf']

# Copy a list of files to the default directory:
>>> copy_files(files=files)
The following files are being copied:


 /Users/patricktoche/GDLC/source/GDLC_unpacked/mobi8/META-INF/container.xml 

 copied to:

 /Users/patricktoche/tmp/container.xml 


 /Users/patricktoche/GDLC/source/GDLC_unpacked/mobi8/OEBPS/content.opf 

 copied to:

 /Users/patricktoche/tmp/content.opf 

# Copy a list of files to a specified directory:
>>> copy_files(files=files, dir='~/tmp/tmp')
The following files are being copied:


 /Users/patricktoche/GDLC/source/GDLC_unpacked/mobi8/META-INF/container.xml 

 copied to:

 /Users/patricktoche/tmp/tmp/container.xml 


 /Users/patricktoche/GDLC/source/GDLC_unpacked/mobi8/OEBPS/content.opf 

 copied to:

 /Users/patricktoche/tmp/tmp/content.opf 

# Attempt to copy non-existent file:
>>> copy_files(files=['~/tmp/bananas.txt'])
The following files are being copied:

The following file was not found:

 /Users/patricktoche/tmp/bananas.txt 

type error: [Errno 2] No such file or directory: '/Users/patricktoche/tmp/bananas.txt'

# Attempt to copy to non-existent directory:
>>> copy_files(dir ='~/bananas')
Aborting. The specified dir argument must be a valid directory.
Example of usage: `copy_files(dir = "~/tmp")`
If the directory does not exist, it will be created if `mkdir=True`.

"""
