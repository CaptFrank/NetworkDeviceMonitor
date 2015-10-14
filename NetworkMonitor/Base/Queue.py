"""

    :Queue:
    ==========

    :
    This is the managed resource between processes.
    Queue such as queues, locks and data are housed
    here to allow for synchronization to occur.
    :

    :copyright: (c) 9/30/2015 by gammaRay.
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

from ..config import *
from .Resource import RESOURCE_TYPES

import multiprocessing
from multiprocessing import Lock
from multiprocessing import JoinableQueue

"""
=============================================
Constants
=============================================
"""

# Program Attributes
__author__      =   "gammaRay"
__version__     =   "1.0"
__date__        =   "9/28/2015"

"""
=============================================
Source
=============================================
"""

# ===========================================
# Managed Queue

class ManagedQueue(JoinableQueue):
    """
    This is the managed queue resource. We use this queue between
    the services and the processors. I.e. pre-fetcher and the
    response parsers.
    """

    # The attribute types.
    __type              = None

    def __init__(self, size=DEFAULT_SIZE):
        """
        The default constructor for the class.

        :param size:            The default size
        :return:
        """

        super(JoinableQueue).__init__(size)
        return

    def initialize(self, type=None):
        """
        This creates the queue and associates it to a resource type.

        :param type:
        :return:
        """

        self.__type     = type
        return



