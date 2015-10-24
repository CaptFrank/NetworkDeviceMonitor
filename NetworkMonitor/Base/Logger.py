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
import logging
import tempfile

try:
    # Python 2.6
    from logutils.dictconfig import dictConfig

except ImportError:

    # Python >= 2.7
    from logging.config import dictConfig

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

# Define the logging configuration
LOGGING_CFG = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'INFO',
        'handlers': ['file', 'console']
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s -- %(levelname)s -- %(message)s'
        },
        'short': {
            'format': '%(levelname)s: %(message)s'
        },
        'free': {
            'format': '%(message)s'
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            # http://stackoverflow.com/questions/847850/cross-platform-way-of-getting-temp-directory-in-python
            'filename': os.path.join(tempfile.gettempdir(), 'netmonitor.log')
        },
        'console': {
            'level': 'CRITICAL',
            'class': 'logging.StreamHandler',
            'formatter': 'free'
        }
    },
    'loggers': {
        'debug': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
        },
        'verbose': {
            'handlers': ['file', 'console'],
            'level': 'INFO'
        },
        'standard': {
            'handlers': ['file'],
            'level': 'INFO'
        }
    }
}


def tempfile_name():
    """
    Return the tempfile name (full path).
    """

    ret = os.path.join(tempfile.gettempdir(), 'netmonitor.log')
    if os.access(ret, os.F_OK) and not os.access(ret, os.W_OK):
        print("WARNING: Couldn't write to log file {0}: (Permission denied)".format(ret))
        ret = tempfile.mkstemp(prefix='glances', suffix='.tmp', text=True)
        print("Create a new log file: {0}".format(ret[1]))
        return ret[1]
    return ret


def logger():
    """
    Build and return the logger.
    """

    # Create the logger
    temp_path = tempfile_name()
    _logger = logging.getLogger()
    LOGGING_CFG['handlers']['file']['filename'] = temp_path
    dictConfig(LOGGING_CFG)
    return _logger