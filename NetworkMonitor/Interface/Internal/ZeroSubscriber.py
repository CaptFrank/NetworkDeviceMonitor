"""

    :ZeroSubscriber:
    ==========

    :
    This is the subscriber that looks for all Rabbitmq queues.
    Once it has found a queue, it then reads content that is in the queue.
    Once the size limit is reached, the package is then sent to the logstash
    with the format defined in the Logstash interface object.

    The search algorithm that is utilized to find queues and information,
    is a round robin style algorithm.
    :

    :copyright: (c) 2015-10-23 by gammaRay.
    :license: BSD, see LICENSE for more details.

    Author:         gammaRay
    Version:        :1.0:
    Date:           9/30/2015
"""

"""
=============================================
Imports
=============================================
"""

import zmq

"""
=============================================
Constants
=============================================
"""


# Program Attributes
__author__          =   "gammaRay"
__version__         =   "1.0"
__date__            =   "9/28/2015"

"""
=============================================
Source
=============================================
"""