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

import multiprocessing

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
        return