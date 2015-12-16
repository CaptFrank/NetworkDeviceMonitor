"""

    :Probe:
    ==========

    :
    This is the worker process that will
    continuously scan the network for new devices and
    include the results in an indexed database (Mongodb).

    This process also issues alarms to the alarm queue based on
    access control lists identified in the ACL db.
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

from NetworkMonitor.Probe.Probe \
    import Probe, PLACEHOLDER

"""
=============================================
Constants
=============================================
"""

# Program Attributes
__author__  =   "gammaRay"
__version__ =   "1.0"
__date__    =   "9/28/2015"

PLACEHOLDER =   ""

"""
=============================================
Source
=============================================
"""

class HostProbe(Probe):
    """
    This is just a namespace thing... We dont actually define
    anything in this class.
    """
    pass
