"""

    :name:
    ==========

    :description:

    :copyright: (c) 2015-10-23 by gammaRay.
    :license: BSD, see LICENSE for more details.

    Author:         gammaRay
    Version:        :1.0:
    Date:           9/30/2015
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
__author__              =   "gammaRay"
__version__             =   "1.0"
__date__                =   "9/28/2015"


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

LOGGER_LEVEL            = logging.INFO,
LOG_FILE_DIR            = '/var/log/NetworkMonitor/'
LOG_FILE_NAME           = '/var/log/NetworkMonitor/mon-%s.log'

DEFAULT_SIZE            = 1024
PACKET_REPORT_MAX       = 200


# Default location for plugins. This can be changed to suit the
# users preferred plugins directory
PLUGIN_WORKSPACE        = './Configs/Plugins/'
CONFIG_WORKSPACE        = './Configs/'

CONNECTION_TIMEOUT      = 5
PUBLISH_INTERVAL        = 1
REPORT_MAX_SIZE         = 10
TTL                     = 600

RESOURCE_MANAGER_ADDR   = ''
RESOURCE_MANAGER_PORT   = 56000
RESOURCE_MANAGER_AUTH   = 'NetworkMonitor'
