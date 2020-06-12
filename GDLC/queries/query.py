"""
Module to interpret user interaction. 

Used to warn the user about processing and potentially overwriting a large number of files and to receive confirmation feedback.

Created 3 May 2020

@author: patricktoche
"""

import sys
import string

def query_yes_no(question, answer='no'):
    """Ask the user a yes/no question, read it with input() and return their answer.
    
    Args:
        question (str): A message presented to the user
        answer (str): User feedback processed after user selection
            default value: 'no'

    Return: 
        answer (str): 'yes' or 'no'
    """
    if not answer:
        prompt = '\n     [y/n]\n'
    elif answer == 'yes':
        prompt = '\n     [y/N]\n'
    elif answer == 'no':
        prompt = '\n     [Y/n]\n'
    else:
        raise ValueError('invalid answer: "%s"' % answer)

    valid_answers = {'yes':'yes', 'y':'yes',
                     'no':'no',   'n':'no'}
    
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        choice = choice.strip(string.punctuation+string.whitespace)
        if answer and choice == '':
            return answer
        elif choice in valid_answers.keys():
            return valid_answers[choice]
        else:
            sys.stdout.write('Please answer "yes" or "no" '\
                             '(or "y" or "n").\n')

