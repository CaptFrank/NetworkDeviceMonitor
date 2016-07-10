"""

    :NtpProbe:
    ============

    :
    This is the NTP probe that is used in the cases where a device needs
    to probe any NTP flows.
    :

    :copyright: (c) 2016-02-11 by francispapineau.
    :license: BSD, see LICENSE for more details.

    Author:         gammaray
    Version:        :1.0:
    Date:           2016-06-12
    
"""

"""
=============================================
Imports
=============================================
"""

import time
from netaddr import *
from tinydb import Query
from scapy.layers.ntp import *

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
__project__ = "NetworkMonitor"
__author__ = "francispapineau"
__version__ = "1.0"
__date__ = "2016-06-12"

"""
=============================================
Source
=============================================
"""