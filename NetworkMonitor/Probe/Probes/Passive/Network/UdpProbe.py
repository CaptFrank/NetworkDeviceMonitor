"""
    :UdpProbe:
    ==========

    :
    This is an udp probe that will keep track of the device IPs and ports that are
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

from scapy.layers.all import *
from NetworkMonitor.Probe.Probes.Passive.Network.TcpProbe \
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

class UdpProbe(TcpProbe):
    """
    This is the ip probe that is a mutable probe. It sniffs the
    ip addresses of all IP packets and correlates the IPs to an
    internal JSON database containing the previous registered IPs.
    The use can provide a previously defined database, that will then
    serve as a filter. In which case the added IPs are reported as foreign.
    If the database is not provided, the IPs are registered and reported
    as alive / dead.

    extends: IpProbe
    """

    # The class name
    name            = "UdpProbe"

    # The probe type
    type            = "UDP"

    # Description
    description     = \
    "This is the probe that will monitor the udp addresses " \
    "on the network and will correlate them to a db."

    # Groups
    groups          = [
        "udp",
        "network",
        "reconnaissance"
    ]

    # Layer filter
    layers          = [UDP, IP]

    # ====================
    # Protected
    # ====================

    # Local database tables
    _tables         = [
        'KNOWN_IP',
        'UNKNOWN_IP',
        'KNOWN_PORT',
    ]

    # ====================
    # Private
    # ====================

    # App configs
    __configs       = None

    # Time
    __date          = None

    def _correlate(self, pkt):
        """
        This is the correlation algorithm that will look at the databases and
        check either the registry or the black list.

        :param pkt:             The read packet
        :return:
        """

        # Get the ip layer
        dst_ip              = pkt[IP].dst
        dst_port            = pkt[UDP].dport
        src_ip              = pkt[IP].src
        src_port            = pkt[UDP].sport
        ip_len              = pkt[IP].len
        ip_chksum           = pkt[IP].chksum
        ip_version          = pkt[IP].version
        ip_id               = pkt[IP].id
        ip_ttl              = pkt[IP].ttl

        # Correlate IP
        self._correlate_ip(
                src_ip,     src_port,
                dst_ip,     dst_port,
                ip_len,     ip_chksum,
                ip_version, ip_id,
                ip_ttl
        )
        return

