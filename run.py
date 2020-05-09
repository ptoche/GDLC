#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created 3 May 2020

@author: patricktoche

"""

# Import module
import GDLC

# If the module is not on the Python path, locate its path, e.g.
import os, sys
# sys.path.append('/usr/sammy/')
os.path.join(os.path.sep, os.getcwd(),  'GDLC')

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
word_out = dictionarize(word_in, verbose=True, clean=False, parser='html.parser')
print(word_out)
