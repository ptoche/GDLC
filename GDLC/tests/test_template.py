"""
This `test_template.py` file is intended to illustrate how doctest works and to alert to common pitfalls. Examples of errors include: 
    indenting the code block below
    omitting an empty line in place of an empty result
    omitting an empty line to mark the end of a print display
    omitting the ellipsis ... for multi-line strings
    omitting a <BLANKLINE> in the output
Small changes to the formatting below will result in errors. 
Set x and y to 1 and 2.
>>> x, y = 1, 2

Print their sum:
>>> print(x+y)
3

>>> def replace_string(text:str, char:str):
...    return text.replace(char, '')
>>> test = '''a
... b
... c'''
>>> r = replace_string(test, 'b')
>>> print(r)
a
<BLANKLINE>
c

Multiline example:
>>> for i in range(10):
...     r = i**i
...     print(' ', r, sep='', end='')
1 1 4 27 256 3125 46656 823543 16777216 387420489

"""