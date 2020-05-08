#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created 3 May 2020

@author: patricktoche

Calls the function stored in 'main.py' to loop over several files.
Make sure you have the appropriate parser libraries installed, e.g.
    pip install lxml        # for general purpose package manager and lxml parser
    conda install html5lib  # for Anaconda environment manager and html5 parser
"""

# Step 1: List files to be processed
def make_names(filepath, first=None, last=None):
    path = os.path.dirname(filepath)
    name = os.path.basename(filepath)
    base, ext = os.path.splitext(name)
    part = re.split(r'(\d+)', base)[0]
    init = int(re.split(r'(\d+)', base)[1])
    if first is not None:
        init = first
    else:
        init = 0
    i = init
    r = []
    def new_name(i):
        nn = os.path.join(path, part) + str(i).zfill(4) + ext
        return nn
    n = new_name(i)
    if last is not None:
        while i < (last+1):
            i += 1
            r.append(n)
            n = new_name(i)
    else:
        while os.path.exists(n):
            i += 1
            r.append(n)
            n = new_name(i)
    return r



# Step 2: Loop away
def loop_away(filelist, outdir, verbose=False, clean=False, parser='xml'):
    print('To Do: check if all definitions are in blockquote with class calibre27')
    print('To Do: Make list of children to print')
    print('To Do: Test find_all instead of findChildren')
    print('To Do: Test body.descendants instead of children\n')
    print('PROCESSING')
    for file in filelist:
        filename = os.path.basename(file)
        outpath = os.path.join(outdir, filename)
        # hard-coded names and classes of tags that contain definitions:
        names = ['blockquote']
        classes = ['calibre27']
        # get the header from the source file
        with open(file, encoding='utf8') as infile:
            head = get_head(infile, parser=parser)
        # get the body from the source file and make it into dictionary
        with open(file) as infile, open(outpath, 'w') as outfile:
            soup = BeautifulSoup(infile, parser=parser)
            body = soup.find('body')
            for child in body.findChildren(recursive=False):
                print('■', end='', flush=True)
                if verbose:
                    print_child_info(child)
                # selected tags are printed as is
                if child.name in ['h1', 'h2', 'h3', '\n', 'link', 'table']:
                    print(child, file=outfile)
                # tags that contain dictionary definitions are processed
                elif child.name in names and any(c in child['class'] for c in classes):
                    #print('debug: check this blockquote child:', child)
                    s = str(child)
                    s = dictionarize(s, verbose=verbose, clean=clean, parser=parser)
                    print(s, file=outfile)
                else:
                    if verbose:
                        print('This child was removed:\n', child)
                    child.extract()
                    print('End.')
        # get the body from the target file and insert it into the head
        with open(outpath, 'r+') as outfile:
            body = outfile.read()
            html = make_html(body=body, head=head, parser=parser)
            outfile.seek(0)
            outfile.write(html)
            outfile.truncate()
    print('\nDONE.')
    return html




# Make names and run loop
indir = os.path.join(os.path.sep, 'Users', 'PatrickToche', 'KindleDict', 'GDLC-Kindle-Lookup', 'GDLC', 'mobi8', 'OEBPS', 'Text')
outdir = os.path.join(os.path.sep, 'Users', 'PatrickToche', 'KindleDict', 'GDLC-Kindle-Lookup', 'Python', 'output')
filepath = os.path.join(os.path.sep, indir, 'part0000.xhtml')
make_names(filepath, last = 4)
make_names(filepath, first = 2, last = 4)
make_names(filepath, first = 275)
filelist = make_names(filepath)
f = filelist[16:17]
xml = loop_away(f, outdir)

