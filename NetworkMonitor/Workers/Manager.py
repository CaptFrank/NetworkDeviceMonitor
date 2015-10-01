"""

    :Manager:
    ==========

    :
    This is the resource manager process that contains both the
    real time data that is acquired from the probes, but also
    the main process attributes (i.e. configs, queues, etc...)
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

import multiprocessing
from multiprocessing.managers import SyncManager
from ..Base.Resource import ManagedResource

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

class ResourceManager(SyncManager):
    """
    This is the resource manager that takes care of the management
    of each data queue and data repository. It also manages the caches
    between applications.
    """

    # The managers name
    __name          = None

    # The management structure
    # We index the dict by management type
    __management    = {}


    def __int__(self, name='default', address=None, authkey=None):
        """
        This is the default constructor for the class.

        :param name:    The manager name
        :param address: The address of the server
        :param authkey: The auth key
        :return:
        """

        # Set internals
        self.__name     = name

        # Override the manager
        SyncManager.__init__(address, authkey)
        return

    def register_resource(self, type, cls):
        """
        This is the main registering method for the class.
        It takes in a task type and a class object.

        :param type:    The task type
        :param cls:     The class object
        :return:
        """

        # Make a new lock based on task type
        if self.__management[type] is None:

            # Create a resource entity to manage
            self.__management[type] = []
            self.__management[type].append(
                ManagedResource(
                    cls
                )
            )

        else:

            # Append the class object to the managed resource
            self.__management[type].append(
                ManagedResource(
                    cls
                )
            )
        return

    def unregister_resource(self, type, cls):
        """
        This is the main unregistering method for the class.
        It takes in a task type and a class object.

        :param type:    The task type
        :param cls:     The class object
        :return:
        """

        # Delete lock based on task type
        return

    def activate_resource(self, type):
        """
        This activates the management handles for a particular
        resource type.

        :param type:
        :return:
        """


        return

    def deactivate_resource(self, type):
        """
        This deactivates the management handles for a particular
        resource type.

        :param type:
        :return:
        """

        return