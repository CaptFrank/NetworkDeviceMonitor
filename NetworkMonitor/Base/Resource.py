"""

    :Resource:
    ==========

    :
    This is the managed resource between processes.
    Resources such as queues, locks and data are housed
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

import multiprocessing
from multiprocessing import Lock
from multiprocessing import JoinableQueue

"""
=============================================
Constants
=============================================
"""

# Program Attributes
__author__          =   "gammaRay"
__version__         =   "1.0"
__date__            =   "9/28/2015"

# ===========================================
# Types
RESOURCE_DEFAULT    = 0

"""
=============================================
Source
=============================================
"""


RESOURCE_TYPES      = [
    "DEFAULT"
]


def add_type(type):
    """
    Adds a type to monitor.
    """
    RESOURCE_TYPES.append(type)
    return

# ===========================================
# Managed Resource

class ManagedResource(object):
    """
    This is the wrapper class that is used to combine all
    resources into one cohesive object. In this case,
    we attribute resources based on tasks and interfaces to the
    application.

    i.e. Ip motoring task, Arp monitoring task
    """

    # Name of the resource
    __name          = None

    # Tag for the resource
    __tag           = None

    # Is it synched ?
    __sync          = None

    # Active flag
    __active        = False

    # The resource lock needed
    __lock          = None

    # The resource to manage
    __resource      = None

    def __init__(self, name=None, tag=None, sync=False):
        """
        This is the default constructor for the class object.

        :param name:        Name of the resource
        :param tag:         Tag for the resource
        :param sync:        Synchronization enabled
        :return:
        """

        # Set the internals of the class
        self.__name = name
        self.__sync = sync
        self.__tag  = tag
        self.__lock = Lock()
        return

    def lock(self):
        """
        Locks the resource to gain access to the data and objects within
        the resource.

        :return:
        """
        return self.__lock.acquire()

    def unlock(self):
        """
        Unlocks the resource to leave it behind for other processes to use.

        :return:
        """
        return self.__lock.release()

    def setObj(self, obj):
        """
        Sets the object in the resource.

        :param obj:         The object to manage.
        :return:
        """

        self.__resource = obj
        return

    def getObj(self):
        """
        Gets the object within the resource.

        :return:
        """
        return self.__resource

    __obj = property(getObj, setObj)


