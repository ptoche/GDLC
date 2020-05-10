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

# Import module:
import GDLC

# Check that the module has been imported:
print(g.__doc__)  # prints the module's docstring

# Check what functions are available
import platform
print(dir(GDLC))

# Call the main function on a word:
word_in = """
  <blockquote class="calibre27">
    <p class="rf">-&gt;a<sup class="calibre32">1</sup></p>

    <p class="df"><code class="calibre22"><sup class="calibre23">■</sup><strong class="calibre13">a</strong></code><sup class="calibre23">1</sup></p>

    <p class="ps">Hom.: <strong class="calibre13">ah</strong></p>

    <p class="p">[<em class="v">pl</em> <em class="calibre24">as</em>] <em class="v">f</em> <strong class="n">1</strong> <span class="v1">ESCR</span> Nom de la primera lletra de l’alfabet català, <em class="ex">a A</em>.</p>

    <p class="p"><strong class="n">2</strong> <strong class="calibre13">no saber ni la a</strong> No saber ni els rudiments d’una cosa.</p>
  </blockquote>
"""
word_out = GDLC..dictionarize(word_in, verbose=True, clean=False, features='lxml')
print(word_out)
