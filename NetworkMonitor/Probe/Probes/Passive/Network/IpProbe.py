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

from netaddr import *
from NetworkMonitor.Base.Reader import \
    Reader
from NetworkMonitor.Storage.ProbeDb import \
    ProbeDb
from NetworkMonitor.Probe.Probes.Passive.PassiveNetworkProbe \
    import PassiveNetworkProbe

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

    # ====================
    # Public
    # ====================

    # Probe type
    type            = 'IpProbe'

    # Layer filter
    layer           = 'IP'

    # ====================
    # Private
    # ====================

    # Config Reader
    __reader        = None

    # Database
    __database      = None

    # Metrics
    __packets_read   = 0


    def __init__(self, iface, queue, file=None):
        """
        This is the default constructor for the class.
        We supply the iface and the queue.

        :param iface:       The iface that needs to be monitored
        :param queue:       The application queue
        :param file:        A file that contains the known ips
        :return:
        """

        # Setup the probe db.
        self.__setup_db(file)

        # Register the probe type as a passive probe
        PassiveNetworkProbe.__init__(
            self,
            self.type,
            iface,
            queue
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

    def __setup_db(self, file):
        """
        Setup the probe specific database.

        :param file:        The config file
        :return:
        """
        # Create a database
        self.__database = ProbeDb()

        # Read the file and the known ips
        if file is not None:

            # We have a valid list read the configs
            self.__reader = Reader()
            configs = self.__reader.read(
                file
            )

            # Convert to dict
            configs_dict = dict(configs)

            # Create a db with the known ips
            self.__database.setup_db(
                configs_dict['IP']
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