"""

    :Mongo:
    ==========

    :
    This is the mongo database interface for the stats that
    are acquired in the applications. Inherently this database
    is not a persistent database. We use this as a caching
    mechanism.
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

from mongoengine import *
from ..Base.Singleton import Singleton


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

class MongoInteraface(object, Singleton):
    """
    This class is the definition to our mongo db storage engine.
    We use this class to create and object that sustains a connection
    to the mongodb.

    This object is also a singleton object that sustains the one connection
    throughout the application.

    This is where we also register the ORM objects.
    """

    """
    =========================================
    Constants
    =========================================
    """

    # Name
    __name      = None

    # Address
    __configs   = None

    # Handles
    __handles   = []

    """
    =========================================
    Imports
    =========================================
    """

    # Import Persistent tables
    import Tables.Persistent.Configs
    import Tables.Persistent.Access
    import Tables.Persistent.Device
    import Tables.Persistent.History

    # Import Cached / Temporary tables
    import Tables.Temporary.Cache
    import Tables.Temporary.Stats

    def __init__(self, name=None, configs=None):
        """
        This is the default constructor for the class.

        :param name:        The name of the interface
        :param configs:     The connection configs

            configs = {

                "host"      :   "localhost",
                "port"      :   9000,
                "password"  :   "test",
                "username"  :   "test"
            }


        :return:
        """

        # Set internals
        self.__name     = name
        self.__configs  = configs

        # Override the base class
        Singleton.__init__(self)
        return

    def connect(self, db):
        """
        This connects the interface to the mongodb server.

        :param db:      The database to connect to
        :return:
        """

        # Sanity check
        if self.__address and (db is not None):

            # Connect to all dbs
            for item in db:

                if item not in self.__handles:
                    # registers the database
                    register_connection(item, **self.__configs)
                    self.__handles.append(db)
            return True

        # There has been a problem
        else:
            return False

    def disconnect(self, db):
        """
        This disconnects the interface to the mongodb server.

        :param db:      The database to disconnect from
        :return:
        """

        # Sanity check
        if self.__address and (db is not None):

            # Connect to all dbs
            for item in db:

                if db in self.__handles:
                    # Disconnect and delete
                    connection.disconnect(db)
                    del self.__handles[db]
            return True

        # A problem occurred.
        else:
            return False



