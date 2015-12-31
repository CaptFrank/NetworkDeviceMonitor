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

    # Probe type
    type      = 'IpProbe'

    # Layer filter
    layer     = 'IP'

    def __init__(self, iface, queue):
        """
        This is the default constructor for the class.
        We supply the iface and the queue.

        :param iface:       The iface that needs to be monitored
        :param queue:       The application queue
        :return:
        """

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

        :param packet:
        :return:
        """
        return

    def report(self, data):
        """
        Generate a report based on either the registered ips or the
        ip correlated to the database.

        :param data:
        :return:
        """
        return

    def __correlate_ip(self, packet):

        return

    def __register_db(self, db):

        return
