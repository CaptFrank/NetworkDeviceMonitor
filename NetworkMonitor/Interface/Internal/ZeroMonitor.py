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
import logging

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

# Zeromq Transport mechanism
__TRANSPORT__       = "tcp://{server}:{port}"

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

    # The application name
    __name              = None

    # The logger
    __logger            = None

    # Prefixes
    __prefixes          = {

        "IN"    : asbytes("IN"),
        "OUT"   : asbytes("OUT")
    }

    # Applications that monitor
    __apps              = []

    # Alive?
    __alive             = True

    # Temporary storage for metrics

    def __init__(self, name, configs):
        """
        This is the main constructor for the class.
        We pass it the configurations as a dict.

        :param name:                The app name
        :param configs:             The configurations dict
        :return:
        """

        # Set internal configs
        self.__name = name
        self.__configs = configs
        self.__logger = logging.getLogger('ZeroMonitor - ' + name)
        Process.__init__(self)
        return

    def setup(self):
        """
        This is the setup method that sets up the monitoring
        interface based on the saved configs.

        :return:
        """

        # Create a monitoring devie
        self.__monitor = MonitoredQueue(
            zmq.XREP,
            zmq.PUB,
            self.__prefixes['IN'],
            self.__prefixes['OUT']
        )

        # Bind to the sockets.
        # - In
        # - Out
        # - Mon
        self.__monitor.bind_in(
            __TRANSPORT__.format(
                server = self.__configs['server'],
                port = self.__configs['rx_port']
            )
        )
        self.__monitor.bind_out(
            __TRANSPORT__.format(
                server = self.__configs['server'],
                port = self.__configs['tx_port']
            )
        )
        self.__monitor.bind_mon(
            __TRANSPORT__.format(
                server = self.__configs['server'],
                port = self.__configs['mon_port']
            )
        )

        # Set the socket options
        # Make the sockets monitored
        self.__monitor.setsockopt_in(zmq.HWM, 1)
        self.__monitor.setsockopt_out(zmq.HWM, 1)
        return

    def run(self):
        """
        Starts the monitoring thread.

        :return:
        """

        # Start the monitor
        self.__monitor.start()

        # From the registered monitoring applications,
        # we execute each one in a round robin fashion.
        while self.__alive:


            # For each app we run it.
            for app in self.__apps:
                app(self)
        return

    def stop(self):
        """
        Stops the monitoring device

        :return:
        """

        # Stops the threads
        # Kill the device monitor thread
        self.__monitor.join()

        # Kill the monitor threads
        self.__alive = False
        return

"""
=============================================
Monitoring applications
=============================================
"""

def __monitor_size(obj):
    """
    This is the monitoring of the size of the packet.
    Here we output to the terminal, (i.e. curses window)
    how big the packets are coming in are.

    :param obj:             The monitor device
    :return:
    """
    return

def __monitor_ids(obj):
    """
    This is the monitoring of the id of the packet.
    Here we output to the terminal, (i.e. curses window)
    what ids of the packets are coming in are.

    :param obj:             The monitor device
    :return:
    """
    return

def __monitor_timestamps(obj):
    """
    This is the monitoring of the timestamps of the packet.
    Here we output to the terminal, (i.e. curses window)
    when the packets were sent.

    :param obj:             The monitor device
    :return:
    """
    return