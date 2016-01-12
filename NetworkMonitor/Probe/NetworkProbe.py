"""

    :NetworkProbe:
    ==========

    :
    This is the class object that implements a PF_RING type
    queue to hold incoming data from the commonly used interface.
    We need this common resource pool to allow for multiple threads
    to act upon the accurately match packet type.
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

from scapy.all import *
from abc import abstractmethod
from NetworkMonitor.Probe.Probe \
    import Probe, PLACEHOLDER_ARRAY, \
    PLACEHOLDER_DICT, PLACEHOLDER_STRING
from NetworkMonitor.Probe.MutableProbe \
    import MutableProbe

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

class NetworkProbe(MutableProbe, Probe):
    """
    This is the base network probing class object.
    It contains the appropriate attributes of a network
    scanner, sniffer that are needed to allow for the
    appropriate traffic to be monitored.

    It is mutable to be made into an active or passive
    probing agent.

    extends: MutableProbe, Probe
    """

    # Check the probe types
    __types         = {
    }

    # Probe table
    __probe_table   = {
        # Probe type -- Probe Function
    }

    # Iface that is used to sniff
    __iface         = None

    # The logger
    _logger         = None

    def __init__(self, type, iface, queue):
        """
        This is the constructor that will set the self
        object to the appropriate object type.

        :param type:        Probe type Active / Passive
        :param queue:       Application queue
        :return:
        """

        # Override the class
        Probe.__init__(self, type, queue, False)
        MutableProbe.__init__(self, self.__types)

        # Set the iface
        self.__iface = iface

        # Run the object
        self.run(
            type, queue,
            **{
                'iface' : iface
            }
        )
        return

    @abstractmethod
    def execute(self, packet):
        """
        This is the execution method for tha passive
        probes.

        :param packet:
        :return:
        """
        raise NotImplemented

    @abstractmethod
    def report(self, data):
        """
        This is the default reporting mechanism for the network
        probes.

        :param data:
        :return:
        """
        raise NotImplemented

    def _run(self):
        """
        This is the general running mechanism.

        :param probe_table: The probing execution tables.
        :return:
        """

        sniff(
            iface = self.__iface,
            prn = self.__process
        )
        return

    def _register_probe(self, type, obj):
        """
        This registers a function based on the type of monitor that
        is needed.

        :param type:        The type of monitor needed -- The layer triggered on it.
        :param obj:         The object callback to call when an event it triggered.
        :return:
        """

        # Update the probe table
        self.__probe_table.update(
            {
                # Type name, Type callback object
                type : {
                    'layer' : obj.layer,
                    'object': obj
                }
            }
        )
        self.__types.update(
            {
                type : self
            }
        )
        return

    def __process(self, packet):
        """
        This is the processing method that is used to process the
        packets in order to filter and create reports internally.

        :packet:            The packet that was sniffed
        :return:
        """

        # Cycle through the probe table
        for probe in self.__probe_table.keys():

            # Get the layer
            layer = self.__probe_table[probe]['layer']
            object = self.__probe_table[probe]['object']

            # Screen the probes....
            if packet.haslayer(layer):

                # Execute the probe
                object.execute(
                    packet
                )
        return