"""

    :__init__.py:
    ==========

    :
    Contains a maintained database of probe types that are
    accessible at the plugin level.
    :

    :copyright: (c) 9/28/2015 by gammaRay.
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

from .DhcpProbe import *
from .DnsProbe import *
from .HttpProbe import *
from .IpProbe import *
from .MacProbe import *
from .TcpProbe import *
from .ArpProbe import *
from .IcmpProbe import *

"""
=============================================
Constants
=============================================
"""

# Program Attributes
__author__  =   "gammaRay"
__version__ =   "1.0"
__date__    =   "9/28/2015"

PASSIVE_NETWORK_PROBES = {
    'DHCPProbe'     : DHCPProbe,
    'DnsProbe'      : DnsProbe,
    'HttpProbe'     : HttpProbe,
    'TcpProbe'      : TcpProbe,
    'IpProbe'       : IpProbe,
    'MacProbe'      : MacProbe,
    'IcmpProbe'     : IcmpProbe,
    'ArpProbe'      : ArpProbe,
}