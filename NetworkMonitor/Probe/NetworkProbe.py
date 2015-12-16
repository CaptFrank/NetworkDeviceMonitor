"""

    :NetworkProbe:
    ==========

    :
    This is the class object that implements a PF_RING type
    queue to hold incoming data from the commonly used interface.
    We need this common resource pool to allow for multiple threads
    to act upon the accurately match packet type.
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

from NetworkMonitor.Probe.MutableProbe \
    import MutableProbe
from NetworkMonitor.Probe.Probes.Active.ActiveNetworkProbe \
    import ActiveNetworkProbe
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

class NetworkProbe(MutableProbe):
    """
    This is the base network probing class object.
    It contains the appropriate attributes of a network
    scanner, sniffer that are needed to allow for the
    appropriate traffic to be monitored.

    It is mutable to be made into an active or passive
    probing agent.

    extends: MutableProbe
    """
    """
    This the disk probe container that contains both the
    static probe and the dynamic probing agents.
    """

    # Check the probe types
    __types         = {
        "active"   : ActiveNetworkProbe,
        "passive"  : PassiveNetworkProbe
    }

    def __init__(self, type, queue):
        """
        This is the constructor that will set the self
        object to the appropriate object type.

        :param type:        Probe type
        :param queue:       Application queue
        :return:
        """

        # Override the class
        MutableProbe.__init__(self, self.__types)

        # Run the object
        self.run(type, queue)
        return