"""

    :ArpProbe:
    ==========

    :
    This is the mac address poller. It scans the network and
    gets the device mac addresses. Once the addresses are
    validated and cached, they are entered in the resource manager
    where other processes can use them for alerts and correlation.
    :

    :copyright: (c) 9/28/2015 by fpapinea.
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

from NetworkMonitor.Probe.Probes.Passive.Network.MacProbe \
    import *

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
class ArpProbe(MacProbe):
    """
    This is the MAC probe that will be used to poll
    the network interface and sniff out the MAC addresse.
    Then is reports them in the data record sent to the
    message engine.

    extends: NetworkProbe
    """

    # The class name
    name            = "ArpProbe"

    # The probe type
    type            = "ARP"

    # Description
    description     = \
    "This is the probe that will monitor the arp addresses " \
    "on the network and will correlate them to a db."

    # Groups
    groups          = [
        "arp",
        "network",
        "reconnaissance"
    ]

    # Layer filter
    layer           = ARP

    # ====================
    # Protected
    # ====================

    # Local database tables
    _tables         = [
        'KNOWN_MAC',
        'UNKNOWN_MAC'
    ]

    # ====================
    # Private
    # ====================

    # App configs
    __configs       = None

    # Time
    __date          = None

    def __init__(self, queue, configs):
        """
        This is the default constructor for the class.
        We supply the iface and the queue.

        :param type:        The type of probe
        :param queue:       The application queue
        :param configs:     The app configs (i.e. known, iface, save)
        :return:
        """

        # Get the configs
        self.__configs = configs

        # Register the probe type as a passive probe
        PassiveNetworkProbe.__init__(
            self,
            self.type,
            queue,
            **{
                'iface' : configs['iface']
            }
        )

        # Set the behaviour
        self.behaviour = self.__configs['behaviour']
        self.logger.info(
            "Created a new Probe of type: %s" %self.type
        )
        return


    def _correlate(self, pkt):
        """
        This is the correlation algorithm that will look at the databases and
        check either the registry or the black list.

        :param pkt:             The read packet
        :return:
        """

        # Get the ip layer
        dest_mac        = pkt[ARP].hwdst
        src_mac         = pkt[ARP].hwsrc
        dest_ip         = pkt[ARP].pdst
        src_ip          = pkt[ARP].psrc

        dest_data = {
            'type'          : 'ARP|IP',
            'seq'           : self._packet_count,
            'time'          : time.asctime(
                time.localtime(
                    time.time()
                )
            ),
            'mac'           : dest_mac,
            'ip'            : dest_ip
        }

        src_data = {
            'type'          : 'ARP|IP',
            'seq'           : self._packet_count,
            'time'          : time.asctime(
                time.localtime(
                    time.time()
                )
            ),
            'mac'           : src_mac,
            'ip'            : src_ip
        }

        # We check the dehaviour
        if self.behaviour == PROBE_MONITORING:

            # We need to check the validity of the ip
            # Get the table
            unknown_table = self._database.get_table(
                'UNKNOWN_MAC'
            )
            known_table = self._database.get_table(
                'KNOWN_MAC'
            )
            src_pkt = known_table.search(
                Query().address == src_mac
            )
            dest_pkt = known_table.search(
                Query().address == dest_mac
            )
            if dest_pkt is None:

                # We have an unknown destination ip
                unknown_table.insert(
                    dest_data
                )
            if src_pkt is None:

                # We have an unknown destination ip
                unknown_table.insert(
                    src_data
                )

        # Just register the IP for logging
        elif self.behaviour == PROBE_OBSERVING:
            table = self._database.get_table(
                'MAC'
            )
            table.insert(
                src_data
            )
            table.insert(
                dest_data
            )
        return