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
from scapy.layers.inet import *

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

    # Fields for filtering
    fields          = []

    # Groups
    groups          = [
        "ip",
        "network",
        "reconnaissance"
    ]

    # Definition
    definition      = {}

    # Template
    template        = {}

    # Data
    data            = {}

    # Layer filter
    layer           = IP

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
        self.__setup_db()
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
        self.__packets_read += 1
        self.__correlate(packet)
        return

    def report(self):
        """
        Generate a report based on either the registered ips or the
        ip correlated to the database.

        :param data:
        :return:
        """

        if self.__configs['behaviour'] == 'MONITOR':

            # We need to return the Unknown vs. Known tables
            known = self.__database.get_table('KNOWN')
            unknown = self.__database.get_table('UNNKNOWN')

            # Get the data
            known_addresses = known.all()
            unknown_addresses = unknown.all()

            # Merge the results and return them
            return {
                'known'     : known_addresses,
                'unknown'   : unknown_addresses
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
                'KNOWN',
                'UNKNOWN'
            ]

            # We need to check the already registered ips
            self.__database.setup_db(
                tables
            )

            # Get the table
            table = self.__database.get_table('KNOWN')

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
        destination     = pkt[IP].dest
        source          = pkt[IP].src

        # We check the dehaviour
        if self.__configs['behaviour'] == 'MONITOR':

            # We need to check the validity of the ip
            # Get the table
            known_table = self.__database.get_table(
                'KNOWN'
            )
            src_pkt = known_table.search(
                Query().address == source
            )
            dest_pkt = known_table.search(
                Query().address == destination
            )
            unknown_table = self.__database.get_table(
                'UNKNOWN'
            )

            if dest_pkt is None:

                # We have an unknown destination ip
                unknown_table.insert(
                    {
                        'type'          : 'IP',
                        'seq'           : self.__packets_read,
                        'time'          : time.asctime(
                            time.localtime(
                                time.time()
                            )
                        ),
                        'address'       : destination,
                    }
                )
            elif src_pkt is None:

                # We have an unknown destination ip
                unknown_table.insert(
                    {
                        'type'          : 'IP',
                        'seq'           : self.__packets_read,
                        'time'          : time.asctime(
                            time.localtime(
                                time.time()
                            )
                        ),
                        'address'       : source,
                    }
                )

        # Just register the IP for logging
        else:
            table = self.__database.get_table(
                'IP'
            )
            table.insert(
                {
                    'type'          : 'IP',
                    'seq'           : self.__packets_read,
                    'time'          : time.asctime(
                        time.localtime(
                            time.time()
                        )
                    ),
                    'address'       : source,
                }
            )
            table.insert(
                {
                    'type'          : 'IP',
                    'seq'           : self.__packets_read,
                    'time'          : time.asctime(
                        time.localtime(
                            time.time()
                        )
                    ),
                    'address'       : destination,
                }
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



