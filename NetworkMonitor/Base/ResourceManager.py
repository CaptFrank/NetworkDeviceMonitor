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
from queue import Queue
from multiprocessing.managers import \
    BaseManager

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

class ResourceQueue(Queue):
    """
    This is the joinable queue definition that is used for the
    publishers. We cal call this queue from the contexts of both
    worker objects.

    extends JoinableQueue
    """
    pass

class ResourceManager(BaseManager):
    """
    This is the base manager that is used to queue data from
    each plugin thread into one entity. From these queues the
    subscriber thread can then take the data and publish it to
    our elastic search database.

    extends: BaseManager
    """

    # Active queues that are in play
    __active_queues         = {}

    def add_queue(self, name):
        """
        This is the function that will add a queue
        with the name given to the Resource Manager
        reference.

        :param name:        The name of the queue to add
        :return:
        """

        self.__active_queues[name] = ResourceQueue()
        return

    def get_queue(self, name):
        """
        This is the method that will get a queue that has already
        been registered to the resource manager.

        :param name:        The name of the queue to add
        :return:
        """

        if name not in self.__active_queues.keys():
            return None
        return self.__active_queues[name]

def get_client_manager():
    """
    This gets the resource manager entity and registers the
    get_queue method.

    :return:
    """

    # Register the queue method
    ResourceManager.register(
        'get_queue',
        callable=ResourceManager.get_queue
    )

    # Get the server manager
    manager = ResourceManager(
        address = (
            "",
            50000
        ),
        authkey = 'NetworkMonitor'
    )
    client = manager.connect()
    return client

def get_server_manager():
    """
    This method sets up the setup manager process.

    :return:
    """

    # Register the queue method
    ResourceManager.register(
        'get_queue',
        callable=ResourceManager.get_queue
    )

    # Get the server manager
    manager = ResourceManager(
        address = (
            "",
            50000
        ),
        authkey = 'NetworkMonitor'
    )
    server = manager.get_server()
    return server, manager


