#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created 3 May 2020

@author: patricktoche

Checks the xml file for any syntax errors. For XML schema validation, we use the etree module from the lxml package. We import StringIO from the io package to pass strings as files to etree. 

"""

import os
from lxml import etree
from io import StringIO
#import sys

root = os.path.join(os.path.sep, 'Users', 'PatrickToche', 'KindleDict', 'GDLC-Kindle-Lookup', 'GDLC', 'mobi8', 'OEBPS', 'Text')
filepath = os.path.join(os.path.sep, root, 'part0000.xhtml')

# parse xml
try:
    doc = etree.parse(StringIO(xml_to_check))
    print('XML well formed, syntax ok.')

# check for file IO error
except IOError:
    print('Invalid File')

# check for XML syntax errors
except etree.XMLSyntaxError as err:
    print('XML Syntax Error, see error_syntax.log')
    with open('error_syntax.log', 'w') as error_log_file:
        error_log_file.write(str(err.error_log))
    quit()

except:
    print('Unknown error, exiting.')
    quit()
