#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created 3 May 2020

@author: patricktoche

Tests for the main function
"""

# Test 1: prototypical case
source = """
<blockquote class="calibre27">
    <p class="rf">-&gt;AAA<sup class="calibre32">1</sup></p>
    <p class="df"><code class="calibre22"><sup class="calibre23">■</sup><strong class="calibre13">AAA -bb</strong></code><sup class="calibre23">1</sup></p>
    <p class="ps">Definition here.</p>
    <p class="p">More details here.</p>
    <p class="p">Even more details here.</p>
  </blockquote>
"""
print(dictionarize(source, verbose=True))

# must work even if class="ps" missing, if class="df" missing, if class="rf" missing


# Test 2: an incomplete definition: missing class="rf"
test = """
  <blockquote class="calibre27">
    <p class="df"><code class="calibre22"><sup class="calibre23">■</sup><strong class="calibre13">AAA -bb</strong></code><sup class="calibre23">1</sup></p>
    <p class="ps">Definition here.</p>
    <p class="p">More details here.</p>
    <p class="p">Even more details here.</p>
  </blockquote>
"""
print(dictionarize(test))


# Test 3: an incomplete definition: missing class="df"
test = """
  <blockquote class="calibre27">
    <p class="rf">-&gt;AAA<sup class="calibre32">1</sup></p>
    <p class="ps">Definition here.</p>
    <p class="p">More details here.</p>
    <p class="p">Even more details here.</p>
  </blockquote>
"""
print(dictionarize(test))


# Test 4: an incomplete definition: missing class="ps" and class="p"
test = """
  <blockquote class="calibre27">
    <p class="rf">-&gt;AAA<sup class="calibre32">1</sup></p>
    <p class="df"><code class="calibre22"><sup class="calibre23">■</sup><strong class="calibre13">AAA -bb</strong></code><sup class="calibre23">1</sup></p>
"""
print(dictionarize(test))


# Test 5: A dictionary entry with weird stuff
test = """
  <blockquote class="calibre27">
    <p class="rf">-&gt;abonar<sup class="calibre32">2</sup></p>

    <p class="df"><code class="calibre22"><sup class="calibre23">■</sup><strong class="calibre13">abonar</strong></code><sup class="calibre23">2</sup></p>

    <p class="ps">Cp. <a class="calibre17" href="part0020.xhtml#d01591">adobar</a> <strong class="calibre13">5</strong></p>

    <p class="ps">[del fr. <em class="calibre24">abonner</em>, íd., der. de <em class="calibre24">bon</em> ‘bo’; 1a FONT: s. XIX]</p>

    <p class="p"><em class="v">v</em> <strong class="n">1</strong> <em class="v">tr</em> Pagar (per altri) l’abonament a una cosa. <em class="ex">Ahir els vam abonar al festival de teatre.</em></p>

    <p class="p"><strong class="n">2</strong> <em class="v">tr</em> <a class="calibre17" href="part0196.xhtml#d62177">pagar</a> <strong class="calibre13">2</strong>.</p>

    <p class="p"><strong class="n">3</strong> <em class="v">tr</em> <span class="v1">COMPT</span> Inscriure en un compte corrent (una partida a favor d’algú); admetre en compte.</p>

    <p class="p"><strong class="n">4</strong> <em class="n1">1</em> <em class="v">pron</em> Prendre un abonament. <em class="ex">Abonar-se al futbol.</em></p>

    <p class="p1"><em class="n1">2</em> <em class="v">pron</em> <em class="v">fig</em> Abusar (d’algú o d’alguna cosa). <em class="ex">T’abones amb ell perquè és petit. Com s’hi abona, amb els pastissets!</em></p>

    <p class="p1"><em class="n1">3</em> <strong class="calibre13">estar abonat</strong> <em class="v">fig</em> Tenir sovint. <em class="ex">Estar abonat al mal de queixal.</em></p>

    <p class="p"><strong class="n">5</strong> <em class="v">tr</em> Tornar uns diners deixats en dipòsit a canvi d’un objecte. <em class="ex">Abonar un envàs.</em></p>

    <p class="tc"><strong class="calibre33">CONJUGACIÓ</strong></p>

    <p class="pc"><strong class="calibre34">INFINITIU:</strong> abonar</p>

    <p class="pc"><strong class="calibre34">GERUNDI:</strong> abonant</p>

    <p class="pc"><strong class="calibre34">PARTICIPI:</strong> abonat, abonada, abonats, abonades</p>

    <p class="pc"><strong class="calibre34">INDICATIU PRESENT:</strong> abono, abones, abona, abonem, aboneu, abonen</p>

    <p class="pc"><strong class="calibre34">INDICATIU IMPERFET:</strong> abonava, abonaves, abonava, abonàvem, abonàveu, abonaven</p>

    <p class="pc"><strong class="calibre34">INDICATIU PASSAT:</strong> aboní, abonares, abonà, abonàrem, abonàreu, abonaren</p>

    <p class="pc"><strong class="calibre34">INDICATIU FUTUR:</strong> abonaré, abonaràs, abonarà, abonarem, abonareu, abonaran</p>

    <p class="pc"><strong class="calibre34">INDICATIU CONDICIONAL:</strong> abonaria, abonaries, abonaria, abonaríem, abonaríeu, abonarien</p>

    <p class="pc"><strong class="calibre34">SUBJUNTIU PRESENT:</strong> aboni, abonis, aboni, abonem, aboneu, abonin</p>

    <p class="pc"><strong class="calibre34">SUBJUNTIU IMPERFET:</strong> abonés, abonessis, abonés, abonéssim, abonéssiu, abonessin</p>

    <p class="pc"><strong class="calibre34">IMPERATIU:</strong> abona, aboni, abonem, aboneu, abonin</p>
  </blockquote>
"""
print(dictionarize(test))


# Test 6: A definition with unnecessary forward slash
test = """
  <blockquote class="calibre27">
    <p class="rf">-&gt;a/</p>

    <p class="df"><code class="calibre22"><strong class="calibre13">a/</strong></code></p>

    <p class="p"><em class="v">abrev</em> <strong class="calibre13">a l’atenció de.</strong></p>
  </blockquote>
"""
print(dictionarize(test, pretty=True))



# Test: Import html file
import os
base = os.path.join(os.path.sep, 'Users', 'PatrickToche', 'KindleDict', 'github','Python','tests')
name0 = 'test4.html'
name1 = 'junk.html'
with open(os.path.join(base, name0)) as infile, open(os.path.join(base, name1), 'w') as outfile:
    soup = BeautifulSoup(infile)
    body = soup.find('body')
    for h in body:
        e = body.find('h2')
        if e:
            outfile.write(str(e))
            e.decompose()
    b = body.findChildren(recursive=False)
    for x in b:
        s = str(dictionarize(str(x)))
        h = '<?xml version="1.0" encoding="utf-8"?>'
        s = s.replace(h, '')
        outfile.write(s)
