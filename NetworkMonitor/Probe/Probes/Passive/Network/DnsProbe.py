"""

    :DnsProbe:
    ==========

    :
    This is the DNS sniffing probe.
    This probe runs in the background and looks for DNS
    queries. Each D NS query is destructed into IP and
    DNS name. From which they are put into a local database.
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

import time
from netaddr import *
from tinydb import Query
from scapy.layers.dns import *

from NetworkMonitor.Storage.ProbeDb import \
    ProbeDb
from NetworkMonitor.Probe.Probes.Passive.Network.IpProbe \
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

class DnsProbe(IpProbe):
    """
    This is the class object that defines the probing agent.
    In this class we define the running method and what the
    local behaviour of the probe is.

    extends: IpProbe
    """

    # The class name
    name            = "DnsProbe"

    # The probe type
    type            = "DNS"

    # Description
    description     = \
    "This is the probe that will monitor the dns addresses " \
    "on the network and will correlate them to a db."

    # Groups
    groups          = [
        "dns",
        "network",
        "reconnaissance"
    ]

    # Layer filter
    layer           = DNS

    # ====================
    # Protected
    # ====================

    # Local database tables
    _tables         = [
        'KNOWN_DNS',
        'UNKNOWN_DNS',
    ]

    # ====================
    # Private
    # ====================

    # App configs
    __configs       = None

    # Time
    __date          = None

    def __setup_db(self):
        """
        Setup the probe specific database.
        :return:
        """
        # Create a database
        self.__database = ProbeDb(
            self.__configs['name']
        )

        # Setup the known database
        if self.behaviour == PROBE_MONITORING:

            # We need to check the already registered ips
            self.__database.setup_db(
                self._tables
            )

            # Get the table
            table = self.__database.get_table('KNOWN_DNS')

            # Add the entries to the internal db
            for dns in self.__configs['known']:

                # Add the Ips in the known table
                table.insert(
                    {
                        'type'          : 'DNS',
                        'address'       : dns,
                    }
                )
        elif self.behaviour == PROBE_OBSERVING:

            # Create a new table
            tables = [
                'DNS'
            ]

            # We need to check the already registered ips
            self.__database.setup_db(
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
        dst             = pkt[IP].dest
        src             = pkt[IP].src
        ip_len          = pkt[IP].len
        ip_chksum       = pkt[IP].chksum
        ip_version      = pkt[IP].version
        ip_id           = pkt[IP].id
        ip_ttl          = pkt[IP].ttl

        # Get the DNS name
        dns_name        = pkt[DNS]

        dns_data = {
            'type'          : 'DNS|IP',
            'seq'           : self._packet_count,
            'time'          : time.asctime(
                time.localtime(
                    time.time()
                )
            ),
            'dns'           : dns_name,
            'src'           : src,
            'dst'           : dst,
            'length'        : ip_len,
            'checksum'      : ip_chksum,
            'ttl'           : ip_ttl,
            'id'            : ip_id,
        }

        # We check the dehaviour
        if self.behaviour == PROBE_MONITORING:

            # We need to check the validity of the ip
            # Get the table
            unknown_table = self._database.get_table(
                'UNKNOWN_DNS'
            )
            known_table = self._database.get_table(
                'KNOWN_DNS'
            )
            pkt = known_table.search(
                Query().address == dns_name
            )
            if pkt is None:

                # We have an unknown destination ip
                unknown_table.insert(
                    dns_data
                )
        # Just register the IP for logging
        elif self.behaviour == PROBE_OBSERVING:
            table = self._database.get_table(
                'DNS'
            )
            table.insert(
                dns_data
            )
        return