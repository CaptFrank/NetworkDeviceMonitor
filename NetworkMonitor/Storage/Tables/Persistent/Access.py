"""

    :Access:
    ==========

    :
    This is the module that defines access tokens,
    either unknown or known access tokens.
    :

    :copyright: (c) 15-09-30 by francispapineau.
    :license: BSD, see LICENSE for more details.

    Author:         francispapineau
    Version:        :version: #TODO
    Date:           15-09-30
    
"""

"""
=============================================
Imports
=============================================
"""

from mongoengine import *

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

class Access(Document):
    """
    This is the overall accessing document that holds
    both valid accesses and invalid accesses within the network.
    """

    # Database Access Name
    name        = StringField(
        required=True
    )

    # The db uuid
    uuid        = UUIDField(
        required=True
    )

    # Date created
    created     = DateTimeField(
        required=True
    )

    # Date updated
    updated     = DateTimeField()

    # Metadata
    meta        = {
        'allow_inheritance'     : True,
        'collection'            : 'access',
        'ordering'              : [
            '-uuid',
            '-name'
        ],
        'indexes'               : [
            '#name',
            '#uuid',
            '#created',
            '#updated'
        ]

    }
