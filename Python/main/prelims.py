
# Preliminary 
# Find all instances of classes for <p> tags
# keep outside the main loop to reduce overhead
import os
base = os.path.join(os.path.sep, 'Users', 'PatrickToche', 'KindleDict', 'GDLC-Kindle-Lookup', 'mobi8', 'OEBPS', 'Text')
excluded = {'cover_page.xhtml', 'part0000.xhtml', 'part0001.xhtml', 'part0002.xhtml', 'part0003.xhtml', 'part0004.xhtml', 'part0005.xhtml', 'part0006.xhtml', 'part0007.xhtml', 'part0008.xhtml', 'part0009.xhtml', 'part0010.xhtml', 'part0011.xhtml', 'part0012.xhtml', 'part0013.xhtml', 'part0014.xhtml', 'part0015.xhtml', 'part0016.xhtml', 'part0276.xhtml', 'part0277.xhtml'}
classes = set()
for root, dirs, files in os.walk(base):
    for file in files:
        if not file in excluded:
            filepath = root + os.sep + file
            if filepath.endswith('.xhtml'): 
                with open(filepath) as infile:
                    s = BeautifulSoup(infile)
                    c = set(value
                            for element in s.find_all(class_=True)  # s.find_all('p', class_=True) 
                            for value in element["class"])
                    print(c)
                    for item in c:
                        if item not in classes:
                            classes.add(item)
print(classes)
## for p tags only:
## {'p', 'calibre31', 'df', 'p1', 'calibre10', 'tlogo', 'trevisio', 'calibre6', 'ps', 'salt6', 'rf', 'tc', 'salt3', 'salt1', 'salt4', 'pc', 'calibre15', 'salt2', 'tautor', 'asang', 'salt', 'tfirma'}
## for all tags:
## {'calibre21', 'calibre34', 'calibre17', 'calibre13', 'ilustrautor', 'p1', 'n', 'vctr', 'calibre36', 'calibre10', 'info', 'ps', 'sinopsi', 'sans2', 'ttitol', 'tc', 'centrat2', 'n1', 'salt1', 'calibre15', 'salt2', 'tautor', 'asang2', 'asang', 'tfirma', 'calibre29', 'df', 'centrat1', 'calibre22', 'calibre27', 'calibre25', 'calibre6', 'calibre35', 'calibre9', 'calibre5', 'sans3', 'calibre23', 'calibre4', 'calibre3', 'v', 'calibre32', 'p', 'calibre12', 'calibre31', 'calibre28', 'calibre24', 'trevisio', 'salt6', 'calibre33', 'calibre11', 'calibre7', 'asang1', 'tdata', 'pc', 'salt4', 'v2', 'calibre37', 'calibre18', 'ocult', 'calibre30', 'calibre16', 'calibre14', 'calibre26', 'calibre20', 'salt5', 'salt10p', 'tlogo', 'ex', 'rf', 'calibre1', 'calibre2', 'sans', 'centrat', 'salt3', 'calibre19', 'cita', 'calibre8', 'n2', 'sans1', 'v1', 'salt', 'calibre'}
## for all tags in non-excluded files:
## {'calibre32', 'calibre34', 'p', 'calibre17', 'df', 'salt10p', 'calibre13', 'calibre24', 'p1', 'calibre22', 'calibre27', 'n', 'vctr', 'calibre25', 'ps', 'ex', 'calibre33', 'rf', 'calibre35', 'tc', 'centrat2', 'n1', 'pc', 'calibre23', 'calibre19', 'v1', 'v', 'calibre'}

