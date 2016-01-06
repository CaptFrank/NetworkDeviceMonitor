"""

    :ResourceManager:
    ==========

    :
    This is the resource manager that is needed to
    pass data from the plugin publishing threads to
    the plugin subscriber thread.
    :

    :copyright: (c) 10/23/2015 by gammaRay.
    :license: BSD, see LICENSE for more details.

    Author:         gammaRay
    Version:        :1.0:
    Date:           10/23/2015
"""

"""
=============================================
Imports
=============================================
"""
from multiprocessing.queues import \
    JoinableQueue
from multiprocessing.managers import \
    BaseManager
from NetworkMonitor.Base.Singleton import \
    Singleton

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

class ResourceManager(Singleton, BaseManager):
    """
    This is the base manager that is used to queue data from
    each plugin thread into one entity. From these queues the
    subscriber thread can then take the data and publish it to
    our elastic search database.

    extends: BaseManager
    """
    pass

class ResourceQueue(JoinableQueue):
    """
    This is the joinable queue definition that is used for the
    publishers. We cal call this queue from the contexts of both
    worker objects.

    extends JoinableQueue
    """
    pass

def add_queue(manager, name):
    """
    This is the function that will add a queue
    with the name given to the Resource Manager
    reference.

    :param name:        The name of the queue to add
    :param manager:     The manager to add the queue to
    :return:
    """