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
from NetworkMonitor.config import *

"""
=============================================
Constants
=============================================
"""

# Program Attributes
__author__  =   "gammaRay"
__version__ =   "1.0"
__date__    =   "9/28/2015"

PROBE_BEHAVIOURS = [
    'MONITOR',
    'OBSERVER'
]
PROBE_MONITORING = PROBE_BEHAVIOURS[0]
PROBE_OBSERVING = PROBE_BEHAVIOURS[1]

"""
=============================================
Source
=============================================
"""

class NetworkProbe(Probe):
    """
    This is the base network probing class object.
    It contains the appropriate attributes of a network
    scanner, sniffer that are needed to allow for the
    appropriate traffic to be monitored.

    It is mutable to be made into an active or passive
    probing agent.

    extends: MutableProbe, Probe
    """

    # Behaviour
    behaviour          = None

    # The logger
    _logger             = None

    # The packet count
    _packet_count       = 0

    # The counter
    _packet_counter     = 0

    # Database
    _database           = None

    # Iface that is used to sniff
    _iface             = None

    # Check the probe types
    _types             = {
    }

    # Probe table
    _probe_table       = {
        # Probe type -- Probe Function
    }

    def __init__(self, type, iface, queue):
        """
        This is the constructor that will set the self
        object to the appropriate object type.

        :param type:        Probe type Active / Passive
        :param queue:       Application queue
        :return:
        """

        # Override the class
        #MutableProbe.__init__(self, self._types)
        Probe.__init__(self, type, queue, False)

        # Set the iface
        self._iface = iface
        return

    def setup(self):
        """
        This is the setup method for the probe. It is called
        to setup the context of the probe itself. In this case
        the probe needs to
        :return:
        """

        # Register all handles
        self.set_data(
            self.data
        )
        self.register_type(
            self.type
        )
        self.set_definition(
            {
                "type"          : self.get_type(),
                "name"          : self.name,
                "description"   : self.description,
                "default"       : "yes",
                "help"          : self.description,
                "tag"           : self.name,
                "behaviour"     : self.behaviour,
                "fields"        : PLACEHOLDER_ARRAY,
                "groups"        : PLACEHOLDER_ARRAY,
            }
        )
        self.set_template(
            {
                "definition"    : self.get_definition(),
                "data"          : PLACEHOLDER_DICT
            }
        )

        # Set a new handle
        self._setup_db()
        self.logger.info(
            "Setup complete for probe: %s"
            %self.name
        )
        return

    def execute(self, packet):
        """
        Execute the filter / probe.

        :param packet:      The packet that has been read
        :return:
        """

        # Update the metrics
        self._packet_counter += 1
        self._correlate(packet)
        return

    def report(self):
        """
        This is the default reporting mechanism for the network
        probes.

        :param data:
        :return:
        """

        # We get all the data
        results = self._database.get_tables()
        template = self.get_template()
        template['data'] = results

        # Set the data
        self.set_data(template)
        return self.get_data()

    def _run(self):
        """
        This is the general running mechanism.

        :param probe_table: The probing execution tables.
        :return:
        """

        sniff(
            iface = self._iface,
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
        self._probe_table.update(
            {
                # Type name, Type callback object
                type : {
                    'layers'    : obj.layers,
                    'object'    : obj
                }
            }
        )
        self._types.update(
            {
                type : self
            }
        )
        return

    @abstractmethod
    def _correlate(self, packet):
        """
        Correlates the read data from the internal data.

        :return:
        """
        raise NotImplemented

    @abstractmethod
    def _setup_db(self):
        """
        Setup the internal database with the appropriate
        tables and data peices.

        :return:
        """
        raise NotImplemented


    def __process(self, packet):
        """
        This is the processing method that is used to process the
        packets in order to filter and create reports internally.

        :packet:            The packet that was sniffed
        :return:
        """

        # Report bool
        reported = False

        self._packet_count     += 1
        self._packet_counter   += 1

        # Cycle through the probe table
        for probe in self._probe_table.keys():

            # Get the layer
            layers = self._probe_table[probe]['layers']
            object = self._probe_table[probe]['object']

            # Check to see if the layers are satisfied
            for layer in layers:

                # If there is a missing layer
                if not packet.haslayer(layer):
                    return

            print("*** Found a good packet to read.")
            # Execute the probe
            object.execute(
                packet
            )

            # Check the packet count to report...
            if self._packet_count >= PACKET_REPORT_MAX:
                object.report()
                reported = True

        if reported:
            reported = False
            self._packet_counter = 0
        return