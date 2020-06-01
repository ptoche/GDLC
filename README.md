## WARNING!

MAY 2020: WORK IN PROGRESS. UNTESTED. VERY PRELIMINARY.

The code has not been optimized and was written over two days without prior thoughts, refactored for another two days, polished a little in my spare time. The code relies on the BeautifulSoup library, a library I had never used before... 

## Overview

Python code to edit an ebook dictionary into a Kindle lookup dictionary that may be associated with the Catalan language. The source files may then be used to rebuild a dictionary. 

**Reader:** _Kindle Paperwhite 2018_ aka Paperwhite 4 (Lookup dictionaries are not supported by all Kindles).

**Source:** _Gran Diccionari de la llengua catalana (Kindle Edition)_. Available for purchase at https://www.amazon.com/Gran-Diccionari-Llengua-Catalana-Catalan-ebook/dp/B00DZWFUG4/ for less than 10 U.S. dollars. A free sample may be requested from amazon. This ebook does not support lookup (it is not listed as a dictionary under the Catalan language). The source was purchased in April 2020 and delivered in mobi format. The mobi file was converted to the azw format with calibre (https://calibre-ebook.com/). The azw file was broken into several components using the KindleUnpack plugin (https://wiki.mobileread.com/wiki/KindleUnpack).  

**Software:**  

* Python is free sofware available for most operating systems: https://www.python.org/download/releases/3.0/. 

* BeautifulSoup is a free Python library: https://pypi.org/project/beautifulsoup4/

* KindleGen is free software freely provided by Amazon: https://www.amazon.com/gp/feature.html?ie=UTF8&docId=1000765211. 

## Installation

You must be able to run Python 3 code and the BeautifulSoup library. As the files to be processed are large and the content proprietary, online emulators may not be the appropriate tool. You must have a copy of the dictionary. A free sample may be found inside the GDLC directory. 

Python: Make sure you have the appropriate parser libraries installed, e.g. the lxml parser. Examples:
    pip install lxml                 # general purpose package manager 
    brew install html.parser  # popular for MacOS
    conda install html5lib     # Anaconda environment manager

## Getting Help

File an issue and let's see if I can help. Let me know if you can contribute. Do you already have a Catalan Lookup dictionary? Let me know! You're looking for one? Let me know. 

## History

My original plan was to make a lookup dictionary for Aranes and Occitan. I started with Catalan because I happen to own an electronic copy of the dictionary. 

Suggestions for improvement welcome!

@author: Patrick Toche. 
