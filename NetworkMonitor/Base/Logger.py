"""

    :Logger:
    ==========

    :
    This is the logger object that is used to log events
    in the application.
    :

    :copyright: (c) 9/28/2015 by gammaRay.
    :license: BSD, see LICENSE for more details.

    Author:         gammaRay
    Version:        :1.0:
    Date:           9/28/2015
"""

"""
=============================================
Imports
=============================================
"""

import os
import time
import logging.handlers
from splunk_logger import SplunkLogger

from ..config import *

"""
=============================================
Constants
=============================================
"""

# Program Attributes
__author__  =   "gammaRay"
__version__ =   "1.0"
__date__    =   "9/28/2015"

"""
=============================================
Source
=============================================
"""

def set_logger(syslog=None, splunk=None):
    """
    This method sets the LOGGER for the context of the
    program.

    The splunk api logging struct is as followed:

        syslog = (

            'address',
            'port'

        )

        splunk = {

            'token' : < access token >,
            'project' : < project id >,
            'api' : < api domain >
            }

    :param syslog:                the syslog server address
    :param splunk:                the configs for the splunk logging engine
    """

    # Check to see if the dir is existent
    if not os.path.isdir(LOG_FILE_DIR):
        print('[-] Logging directory does not exist, creating.')

        # We create a dir
        os.makedirs(LOG_FILE_DIR)
        print('[+] Logging directory created: %s.' % LOG_FILE_DIR)

    # We set the file name
    filename = LOG_FILE_NAME % time.strftime('%d-%m-%y')

    # set up logging to file - see previous section for more details
    logging.basicConfig(
        level       =   logging.DEBUG,
        format      =   '[%(asctime)s]: %(name)-20s %(levelname)-20s %(message)s',
        datefmt     =   '%y-%m-%d %H:%M:%S',
        filename    =   filename,
        filemode    =   'a'
    )

    # We create the root LOGGER for console
    logger_console = logging.StreamHandler()
    logger_console.setLevel(LOGGER_LEVEL)

    # Create a formatter
    logger_formatter = logging.Formatter('[%(asctime)s]: %(name)-50s: %(levelname)-20s %(message)s')

    # We set the formatters
    logger_console.setFormatter(logger_formatter)

    # We set the root handlers
    logging.getLogger('').addHandler(logger_console)
    print('[+] Added a console logging engine...')

    if syslog:
        add_syslogger(syslog)

    if splunk:
        add_splunklogger(splunk)
    return

def add_syslogger(address):
    """
    This adds a syslogger instance to the root logger
    instance.

    :param address:             the address of the syslog server
    :return:
    """

    # Add the syslogger
    syslogger = logging.handlers.SysLogHandler(
        address=address
    )  #('syslog.haligonia.home.com',514))

    logging.getLogger('').addHandler(syslogger)
    print('[+] Added a syslog logging engine...')
    return

def add_splunklogger(configs):
    """
    This adds a splunk logger instance to the root logger
    instance.

    :param configs:             the dict containing the configs
    :return:
    """

    # Add the splunk logger
    splunk = SplunkLogger(
        **configs
    )
    logging.getLogger('').addHandler(splunk)
    print('[+] Added a splunk logging engine...')
    return
