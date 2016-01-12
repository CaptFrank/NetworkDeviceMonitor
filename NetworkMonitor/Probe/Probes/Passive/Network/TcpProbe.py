"""
    :TcpProbe:
    ==========

    :
    This is an TCP probe that will keep track of the device IPs and ports that are
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

from NetworkMonitor.Probe.Probes.Passive.Network.IpProbe import *

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

class TcpProbe(IpProbe):
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
    name            = "TcpProbe"

    # The probe type
    type            = "TCP"

    # Description
    description     = \
    "This is the probe that will monitor the tcp addresses " \
    "on the network and will correlate them to a db."

    # Groups
    groups          = [
        "tcp",
        "network",
        "reconnaissance"
    ]

    # Layer filter
    layer           = TCP

    # ====================
    # Private
    # ====================

    # Database
    __database      = None

    # Metrics
    __packets_read  = 0

    # App configs
    __configs       = None

    # Time
    __date          = None

    def report(self):
        """
        Generate a report based on either the registered ips or the
        ip correlated to the database.

        :param data:
        :return:
        """

        if self.__configs['behaviour'] == 'MONITOR':

            # We need to return the Unknown vs. Known tables
            known_ip = self.__database.get_table('KNOWN_IP')
            known_port = self.__database.get_table('KNOWN_PORT')
            unknown = self.__database.get_table('UNNKNOWN')

            # Get the data
            unknown = unknown.all()
            known_addresses = known_ip.all()
            known_ports = known_port.all()

            # Merge the results and return them
            return {
                'known'     : {
                    'ip'    : known_addresses,
                    'port'  : known_ports
                },
                'unknown'   : unknown,
            }
        else:

            # Return all the ips
            ip = self.__database.get_table('IP')
            ip_addresses = ip.all()

            return {
                'ip'        : ip_addresses
            }

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
        if self.__configs['behaviour'] == 'MONITOR':

            # Create a new db table
            tables = [
                'KNOWN_IP',
                'KNOWN_PORTS',
                'UNKNOWN',
            ]

            # We need to check the already registered ips
            self.__database.setup_db(
                tables
            )

            # Get the table
            table = self.__database.get_table('KNOWN_IP')

            # Add the entries to the internal db
            for ip in self.__configs['known_ip']:

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
            # Get the table
            table = self.__database.get_table('KNOWN_PORT')

            # Add the entries to the internal db
            for port in self.__configs['known_port']:

                # Add the Ips in the known table
                table.insert(
                    {
                        'type'          : 'PORT',
                        'port'          : port,
                    }
                )
        else:

            # Create a new table
            tables = [
                'IP'
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
        destination         = pkt[IP].dest
        destination_port    = pkt[TCP].dport
        source              = pkt[IP].src
        source_port         = pkt[TCP].sport

        # Correlate IP
        self.__correlate_ip(
                source, source_port,
                destination, destination_port
        )
        return

    def __correlate_ip(self, src, src_port, dst, dst_port):
        """
        Correlate the ip addresses.

        :return:
        """

        # We check the dehaviour
        if self.__configs['behaviour'] == 'MONITOR':

            # We need to check the validity of the ip
            # Get the table
            known_ip_table = self.__database.get_table(
                'KNOWN_IP'
            )
            unknown_table = self.__database.get_table(
                'UNKNOWN'
            )

            known_port_table = self.__database.get_table(
                'KNOWN_PORT'
            )

            # Address
            src_pkt = known_ip_table.search(
                Query().address == src
            )
            dst_pkt = known_ip_table.search(
                Query().address == dst
            )

            # Port
            src_port_q = known_port_table.search(
                Query().address == src_port
            )
            dst_port_q = known_port_table.search(
                Query().address == dst_port
            )


            if (dst_pkt is None) or \
                    (dst_port_q is None):

                # We have an unknown destination ip
                unknown_table.insert(
                    {
                        'type'          : 'IP|PORT',
                        'seq'           : self.__packets_read,
                        'time'          : time.asctime(
                            time.localtime(
                                time.time()
                            )
                        ),
                        'address'       : dst,
                        'port'          : dst_port
                    }
                )
            elif (src_pkt is None) or \
                    (src_port_q is None):

                # We have an unknown destination ip
                unknown_table.insert(
                    {
                        'type'          : 'IP|PORT',
                        'seq'           : self.__packets_read,
                        'time'          : time.asctime(
                            time.localtime(
                                time.time()
                            )
                        ),
                        'address'       : src,
                        'port'          : src_port
                    }
                )

        # Just register the IP for logging
        else:
            table = self.__database.get_table(
                'IP'
            )
            table.insert(
                {
                    'type'          : 'IP|PORT',
                    'seq'           : self.__packets_read,
                    'time'          : time.asctime(
                        time.localtime(
                            time.time()
                        )
                    ),
                    'address'       : src,
                    'port'          : src_port
                }
            )
            table.insert(
                {
                    'type'          : 'IP|PORT',
                    'seq'           : self.__packets_read,
                    'time'          : time.asctime(
                        time.localtime(
                            time.time()
                        )
                    ),
                    'address'       : dst,
                    'port'          : dst_port
                }
            )
        return
