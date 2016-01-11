"""

    :IPProbe:
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

import gc
#from netaddr import *
from NetworkMonitor.Storage.ProbeDb import \
    ProbeDb
from NetworkMonitor.Probe.Probes.Passive.PassiveNetworkProbe \
    import PassiveNetworkProbe, PLACEHOLDER_DICT, \
    PLACEHOLDER_STRING, PLACEHOLDER_ARRAY

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
    name        = "IpProbe"

    # The probe type
    type        = "IP"

    # Description
    description = \
    "This is the probe that will monitor the ip addresses " \
    "on the network and will correlate them to a db."

    # Fields for filtering
    fields      = []

    # Groups
    groups      = [
        "ip",
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
    layer           = 'IP'

    # ====================
    # Private
    # ====================

    # Database
    __database      = None

    # Metrics
    __packets_read  = 0

    # App configs
    __configs       = None

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
        gc.enable()
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

        return

    def report(self, data):
        """
        Generate a report based on either the registered ips or the
        ip correlated to the database.

        :param data:
        :return:
        """
        return

    def __setup_db(self):
        """
        Setup the probe specific database.
        :return:
        """
        # Create a database
        self.__database = ProbeDb(
            self.get_db_name(
                self.__configs
            )
        )

        # Setup the known database
        if self.__configs['behaviour'] == 'MONITOR':

            # Create a new db table
            table = {
                'known'     : self.__configs['known']
            }

            # We need to check the already registered ips
            self.__database.setup_db(
                table
            )

        return

    def __correlate_ip(self, packet):
        """
        This is the correlation algorithm that will look at the databases and
        check either the registry or the black list.

        :param packet:
        :return:
        """

        return