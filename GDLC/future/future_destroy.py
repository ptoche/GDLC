"""Strip empty tags

Improved version of patched_extract()

Status: In Progress
"""

from GDLC import GDLC
from bs4 import BeautifulSoup

# Usage:
def strip_empty_tags(soup:BeautifulSoup):
    for item in soup.find_all():
        if not item.get_text(strip=True):
            item.destroy()  # This method to be added to PageElement, see below
    return soup



# based on BeautifulSoup extract(), decompose(), smooth() methods:

# import PageElement if it has not been imported already
import sys
if 'PageElement' not in sys.modules:
    from bs4 import PageElement


def debug_destroy(self, pos):
    if pos == 1:
        try:
            __self_index = self.parent.index(self)
        except:
            pass
        try:
            print('DEBUG 1: self = \n\n', self, '\n\n')
        except:
            pass
        try:
            print('DEBUG 2: self.parent.contents[_self_index] = \n\n', self.parent.contents[__self_index], '\n\n')
        except:
            pass
        try:
            print('DEBUG 3: self.contents[_self_index-1] = \n\n', self.contents[__self_index-1], '\n\n')
        except:
            pass
        try:
            print('DEBUG 4: self.contents[_self_index+1] = \n\n', self.contents[__self_index+1], '\n\n')
        except:
            pass
        try:
            print('DEBUG 5: self._last_descendant() = \n\n', self._last_descendant(), '\n\n')
        except:
            pass
        try:
            print('DEBUG 6: self._last_descendant().next_element = \n\n', self._last_descendant().next_element, '\n\n')
        except:
            pass
        try:
            print('DEBUG 7: self._last_descendant().previous_element = \n\n', self._last_descendant().previous_element, '\n\n')
        except:
            pass
    if pos == 2:
        try:
            print('DEBUG 8: self.__dict__. = \n\n', self.__dict__.)
        except:
            pass
    if pos == 3:
        try:
            for i in self.contents[:]:
                while i is not None:
                    n = i.next_element
                    print('DEBUG 9: self.contents[:].next_element = \n\n', i.next_element, '\n\n')
                    i = n
        except:
            pass
    return None


def destroy(self, _self_index=None, debug=False):
    """Combines several elements of BeautifulSoup extract(), decompose(), smooth() methods.    

    Remove this element from the tree and its children.

    :param _self_index: The location of this element in its parent's
       .contents, if known. Passing this in allows for a performance
       optimization.

    :return: `self`, no longer part of the tree.
    """
    if debug:
        debug_destroy(self, 1)
    # from extract() method
    if self.parent is not None:
        if _self_index is None:
            _self_index = self.parent.index(self)
        del self.parent.contents[_self_index]

        # remove nearby parents if empty
        # check that nearby parent.contents is empty before deleting:
        try:
            for i in range(_self_index-1, _self_index+1):
                if str(self.parent.contents[i]).strip() == '':
                    del self.parent.contents[i]
        except: 
            pass

    # Find the two elements that would be next to each other if this
    # element and children had not been parsed and connect them:
    last_child = self._last_descendant()
    next_element = last_child.next_element

    if (self.previous_element is not None and
        self.previous_element is not next_element):
        self.previous_element.next_element = next_element
    if next_element is not None and next_element is not self.previous_element:
        next_element.previous_element = self.previous_element
    self.previous_element = None
    last_child.next_element = None

    self.parent = None
    if (self.previous_sibling is not None
        and self.previous_sibling is not self.next_sibling):
        self.previous_sibling.next_sibling = self.next_sibling
    if (self.next_sibling is not None
        and self.next_sibling is not self.previous_sibling):
        self.next_sibling.previous_sibling = self.previous_sibling
    self.previous_sibling = self.next_sibling = None
    
    if debug:
        debug_destroy(self, 3)

    return self
# attach new method:
PageElement.destroy = destroy




# TESTING GROUND:
>>> dml = '''<html>
... <head>
...   <title>TITLE</title>
... </head>
...   <body>'LINE 0 AFTER OPENING BODY TAG FOLLOWED BY LINE BREAK'
...     'LINE 1 NO SPACE BEFORE DIV'<div>TEXT1</div>'LINE 1 NO SPACE AFTER DIV'
...     'LINE 2 NO SPACE BEFORE P'<p>TEXT2</p>'LINE 2 NO SPACE AFTER P'
...     'LINE 3 NO SPACE BEFORE DIV'<div><i>TEXT3</i></div>  'LINE 3 DOUBLE SPACE AFTER DIV'# COMMENT
...   </body>'LINE 4 AFTER CLOSING BODY TAG'
... </html>'''
>>> dml = '''<html>
... <head>
...   <title>TITLE</title>
... </head>
...   <body>
...     <div>TEXT1</div>
...     <p>TEXT2</p>
...     <div><i>TEXT3</i></div>  # COMMENT
...   </body>
... </html>'''



>>> soup = BeautifulSoup(dml, features='lxml')
>>> for tag in soup.find_all('div'):
>>>     tag.destroy()
>>> print(soup)


dml = '''<html><body>TEXT_BEFORE <i>ITALIC</i> TEXT_AFTER</body></html>'''
soup = BeautifulSoup(dml, features='lxml')
tags = soup.find_all('i')
for i in tags:
    print('parent = ', i.parent)
    print('child = ', i.child)
    print('descendent = ', i.descendent)
    print('next_sibling = ', i.next_sibling)
    print('previous_sibling = ', i.previous_sibling)
    print('next_element = ', i.next_element)
    print('previous_element = ', i.previous_element)

soup = BeautifulSoup(dml, features='lxml')
print('soup = ', soup)
for i in soup.find_all('i'):
    print('i = ', i)
    p = i.parent
    print('i.parent = ', p)
    pe = p.previous_element
    print('p.previous_element = ', pe)
    ne = p.next_element
    print('p.next_element = ', ne)
#    i.extract()
    i.destroy(debug=False)
    print('soup = ', soup)
    
soup.find_all()


def is_surrounded_by_spaces(tag: Tag) -> bool:
    """
    True if tag is surrounded by empty spaces, False otherwise.
    """
    from bs4 import NavigableString as NS
    try:
        lhs = tag.previous_element
        rhs = tag.next_element
    except:
        return None
    if isinstance(lhs, NS) and isinstance(rhs, NS):
        if lhs.endswith(' ') and rhs.endswith(' '):
            lhs.replace_with(lhs.rstrip())
        
        
    return is_surrounded


