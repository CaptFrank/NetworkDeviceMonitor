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

import gc
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
class MacProbe(NetworkProbe):
    """
    This is the MAC probe that will be used to poll
    the network interface and sniff out the MAC addresse.
    Then is reports them in the data record sent to the
    message engine.

    extends: NetworkProbe
    """