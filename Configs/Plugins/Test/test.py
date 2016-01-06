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
    __app           = 'TEST'

    def __init__(self):
        """
        This is the constructor for the class.

        :param configs:         The configurations for the plugin
        :return:
        """

        Plugin.__init__(
            self,
            self.__name
        )
        return

    def _setup(self, info):
        """
        This is an empty method that is meant to show that
        the setup procedure is done properly.

        :param info:            The configs
        :return:
        """

        self._configs = info

        # Setup the publisher for the task
        # Setup the amqp url here we put the user name and password

        for app in self._configs['APPS'].values():

            # Register the plugin
            self.register(
                self.__name,
                self.__testing,
                app
            )

            # Start the publisher
            self.start_app_coms(
                app['name']
            )
            self._logger.info(
                "Started application: %s"
                %app['name']
            )
        self._logger.info(
            "Setup the TEST plugin."
        )
        return

    def _kill(self):
        """
        Disconnects the publisher
        :return:
        """

        self._logger.info(
            "Disconnecting publishers..."
        )
        self.kill_publishers()
        return

    @staticmethod
    def __testing(info):
        """
        This is the run method. It basically prints the following
        string: "{'info' : "Testing !!!"}" in both the message queue and also in the
        console to track.

        :return:
        """

        import time

        message = {
                'info' : "Testing !!!"
            }

        info['resource'].setObj(
            message
        )

        # Publish the entire resource to track...
        info['queue'].put(
            info['resource'].__dict__
        )
        time.sleep(
            2
        )
        return


