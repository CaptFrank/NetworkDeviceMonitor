"""

    :MacProbe:
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

import time
from netaddr import *
from tinydb import Query
from scapy.layers.inet6 import *

from NetworkMonitor.Storage.ProbeDb import \
    ProbeDb
from NetworkMonitor.Probe.Probes.Passive.PassiveNetworkProbe \
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
class MacProbe(PassiveNetworkProbe):
    """
    This is the MAC probe that will be used to poll
    the network interface and sniff out the MAC addresse.
    Then is reports them in the data record sent to the
    message engine.

    extends: NetworkProbe
    """

    # The class name
    name            = "MacProbe"

    # The probe type
    type            = "MAC"

    # Description
    description     = \
    "This is the probe that will monitor the mac addresses " \
    "on the network and will correlate them to a db."

    # Groups
    groups          = [
        "mac",
        "network",
        "reconnaissance"
    ]

    # Layer filter
    layers          = [Ether, IP]

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
    _configs        = None

    # Time
    _date           = None

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
        self._configs = configs
        self._configs['name'] = self.name

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
        self.logger.info(
            "Created a new Probe of type: %s" %self.type
        )
        return

    def _setup_db(self):
        """
        Setup the probe specific database.
        :return:
        """
        # Create a database
        self._database = ProbeDb(
            self._configs['name']
        )

        # Setup the known database
        if self.behaviour == PROBE_MONITORING:

            # We need to check the already registered ips
            self._database.setup_db(
                self._tables
            )

            # Get the table
            table = self._database.get_table('KNOWN_MAC')

            # Add the entries to the internal db
            for mac in self._configs['known']:

                # Add the Ips in the known table
                table.insert(
                    {
                        'type'          : 'MAC',
                        'address'       : mac,
                    }
                )
        elif self.behaviour == PROBE_OBSERVING:

            # Create a new table
            tables = [
                'MAC'
            ]

            # We need to check the already registered ips
            self._database.setup_db(
                tables
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
        dest_mac        = pkt[Ether].dst
        src_mac         = pkt[Ether].src
        type_mac        = pkt[Ether].type
        dest_ip         = pkt[IP].dst
        src_ip          = pkt[IP].src
        ip_len          = pkt[IP].len
        ip_chksum       = pkt[IP].chksum
        ip_version      = pkt[IP].version
        ip_id           = pkt[IP].id
        ip_ttl          = pkt[IP].ttl

        dest_data = {
            'type'          : 'IP|MAC',
            'seq'           : self._packet_count,
            'time'          : time.asctime(
                time.localtime(
                    time.time()
                )
            ),
            'mac'           : dest_mac,
            'mactype'       : type_mac,
            'length'        : ip_len,
            'checksum'      : ip_chksum,
            'ttl'           : ip_ttl,
            'id'            : ip_id,
            'ip'            : dest_ip,
            'ver'           : ip_version
        }

        src_data = {
            'type'          : 'IP|MAC',
            'seq'           : self._packet_count,
            'time'          : time.asctime(
                time.localtime(
                    time.time()
                )
            ),
            'mac'           : src_mac,
            'mactype'       : type_mac,
            'length'        : ip_len,
            'checksum'      : ip_chksum,
            'ttl'           : ip_ttl,
            'id'            : ip_id,
            'ip'            : src_ip,
            'ver'           : ip_version

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