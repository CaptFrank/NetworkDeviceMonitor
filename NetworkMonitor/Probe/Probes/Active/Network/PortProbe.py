"""

    :PortProbe:
    ==========

    :
    This is a probe that will scan for available ports on a
    device. This probe will use the nmap binary to ping each
    port.
    :

    :copyright: (c) 10/23/2015 by fpapinea.
    :license: BSD, see LICENSE for more details.

    Author:         fpapinea
    Version:        :1.0:
    Date:           10/23/2015
"""

"""
=============================================
Imports
=============================================
"""

import gc
import nmap
import psutil
from NetworkMonitor.Probe.Probe \
    import Probe, PLACEHOLDER_STRING

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

class PortProbe(Probe):
    """
    This is the user probe that scans what ports are on
    a specific system.

    extends: Probe
    """

    # The class name
    name        = "PortProbe"

    # The probe type
    type        = "Ports"

    # Description
    description = \
    "Gets the ports on the probe that is running."

    # Fields for filtering
    fields      = []

    # Groups
    groups      = [
        "ports",
        "prefetch",
        "reconnaissance"
    ]

    # Definition
    definition  = {}

    # Template
    template    = {}

    # Data
    data        = {}

    # Continuous flag
    continuous  = False

    def __init__(self, queue):

        return

    def setup(self):

        return

    def _run(self):

        return