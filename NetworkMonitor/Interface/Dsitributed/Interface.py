"""

    :Interface:
    ==========

    :
    This is the distributed interface to the MQTT broker which will
    host all the comms from all other nodes. This class will
    subscribe to all the interested topics. From each topic, we
    can get all relevant information.

    [Server] -----> [Interface] ------> [Topic 1] ---> [Broker]
                            |---------> [Topic 2] ----->|
                            |---------> [Topic 3] ----->|
                            |---------> [Topic 4] ----->|
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