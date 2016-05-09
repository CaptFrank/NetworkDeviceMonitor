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

class TcpProbe(IpProbe):
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
    layers          = [TCP, IP]

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
    _configs       = None

    # Time
    _date          = None

    def _setup_db(self):
        """
        Setup the probe specific database.
        :return:
        """
        # Create a database
        self._database = ProbeDb(
            self._configs['name']
        )

        # Setup the known database
        if self.behaviour == PROBE_MONITORING:

            # We need to check the already registered ips
            self._database.setup_db(
                self._tables
            )

            # Get the table
            table = self._database.get_table('KNOWN_IP')

            # Add the entries to the internal db
            for ip in self._configs['known_ip']:

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
            table = self._database.get_table('KNOWN_PORT')

            # Add the entries to the internal db
            for port in self._configs['known_port']:

                # Add the Ips in the known table
                table.insert(
                    {
                        'type'          : 'PORT',
                        'port'          : port,
                    }
                )
        elif self.behaviour == PROBE_OBSERVING:

            # Create a new table
            tables = [
                'TCP'
            ]

            # We need to check the already registered ips
            self._database.setup_db(
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
        dst_ip              = pkt[IP].dst
        dst_port            = pkt[TCP].dport
        src_ip              = pkt[IP].src
        src_port            = pkt[TCP].sport
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

    def _correlate_ip(self, src, src_port, dst, dst_port,
                      ip_len, ip_chksum, ip_version, ip_id, ip_ttl):
        """
        Correlate the ip addresses.

        :return:
        """

        dest_data = {
            'type'          : 'IP|PORT',
            'seq'           : self._packet_count,
            'time'          : time.asctime(
                time.localtime(
                    time.time()
                )
            ),
            'ip'            : dst,
            'port'          : dst_port,
            'length'        : ip_len,
            'checksum'      : ip_chksum,
            'ttl'           : ip_ttl,
            'id'            : ip_id,
            'version'       : ip_version
        }

        src_data = {
            'type'          : 'IP|PORT',
            'seq'           : self._packet_count,
            'time'          : time.asctime(
                time.localtime(
                    time.time()
                )
            ),
            'ip'            : src,
            'port'          : src_port,
            'length'        : ip_len,
            'checksum'      : ip_chksum,
            'ttl'           : ip_ttl,
            'id'            : ip_id,
            'version'       : ip_version
        }

        # We check the dehaviour
        if self.behaviour == PROBE_MONITORING:

            # We need to check the validity of the ip
            # Get the table
            known_ip_table = self._database.get_table(
                'KNOWN_IP'
            )
            unknown_table = self._database.get_table(
                'UNKNOWN_IP'
            )
            known_port_table = self._database.get_table(
                'KNOWN_PORT'
            )

            # Address
            src_pkt_q = known_ip_table.search(
                Query().address == src
            )
            dst_pkt_q = known_ip_table.search(
                Query().address == dst
            )

            # Port
            src_port_q = known_port_table.search(
                Query().address == src_port
            )
            dst_port_q = known_port_table.search(
                Query().address == dst_port
            )

            if (dst_pkt_q is None) or \
                    (dst_port_q is None):

                # We have an unknown destination ip
                unknown_table.insert(
                    dest_data
                )
            elif (src_pkt_q is None) or \
                    (src_port_q is None):

                # We have an unknown destination ip
                unknown_table.insert(
                    src_data
                )

        # Just register the IP for logging
        elif self.behaviour == PROBE_OBSERVING:
            table = self._database.get_table(
                'TCP'
            )
            table.insert(
                src_data
            )
            table.insert(
                dest_data
            )
        return
