#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GDLC debugging

Functions to debug the GDLC module. Some of these functions are called if the argument `verbose` is set to `True`. Some of these functions are used only to assist code writing.

Created 3 May 2020

@author: patricktoche
"""
from bs4 import BeautifulSoup, Tag, NavigableString, Comment, PageElement
from pprint import pprint
import logging
import traceback
import time

def print_children(soup: BeautifulSoup) -> None:
    """
    Print information about all children and descendents.

    Args: 
        soup (BeautifulSoup): dictionary entry
    """
    print('\n')
    print('Number of children and descendants of main soup object:\n')
    print('No. children:   ', len(list(soup.children)))
    print('\nThe children are printed below:')
    print('\n', list(soup.children))
    print('\nNo. descendants:', len(list(soup.descendants)))
    print('\nThe descendants are printed below:')
    print('\n', list(soup.descendants))
    print('\n')
    return None


def print_child_extract(child: Tag) -> None:
    """
    Print information about each dictionary entry as a child of main soup.

    Args: 
        child (Tag): child of dictionary entry
    """
    print('\n')
    print('This child was removed:\n', child)
    print('\nIf this was not intended, adjust the list of protected tags and classes.')
    return None


def print_child_info(child: Tag) -> None:
    """
    Print information about each dictionary entry as a child of main soup.

    Args: 
        child (Tag): child of dictionary entry
    """
    print('\n')
    print('child.name =', child.name)
    print('child["class"]', child['class'])
    print('\n')
    return None


def print_counter(i: int) -> None:
    """Print a counter. 
    """
    print('\n')
    print('Counter updated at each iteration over the children:')
    print('i = ', i)
    print('\n')
    return None


def print_dictionary_info(n: int) -> None:
    """Print the number of definitions in the current document."""
    print('\n')
    print('This dictionary contains ', n, ' definitions.')
    print('\n')
    return None


def print_log_error(item, error=None, record=[]) -> None:
    """
    Print a message and log an exception.

    Modules: 
        logging (error), traceback
    """
    print('\n\nEXCEPTION RAISED! \n\nPROBLEM WITH:\n\n', item, '\n\nAN ERROR WAS LOGGED\n\n')
    logging.error("Exception occurred: %s", error)
    record.append(item)
    trace = traceback.format_exc()
    logging.error(trace)
    return None


def print_soup_info(soup: BeautifulSoup, name=None) -> str:
    """
    Print information about a BeautifulSoup object for degugging purposes.

    Modules: bs4 (BeautifulSoup)
    """ 
    info = {'name': None, 'type': None, 'class': None, 'content': None, 'children': None}
    soup_name, soup_type, soup_class, soup_content, soup_children =  ([], ) * 5
    try:
        soup_name = soup.name
    except Exception:
        soup_name.append('NA')
    try:
        soup_type = type(soup)
    except Exception:
        soup_type.append('NA')
    try:
        soup_class = [i.text.strip() for i in soup.select('class')]
    except Exception:
        soup_class.append('NA')
    try:
        for si in soup.content:
            soup_content.append(si)
    except Exception:
        soup_content.append('NA')
    try:
        if soup.findChildren(recursive=False):
            soup_children = soup.findChildren(recursive=False)
    except Exception:
        soup_children.append('NA')
    # add information to dictionary:
    info.update({'name': soup_name, 'type': soup_type, 'content': soup_content, 'children': soup_children})
    # print to console:
    sep_line = '============================================================================='
    print('\n\n INFORMATION REQUESTED:\n', sep_line, '\n') 
    pprint.pprint(info, indent=0, width=80)
    print('\n', sep_line, '\n\n')
    # return the dictionary
    return info


def print_summary(docstring: str) -> None:
    """
    Prints a function's docstring.

    Args: 
        docstring (str): documentation
    """
    print('\n')
    print('The `verbose` flag was set to `True`\n')
    print('Summary of main function:\n')
    print(docstring)
    print('\n')
    return None


def print_output(output: str) -> None:
    """
    Print output to screen surrounded by double lines (more visible, useful for debugging).

    Args: 
        output (str): any string
    """
    print('\n\nOUTPUT PRINTOUT:\n================\n', output, '\n================\n\n')
    return None


def print_type(*args) -> None:
    """
    Print the type of the argument. 

    Args: 
        args (any type): tuple of any size
    Returns: 
        None
    """
    print('\n')
    for idx, arg in enumerate(args, start=1):
        print('type of arg %s is %s' % (idx, type(arg)))
    print('\n')
    return None


def print_warn_missing(item: Tag) -> None:
    """Warn about items with length 0"""
    print('\n')
    print('Warning: These items are empty and will be stripped:\n', item)
    if item.parent:
        print('These items are children of\n', item.parent)
        print('\n')
    return None
