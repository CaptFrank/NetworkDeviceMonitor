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

import datetime
from uuid import uuid4

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
RESOURCE_TEST       = 1

"""
=============================================
Source
=============================================
"""


RESOURCE_TYPES      = [
    "DEFAULT",
    "TEST"
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
    name          = None

    # Tag for the resource
    tag           = None

    # Tracking
    uuid          = None

    # The resource to manage
    resource      = None

    # Time at which the resource is set
    time          = None

    def __init__(self, name=None, tag=None):
        """
        This is the default constructor for the class object.

        :param name:        Name of the resource
        :param tag:         Tag for the resource
        :param sync:        Synchronization enabled
        :return:
        """

        # Set the internals of the class
        self.name = name
        self.tag  = tag
        self.uuid = str(uuid4())
        return

    def setObj(self, obj):
        """
        Sets the object in the resource.

        :param obj:         The object to manage.
        :return:
        """

        # Set the object
        self.resource = obj

        # Set the time at which the object is set
        self.time     = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return

    def getObj(self):
        """
        Gets the object within the resource.

        :return:
        """
        return self.resource

    __obj = property(getObj, setObj)


