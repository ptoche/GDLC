"""
Configure logging
"""

# To navigate the directory structure:
import os

# To add a time stamp to the log's file name:
from datetime import datetime

# Python's logging module:
import logging

def custom_logs(datefmt='%Y-%m-%d::%H:%M:%S', 
                filename=datetime.now().strftime(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logfiles', 'GDLC_%Y_%m_%d_%H_%M.log')),
                format='%(name)s:%(asctime)s %(filename)s %(process)d[%(funcName)s line:%(lineno)d] %(levelname)s:%(message)s',
                filemode='w',
                force=True,
                level='debug'):
    """
    Create a custom logger.

    Args:
        datefmt (str): date format, defaults to '%H:%M:%S'
        filename (str): full path to logfile with extension included
        format (str): format option passed to logging.basicConfig
        filemode (str): 'w' for 'write' mode, 'a' for 'append' mode
        force (bool): set to True to clear existing handlers
        level (str): select from: 'debug' > 'info' > 'warning' > 'error' > 'critical'
        level (int): select from:    50   >   40   >    30     >    20   >    10
        level (str, int): also accepts uppercase ('DEBUG') or integer as string ('10')

    Returns:
        head (str): head of the html page
    """
    logger = logging.getLogger(__name__)
    # clear handlers  --fix for annoying feature -- but does force=True work too?
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    # set basic configuration (see the docs for the numeric values of logging levels):
    d = {'debug': '10', 'info': '20', 'warning': '30', 'error': '40', 'critical': '50'} 
    if isinstance(level, int):
        level = str(level)  # convert level to string to enable membership check below
    level = level.lower()  # allow keywords like 'DEBUG' 
    if level not in d and level not in d.values():
        return print('The argument `level` must take one of the following values or keys:\n\n', d)
    if level in d:
        level = d[level]
    level = int(level)  # convert level to integer, as basicConfig expects an integer
    logging.basicConfig(datefmt=datefmt,
                        filename=filename,
                        filemode=filemode,
                        force=force,
                        format=format,
                        level=level)
    return print('The logging package has been imported and configured. Logs will be saved as: ', filename)

