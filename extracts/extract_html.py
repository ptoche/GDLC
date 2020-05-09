# Extract portion from very large html 
# each step broken down for clarity
# first look inside html to find cut-off text
import os
base = os.path.join(os.path.sep, 'Users', 'PatrickToche', 'calibre', 'RAE', 'mobi7')
name0 = 'book.html'
# save head
with open(os.path.join(base, name0)) as infile, open(os.path.join(base, 'head.html'), 'w') as outfile:
    for line in infile:
        head, sep, tail = line.partition('<body>')
        outfile.write(head)
# save body in two steps
with open(os.path.join(base, name0)) as infile, open(os.path.join(base, 'tmp.html'), 'w') as outfile:
    for line in infile:
        head, sep, tail = line.partition('Comienzo, al final del artículo, del bloque de envíos a otros lemas.</td></tr> </tbody> </table> </div> </div>')
        outfile.write(tail)
with open(os.path.join(base, 'tmp.html')) as infile, open(os.path.join(base, 'body.html'), 'w') as outfile:
    for line in infile:
        head, sep, tail = line.partition('<idx:entry scriptable="yes"><idx:orth value="abaá">')
        outfile.write(head)
# save foot
with open(os.path.join(base, name0)) as infile, open(os.path.join(base, 'foot.html'), 'w') as outfile:
    for line in infile:
        head, sep, tail = line.partition('</body>')
        outfile.write(tail)
# merge head, body and foot
filenames = [os.path.join(base, 'head.html'), os.path.join(base, 'body.html'), os.path.join(base, 'foot.html')] 
with open(os.path.join(base, 'extract.html'), 'w') as outfile:
    for names in filenames: 
        with open(names) as infile: 
            outfile.write(infile.read()) 
        outfile.write("\n") 


