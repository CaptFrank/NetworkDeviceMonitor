"""

    :PassiveNetworkProbe:
    ==========

    :
    This is the passive networking probe.
    We use this to probe the traffic in a passive methodology.
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

from NetworkMonitor.Probe.Probe \
    import Probe, PLACEHOLDER
from NetworkMonitor.Probe.NetworkProbe \
    import NetworkProbe

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

class PassiveNetworkProbe(NetworkProbe):
    """
    This is the derivative of the network probe and allows
    the network probe to be setup, ran and returned.

    This serves as an abstract class.

    extends: Network Probe
    """

    def __init__(self, type, iface, queue):
        """
        This is the constructor that will set the self
        object to the appropriate object type.

        :param type:        Probe type
        :param queue:       Application queue
        :return:
        """

        # Override the class
        NetworkProbe.__init__(self, type, iface, queue)

        # Register the type
        self._register_type(
            "passive",
            self
        )
        return