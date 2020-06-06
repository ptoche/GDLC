""" Test: Import html file and save to file
first version used for loop_away(): kept for reference only
""" 

import os
indir = os.path.join(os.path.sep, os.getcwd(), 'GDLC', 'tests')
outdir = os.path.join(os.path.sep, os.getcwd(), 'GDLC', 'tmp')
name0 = 'test4.html'
name1 = 'junk.html'
with open(os.path.join(indir, name0)) as infile, open(os.path.join(indir, name1), 'w') as outfile:
    soup = BeautifulSoup(infile, features='xml')
    body = soup.find('body')
    for h in body:
        e = body.find('h2')
        if e:
            outfile.write(str(e))
            e.decompose()
    b = body.findChildren(recursive=False)
    for x in b:
        s = str(make_entry(str(x)))
        h = '<?xml version="1.0" encoding="utf-8"?>'
        s = s.replace(h, '')
        outfile.write(s)
