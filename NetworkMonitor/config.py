"""

    :name:
    ==========

    :description:

    :copyright: (c) 9/28/2015 by fpapinea.
    :license: BSD, see LICENSE for more details.

    Author:         fpapinea
    Version:        :version: #TODO
    Date:           9/28/2015
"""

"""
=============================================
Imports
=============================================
"""

import logging

"""
=============================================
Constants
=============================================
"""

# Program Attributes
__author__ = 'fpapinea'
__version__ = ""  #TODO
__date__ = "9/28/2015"

"""
=============================================
Variables
=============================================
"""

"""
=============================================
Source
=============================================
"""

LOGGER_LEVEL        = logging.INFO
LOG_FILE_DIR        = '/var/log/NetworkMonitor/'
LOG_FILE_NAME       = '/var/log/NetworkMonitor/mon-%s.log'

DEFAULT_SIZE        = 1024


# Default location for plugins. This can be changed to suit the
# users preferred plugins directory
PLUGIN_WORKSPACE    = './Configs/Plugins/'
CONFIG_WORKSPACE    = './Configs/'