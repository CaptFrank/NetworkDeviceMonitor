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

    # The zeromq context object
    __context           = None

    # The monitoring device handle
    __monitor           = None

    # The configs
    __configs           = None

    # Prefixes
    __prefixes          = {

        "IN"    : asbytes("IN"),
        "OUT"   : asbytes("OUT")
    }

    def __init__(self, configs):
        """
        This is the main constructor for the class.
        We pass it the configurations as a dict.

        :param configs:             The configurations dict
        :return:
        """

        # Set internal configs
        self.__configs = configs
        Process.__init__(self)
        return

    def setup(self):
        """
        This is the setup method that sets up the monitoring
        interface based on the saved configs.

        :return:
        """

        # Create a montoring devie
        self.__monitor = MonitoredQueue(
            zmq.XREP,
            zmq.PUB,
            self.__prefixes['IN'],
            self.__prefixes['OUT']
        )

        # Bind to the sockets.
        self.__monitor.bind_in(
            "tcp://{server}:{port}".format(
                server = self.__configs['server'],
                port = self.__configs['port']
            )
        )