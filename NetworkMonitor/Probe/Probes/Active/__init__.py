"""

    :__init__.py:
    ==========

    :
    Contains a maintained database of probe types that are
    accessible at the plugin level.
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

from .Host import *
from .Network import *

"""
=============================================
Constants
=============================================
"""

# Program Attributes
__author__  =   "gammaRay"
__version__ =   "1.0"
__date__    =   "9/28/2015"

ACTIVE_PROBES = {
    'host'      : ACTIVE_HOST_PROBES,
    'network'   : ACTIVE_NETWORK_PROBES
}