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
    name        = "MacProbe"

    # The probe type
    type        = "MAC"

    # Description
    description = \
    "This is the probe that will monitor the mac addresses " \
    "on the network and will correlate them to a db."

    # Fields for filtering
    fields      = []

    # Groups
    groups      = [
        "mac",
        "network",
        "reconnaissance"
    ]

    # Definition
    definition  = {}

    # Template
    template    = {}

    # Data
    data        = {}

    # Layer filter
    layer           = 'Ethernet'

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
            mac = self.__database.get_table('MAC')
            mac_addresses = mac.all()

            return {
                'mac'        : mac_addresses
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
            for mac in self.__configs['known']:

                # Add the Ips in the known table
                table.insert(
                    {
                        'type'          : 'MAC',
                        'address'       : mac,
                    }
                )
        else:

            # Create a new table
            tables = [
                'MAC'
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
        destination     = pkt[Ether].dest
        source          = pkt[Ether].src

        # We check the dehaviour
        if self.__configs['behaviour'] == 'MONITOR':

            # We need to check the validity of the ip
            # Get the table
            unknown_table = self.__database.get_table(
                'UNKNOWN'
            )
            src_pkt = unknown_table.search(
                Query().address == source
            )
            dest_pkt = unknown_table.search(
                Query().address == destination
            )

            if dest_pkt is None:

                # We have an unknown destination ip
                unknown_table.insert(
                    {
                        'type'          : 'MAC',
                        'seq'           : self.__packets_read,
                        'time'          : time.asctime(
                            time.localtime(
                                time.time()
                            )
                        ),
                        'address'       : dest_pkt,
                    }
                )
            elif src_pkt is None:

                # We have an unknown destination ip
                unknown_table.insert(
                    {
                        'type'          : 'MAC',
                        'seq'           : self.__packets_read,
                        'time'          : time.asctime(
                            time.localtime(
                                time.time()
                            )
                        ),
                        'address'       : src_pkt,
                    }
                )

        # Just register the IP for logging
        else:
            table = self.__database.get_table(
                'MAC'
            )
            table.insert(
                {
                    'type'          : 'MAC',
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
                    'type'          : 'MAC',
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