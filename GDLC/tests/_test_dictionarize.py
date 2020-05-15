""" 
Dictionarize typical word definitions

Output similar to Real Acadamia Española azw format:
>>> test = '''<blockquote class="calibre27">
    <p class="rf">-&gt;AAA<sup class="calibre32">1</sup></p>
    <p class="df"><code class="calibre22"><sup class="calibre23">■</sup><strong class="calibre13">AAA -bb</strong></code><sup class="calibre23">1</sup></p>
    <p class="ps">Definition here.</p>
    <p class="p">More details here.</p>
    <p class="p">Even more details here.</p>
  </blockquote>'''
>>> print(dictionarize(test))
<idx:entry scriptable="yes">
    <idx:orth value="AAA">
      <idx:infl>
        <idx:iform name="" value="AAA"/>
      </idx:infl>
    </idx:orth>
        <div><span><b>AAA</b></span></div><span><strong class="calibre13">AAA -bb</strong><sup class="calibre23">1</sup>.</span>
    <div>
<blockquote><span>Definition here.</span></blockquote>
<blockquote><span>More details here.</span></blockquote>
<blockquote><span>Even more details here.</span></blockquote>
</div>
</idx:entry>
# 
Output similar to Real Acadamia Española mobi format (class + id suppressed)
>>> print(dictionarize(test, clean=True))
<idx:entry scriptable="yes">
    <idx:orth value="AAA">
      <idx:infl>
        <idx:iform name="" value="AAA"/>
      </idx:infl>
    </idx:orth>
        <div><span><b>AAA</b></span></div><span><strong>AAA -bb</strong><sup>1</sup>.</span>
    <div>
<blockquote align="left"><span>Definition here.</span></blockquote>
<blockquote align="left"><span>More details here.</span></blockquote>
<blockquote align="left"><span>Even more details here.</span></blockquote>
</div>
</idx:entry>
# 
Incomplete definition: missing class="rf"
>>> test = '''<blockquote class="calibre27">
    <p class="df"><code class="calibre22"><sup class="calibre23">■</sup><strong class="calibre13">AAA -bb</strong></code><sup class="calibre23">1</sup></p>
    <p class="ps">Definition here.</p>
    <p class="p">More details here.</p>
    <p class="p">Even more details here.</p>
  </blockquote>'''
>>> print(dictionarize(test))

# 
Incomplete definition: missing class="df"
>>> test = '''<blockquote class="calibre27">
    <p class="rf">-&gt;AAA<sup class="calibre32">1</sup></p>
    <p class="ps">Definition here.</p>
    <p class="p">More details here.</p>
    <p class="p">Even more details here.</p>
  </blockquote>'''
>>> print(dictionarize(test))

# 
Incomplete definition: missing class="ps" and class="p"
>>> test = '''<blockquote class="calibre27">
    <p class="rf">-&gt;AAA<sup class="calibre32">1</sup></p>
    <p class="df"><code class="calibre22"><sup class="calibre23">■</sup><strong class="calibre13">AAA -bb</strong></code><sup class="calibre23">1</sup></p>'''
>>> print(dictionarize(test))
<idx:entry scriptable="yes">
    <idx:orth value="AAA">
      <idx:infl>
        <idx:iform name="" value="AAA"/>
      </idx:infl>
    </idx:orth>
        <div><span><b>AAA</b></span></div><span><strong class="calibre13">AAA -bb</strong><sup class="calibre23">1</sup>.</span>
    <div>
</div>
</idx:entry>
# 
Definition with unnecessary forward slash: 
>>> test = '''<blockquote class="calibre27">
    <p class="rf">-&gt;a/</p>
    <p class="df"><code class="calibre22"><strong class="calibre13">a/</strong></code></p>
    <p class="p"><em class="v">abrev</em> <strong class="calibre13">a l’atenció de.</strong></p>
  </blockquote>'''
>>> print(dictionarize(test))
<idx:entry scriptable="yes">
    <idx:orth value="a/">
      <idx:infl>
        <idx:iform name="" value="a/"/>
      </idx:infl>
    </idx:orth>
        <div><span><b>a/</b></span></div><span><strong class="calibre13">a/</strong>.</span>
    <div>
<blockquote><span><em class="v">abrev</em> <strong class="calibre13">a l’atenció de.</strong></span></blockquote>
</div>
</idx:entry>
#
A long dictionary entry:
>>> test = '''<blockquote class="calibre27">
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
  </blockquote>'''
>>> print(dictionarize(test, clean=True))
<idx:entry scriptable="yes">
    <idx:orth value="abonar">
      <idx:infl>
        <idx:iform name="" value="abonar"/>
      </idx:infl>
    </idx:orth>
        <div><span><b>abonar</b></span></div><span><strong>abonar</strong><sup>2</sup>.</span>
    <div>
<blockquote align="left"><span>Cp. adobar <strong>5</strong></span></blockquote>
<blockquote align="left"><span>[del fr. <em>abonner</em>, íd., der. de <em>bon</em> ‘bo’; 1a FONT: s. XIX]</span></blockquote>
<blockquote align="left"><span><em>v</em> <strong>1</strong> <em>tr</em> Pagar (per altri) l’abonament a una cosa. <em>Ahir els vam abonar al festival de teatre.</em></span></blockquote>
<blockquote align="left"><span><strong>2</strong> <em>tr</em> pagar <strong>2</strong>.</span></blockquote>
<blockquote align="left"><span><strong>3</strong> <em>tr</em> <span>COMPT</span> Inscriure en un compte corrent (una partida a favor d’algú); admetre en compte.</span></blockquote>
<blockquote align="left"><span><strong>4</strong> <em>1</em> <em>pron</em> Prendre un abonament. <em>Abonar-se al futbol.</em></span></blockquote>
<blockquote align="left"><span><em>2</em> <em>pron</em> <em>fig</em> Abusar (d’algú o d’alguna cosa). <em>T’abones amb ell perquè és petit. Com s’hi abona, amb els pastissets!</em></span></blockquote>
<blockquote align="left"><span><em>3</em> <strong>estar abonat</strong> <em>fig</em> Tenir sovint. <em>Estar abonat al mal de queixal.</em></span></blockquote>
<blockquote align="left"><span><strong>5</strong> <em>tr</em> Tornar uns diners deixats en dipòsit a canvi d’un objecte. <em>Abonar un envàs.</em></span></blockquote>
<blockquote align="left"><span><strong>CONJUGACIÓ</strong></span></blockquote>
<blockquote align="left"><span><strong>INFINITIU:</strong> abonar</span></blockquote>
<blockquote align="left"><span><strong>GERUNDI:</strong> abonant</span></blockquote>
<blockquote align="left"><span><strong>PARTICIPI:</strong> abonat, abonada, abonats, abonades</span></blockquote>
<blockquote align="left"><span><strong>INDICATIU PRESENT:</strong> abono, abones, abona, abonem, aboneu, abonen</span></blockquote>
<blockquote align="left"><span><strong>INDICATIU IMPERFET:</strong> abonava, abonaves, abonava, abonàvem, abonàveu, abonaven</span></blockquote>
<blockquote align="left"><span><strong>INDICATIU PASSAT:</strong> aboní, abonares, abonà, abonàrem, abonàreu, abonaren</span></blockquote>
<blockquote align="left"><span><strong>INDICATIU FUTUR:</strong> abonaré, abonaràs, abonarà, abonarem, abonareu, abonaran</span></blockquote>
<blockquote align="left"><span><strong>INDICATIU CONDICIONAL:</strong> abonaria, abonaries, abonaria, abonaríem, abonaríeu, abonarien</span></blockquote>
<blockquote align="left"><span><strong>SUBJUNTIU PRESENT:</strong> aboni, abonis, aboni, abonem, aboneu, abonin</span></blockquote>
<blockquote align="left"><span><strong>SUBJUNTIU IMPERFET:</strong> abonés, abonessis, abonés, abonéssim, abonéssiu, abonessin</span></blockquote>
<blockquote align="left"><span><strong>IMPERATIU:</strong> abona, aboni, abonem, aboneu, abonin</span></blockquote>
</div>
</idx:entry>
"""

