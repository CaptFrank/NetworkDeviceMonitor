"""

    :IpProbe:
    ==========

    :
    This is an IP probe that will keep track of the device IPs that are
    sending or receiving in the network. It also keeps track of
    the IPs that are alive and runnign as well as the IPs that are
    not running -- or dead.
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
from scapy.layers.all import *

from NetworkMonitor.Storage.ProbeDb \
    import ProbeDb
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

class IpProbe(PassiveNetworkProbe):
    """
    This is the ip probe that is a mutable probe. It sniffs the
    ip addresses of all IP packets and correlates the IPs to an
    internal JSON database containing the previous registered IPs.
    The use can provide a previously defined database, that will then
    serve as a filter. In which case the added IPs are reported as foreign.
    If the database is not provided, the IPs are registered and reported
    as alive / dead.

    extends: PassiveNetworkProbe
    """

    # The class name
    name            = "IpProbe"

    # The probe type
    type            = "IP"

    # Description
    description     = \
    "This is the probe that will monitor the ip addresses " \
    "on the network and will correlate them to a db."

    # Groups
    groups          = [
        "ip",
        "network",
        "reconnaissance"
    ]

    # Layer filter
    layer           = IP

    # ====================
    # Protected
    # ====================

    # Local database tables
    _tables         = [
        'KNOWN_IP',
        'UNKNOWN_IP'
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

        self.logger.info(
            "Created a new Probe of type: %s" %self.type
        )
        return

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
            self._database.setup_db(
                self._tables
            )

            # Get the table
            table = self.__database.get_table('KNOWN_IP')

            # Add the entries to the internal db
            for ip in self.__configs['known']:

                # We need to convert it into a supported IP
                # This IP can be a subnet IP that needs to be put into a list
                address = self.__get_address(
                    ip
                )

                if type(address) is list():
                    for ip in address:

                        # Add the Ips in the known table
                        table.insert(
                            {
                                'type'          : 'IP',
                                'address'       : ip,
                            }
                        )
                else:
                    # Add the Ips in the known table
                    table.insert(
                        {
                            'type'          : 'IP',
                            'address'       : ip,
                        }
                    )
        elif self.behaviour == PROBE_OBSERVING:

            # Create a new table
            tables = [
                'IP'
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
        dest_mac        = pkt[Ether].dest
        src_mac         = pkt[Ether].src
        dest_ip         = pkt[IP].dest
        src_ip          = pkt[IP].src

        dest_data = {
            'type'          : 'IP|MAC',
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
            'type'          : 'IP|MAC',
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
                'UNKNOWN_IP'
            )
            known_table = self._database.get_table(
                'KNOWN_IP'
            )
            src_pkt = known_table.search(
                Query().address == src_ip
            )
            dest_pkt = known_table.search(
                Query().address == dest_ip
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
                'IP'
            )
            table.insert(
                src_data
            )
            table.insert(
                dest_data
            )
        return

    def __get_address(self, ip):
        """
        This is the method that is used to get the ip address
        or network that is needed in the probing.

        :param ip:              The ip address or the ip network
        :return:
        """

        # Container
        addresses = []

        # Generator
        generate_ip = lambda address : addresses.append(
                {
                    'v4'    :   str(
                        address.ipv4()
                    ),
                    'v6'    :   str(
                        address.ipv6()
                    )
                }
        )

        # We have a network to generate
        if '/' in ip:
            network = list(IPNetwork(ip))
            for address in network:
                generate_ip(address)
            return addresses
        else:
            return ip



