#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add the GDLC directory to your PYTHONPATH. 

MacOS/Linus: open ~/.bash_profile and add the following:
    export PYTHONPATH="/Users/username/GDLC"
Or if you use Spyder, set it via python -> PYTHONPATH manager

Windows: Computer -> Properties -> Advanced system settings -> Environment variables -> New
Name the new variable PYTHONPATH and set its value to the directory path, e.g. "C:/GDLC" 

Check that your PYTHONPATH has been set properly with:
    import os
    os.environ['PYTHONPATH']

Created 9 May 2020

@author: patricktoche
"""

# Install module from github:
pip install https://github.com/ptoche/GDLC/zipball/master

# or if git is installed on your system:
pip install git+https://github.com/ptoche/GDLC.git#egg=GDLC

"""
# Import the main package `GDLC`:
from GDLC import GDLC  # I can then call `GDLC.tests`
                       # otherwise with a simple `import GDLC`
                       # it's `GDLC.GDLC.tests`

# Explore the package contents:
dir(GDLC)            # lists all available directories
help(GDLC)           # prints package contents
print(GDLC.__doc__)  # prints the package docstrings
                     # worked initially, now returns None.
""" 

## SECTION I: Importing the GDLC package

# 1. Standard import statements: 

# Import the main package `GDLC`:
import GDLC.GDLC

# Import the sub-package `tests`:
import GDLC.tests

# Run GDLC functions:
GDLC.GDLC.replace_strings('abc', 'b')

# Run tests functions:
GDLC.tests.test_examples()


# 2. More convenient alternatives: Use an alias

# Import the main package `GDLC` with an alias:
    # Type g.f() instead of GDLC.GDLC.f()
import GDLC.GDLC as g

# Explore the package contents:
print(g.__doc__)

# Run functions from the main package:
g.replace_strings('abc', 'b')

# Import the sub-package `tests` with an alias:
    # Type t.f() instead of GDLC.tests.tests.f()
import GDLC.tests.tests as t

# Explore the sub-package contents:
print(t.__doc__)

# Run functions from the sub-package:
t.test_examples(verbose=True)


# 3. Another convenient alternative: Import the modules directly from the package

# Import the main package `GDLC` directly:
    # Type GDLC.f() instead of GDLC.GDLC.f()
from GDLC import GDLC

# Explore the main package contents:
print(GDLC.__doc__)
help(GDLC)

# Run functions from the main package:
GDLC.replace_strings('abc', 'b')

# Import the sub-package `tests` directly:
    # Type tests.f() instead of GDLC.tests.tests.f()
from GDLC.tests import tests

# Explore the sub-package contents:
help(tests)

# Run functions from the sub-package:
tests.test_examples(verbose=True)



## SECTION II: Logging runs for debugging

# To log errors, the logs sub-package must be invoked before running code. 
from GDLC.logs.logs import custom_logs
custom_logs()  # configures options for logging and prints the directory where logs will be saved
xml = loop_away(f, outdir)
# To obtain information about the `custom_logs` arguments, type:
help(logs)



## SECTION III: Running tests

from GDLC import GDLC
from GDLC.tests import tests
tests.test_examples(verbose=True)


## SECTION IV: Using the GDLC package to make the dictionary

# Loop
from GDLC.GDLC import *  # lazy and crazy

# Make names and run loop
# source directory with original dictionary files in `mobi8` `xhtml` format:
indir = os.path.join(os.path.sep, 'Users', 'PatrickToche', 'GDLC', 'source', 'GDLC_unpacked', 'mobi8', 'OEBPS', 'Text')
# output directory with processed dictionary files:
outdir = os.path.join(os.path.sep, 'Users', 'PatrickToche', 'GDLC', 'output', 'GDLC_processed', 'mobi8', 'OEBPS', 'Text')
# source file:
filepath = os.path.join(os.path.sep, indir, 'part0000.xhtml')
# make_names(filepath, first = 16, last = 17)

filelist = make_names(filepath)

# test with a smaller subset of files
f = filelist[149:151]
# xml = loop_away(f)  # the default output directory, `outdir` is set to `tmp`
xml = loop_away(f, outdir)

To do: Skip files 000-015 and 276-277
To do: clean up these non-dictionary pages
To do: generate a LookUp mobi file with definitions only + cover