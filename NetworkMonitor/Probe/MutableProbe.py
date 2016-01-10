"""

    :MutableProbe:
    ==========

    :
    This is the base class for mutable probes, such as
    any probe that could report dynamic or static data
    to the main engine.
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

import logging

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

class MutableProbe(object):
    """
    This is the mutable probe class that contains the possible
    mutable types and contains them into one entity that can be
    set and instantiated externally.

    extends: Probe
    """

    # Default types container
    __types         = {
        "none"      : None
    }

    # The logger object
    logger        = None

    def __init__(self, types, **kwargs):
        """
        This is the default constructor for the class container.
        We use this constructor to register the possible class types.

        :param types:           The probe types in a dict.
        :return:
        """

        # Register the types
        self.__types.update(
            types
        )

        self.logger = logging.getLogger(
            "MutableProbe"
        )

        return

    def run(self, type, queue, **kwargs):
        """
        This method returns the appropriate class type that
        is needed based on the type passed.

        :param type:            Probe type
        :param queue:           Application queue
        :return:
        """

        if type in self.__types.keys():

            # Class type registered.
            self.__class__ = self.__types[type]
        else:

            # Class type not registered.
            self.__class__ = self.__types['none']

        # Return the mutated class object.
        return self.__init__(queue, **kwargs)