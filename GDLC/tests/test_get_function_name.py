""" 
Get a function's name from inside the function's body.

>>> from GDLC.GDLC import *
>>> def print_function_name():
...     '''Print output of `get_function_name()`'''
...     return print(get_function_name())
>>> get_function_name()
'get_function_name'

>>> print_function_name()
get_function_name

"""
