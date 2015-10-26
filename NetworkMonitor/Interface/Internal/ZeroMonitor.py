"""

    :ZeroMonitor:
    ==========

    :
    This is the monitring class for each queue created.
    It allows us to tap into the data pipe and see realtime
    data from each queue as they are inserted in the queue.
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

import zmq
import time

from zmq.devices.basedevice \
    import ProcessDevice

from zmq.devices.monitoredqueuedevice \
    import MonitoredQueue

from zmq.utils.strtypes \
    import asbytes

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

class ZeroMonitor(Process):
    """
    This is the class object that will host the monitoring
    functionality for the queues. Depending on if the monitor flag
    is set to true, this monitoring feature is enabled.
    """

    def __init__(self):



        Process.__init__(self)
        return

