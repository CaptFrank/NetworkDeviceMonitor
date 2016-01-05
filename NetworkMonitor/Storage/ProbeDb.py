"""

    :ProbeDb:
    ==========

    :
    This is the probe database engine. It is needed
    to store and cache some data from the plugin modules.
    This module is mutable and can be wrapped to any type
    of database needed (i.e. key - value db, string db, cache, etc...)
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

from tinydb import \
    TinyDB
from tinydb.storages import \
    MemoryStorage

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

class ProbeDb(TinyDB):
    """
    This is the probe database engine that is contained in memory.
    No disk IO is needed to cache data, thus the speed of this
    database is fast. We use this database engine as a localized
    resource to each plugin.

    For instance the IpPlugin will use this probe database,
    as a caching mechanism for the IPs that are read and registered.

    extends: TinyDB
    """

    def __init__(self):
        """
        This is the constructor for the class.

        :param plugin_name:     The plugin name that needs this db.
        :param probe_name:      The probe name that needs this db.
        :return:
        """

        # Override the base class
        TinyDB.__init__(
            self,
            storage=MemoryStorage
        )
        return

    def setup_db(self, data):
        """
        Sets up the database with either no data
        or with passed data.

        The data needs to be formatted in a dict form.
        i.e.
            data = {
                    "table 1" : {
                        "data 1" : data,
                        "data 2" : data
                        },
                    "table 2" : {
                        "data 1" : data,
                        "data 2" : data
                        }
                    }

        :param data:            The data needed to start the database
        :return:
        """

        # If there is no data return
        if data is None:
            return

        # Setup the tables and data
        for name in data.keys():
            table = self.table(
                name
            )

            # Setup data
            for key, data in zip(
                    data['table'].keys(),
                    data['table'].values()
            ):
                table.insert(
                    {
                        key,
                        data
                    }
                )
        return