"""

    :Test:
    ==========

    :
    This is a test plugin that is implemented
    only to test both the plugin architecture and
    the messaging queue (i.e. Rabbitmq)
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

from yapsy.IPlugin import IPlugin

from NetworkMonitor.Base.Plugin \
    import Plugin
from NetworkMonitor.Interface.Internal.RabbitPublisher \
    import RabbitmqPublisher


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

class RabbitTestPlugin(Plugin, IPlugin):
    """
    This class is an example of plugin object, that
    can be implemented for each type of Probe task.

    It extends the Plugin class.
    """

    # The plugin name
    __name          = 'TEST'

    # The plugin category
    __tag           = 'TEST'

    def __init__(self):
        """
        This is the constructor for the class.

        :param configs:         The configurations for the plugin
        :return:
        """

        Plugin.__init__(self, self.__name, self.__tag)
        return

    def setup(self, info):
        """
        This is an empty method that is meant to show that
        the setup procedure is done properly.

        :param info:            The configs
        :return:
        """

        self._configs = info

        # Setup the publisher for the task
        # Setup the amqp url here we put the user name and password
        #TODO self._publisher =

        # Start the publisher
        self._publisher.start()
        self._logger.info("Setup the TEST plugin.")
        return

    def _run(self):
        """
        This is the run method. It basically prints the following
        string: "Testing !!!" in both the message queue and also in the
        console to track.

        :return:
        """

        # Call the testing method.
        self.__testing()
        return

    def _kill(self):
        """
        Disconnects the publisher
        :return:
        """

        self._logger.info("Disconnecting publisher...")
        self._publisher.stop()
        return

    def __testing(self):
        """
        This is the run method. It basically prints the following
        string: "{'info' : "Testing !!!"}" in both the message queue and also in the
        console to track.

        :return:
        """

        import datetime
        message = {
                'info' : "Testing !!!"
            }

        self._resource.setObj(message)
        self._logger.info(
            self._resource.getObj()
        )

        # Publish the entire resource to track...
        self._queue.put(self._resource.__dict__)
        time.sleep(2)
        return

