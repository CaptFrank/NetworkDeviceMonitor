"""

    :ZeroPublisher:
    ==========

    :
    This is the object that will publish the objects to the message
    server.
    :

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

import sys
import zmq
import time

from multiprocessing \
    import Process

"""
=============================================
Constants
=============================================
"""

# Program Attributes
__author__          =   "gammaRay"
__version__         =   "1.0"
__date__            =   "9/28/2015"

"""
=============================================
Source
=============================================
"""

class ZeroPublisher(object):
    """
    This is the class object that represents the publisher
    object that will take the message and send it to the
    publish queue.
    """

    # This is the name of the publisher
    __name          = None

    # This is the configs for the publisher
    __configs       = None

    def __init__(self, name, configs):

        return
