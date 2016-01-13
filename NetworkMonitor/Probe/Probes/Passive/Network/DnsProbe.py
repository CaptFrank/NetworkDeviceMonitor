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
        else:

            # Create a new table
            tables = [
                'DNS'
            ]

            # We need to check the already registered ips
            self.__database.setup_db(
                tables
            )
        return

    def __correlate(self, pkt):
        """
        This is the correlation algorithm that will look at the databases and
        check either the registry or the black list.

        :param pkt:             The read packet
        :return:
        """

        # Get the ip layer
        dest            = pkt[IP].dest
        src             = pkt[IP].src

        # Get the ports
        src_port        = pkt[TCP].sport
        dest_port       = pkt[TCP].dport

        # Get the DNS name
        dns_name        = pkt[DNS]

        # Correlate IP
        self.__correlate_ip(
                source, source_port,
                destination, destination_port
        )
        return