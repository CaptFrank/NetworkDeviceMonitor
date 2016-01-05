"""

    :Plugin:
    ==========

    :
    This is the base plugin class that is meant to extend
    the process class and that also extends the IPlugin class
    to conform to the yapsy plugin interface.
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

import logging

from NetworkMonitor.Base.Resource \
    import ManagedResource
from abc import ABCMeta, abstractmethod
from multiprocessing import Process, Queue
from NetworkMonitor.Interface.Internal.Rabbitmq.RabbitPublisher \
    import NodePublisher
from NetworkMonitor.Interface.Internal.Rabbitmq.RabbitSubscriber \
    import NodeConsumer

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

class Plugin(Process):
    """
    This is the base class for the plugin objects.
    Each plugin must confirm to this template in order
    to run within the plugin framework and this application.
    Each plugin runs in its own Process, speeding up the speed of the
    application.
    """

    # Making this class and abstract class to extend.
    __metaclass__       = ABCMeta

    # This is the process configs that are needed to setup and
    # run the task individually.
    _configs            = None

    # This is the name of the process
    _name               = None

    # The plugin id to route on
    _id                 = None

    # This is the logger object for the class
    _logger             = None

    # This is the running flag.
    _running            = True

    # Apps in a plugin
    # Looks like:
    # {
    #   name : {
    #               pub         : <publisher>,
    #               sub         : <subscriber>,
    #               resource    : <managed resource>,
    #               queue       : <application queue>,
    #   }
    # }
    __apps              = {

    }

    # The logstash reference
    __logstash          = None

    # The main subscriber...
    __subscriber        = None

    def __init__(self, name):
        """
        This is the base constructor method that receives

        :param name:            The plugin name
        :param tag:             The plugin category
        :param logstash:        The logstash process handle
        :return:
        """

        # Setup the internals of the object
        self._logger = logging.getLogger(
            name
        )

        # Override the super class
        Process.__init__(
            self,
            name=name
        )
        return

    def setup(self, info):
        """
        This is the setup method for the process, called before it
        is ran.

        :return:
        """

        # Setup the subscriber instance
        self.__subscriber = NodeConsumer(
            NodeConsumer.format_url(
                info['SUBSCRIBER']
            ),
            self._name,
            self.__apps.keys()
        )

        # Wrapper
        self._setup(info)
        return

    @abstractmethod
    def _setup(self, info):
        """
        Wrapped method for plugins.

        :param info:
        :return:
        """
        raise NotImplemented

    def run(self):
        """
        This is the default process running method.
        :return:
        """

        # Connect the subscriber.
        self._logger.info("[+] Connecting the subscriber...")
        self.__subscriber.start()

        # We deffer the running task to the _run method.
        self._logger.info(
            "[+] Entering the run loop for plugin: %s"
            %self._name
        )

        while self._running:
            self._run()
        self._logger.info(
            "[-] Killed the run loop for plugin: %s"
            %self._name
        )
        return

    def _run(self):
        """
        The default run method for the process.

        :return:
        """

        for app in self.__apps.values():
            app['entry'](app)
        return

    def kill(self):
        """
        This method basically flips the running flag on the
        process to kill it.

        :return:
        """
        self._running = False
        self._logger.info(
            "[-] Killing the plugin: %s"
            %self._name
        )

        # The disconnection method
        self._kill()

        # Kill all queues
        for app in self.__apps.values():
           app['queue'].close()
           app['queue'].join_thread()
        return

    @abstractmethod
    def _kill(self):
        """
        Disconnects the client

        :return:
        """
        raise NotImplemented

    @staticmethod
    def _format(name, app):
        """
        Formats the queue name based on the plugin name and the app

        :param name:                The plugin name
        :param app:                 The sub app to use th queue
        :return:
        """
        return "{name}.{app}".format(name=name, app=app)

    def register(self, name, entry, configs):
        """
        Register the application within the plugin.

        :param name:                The name of the app
        :param entry:               The entry point of the app
        :param configs:             The configs for the app
        :return:
        """

        temp = {}

        # Create the application queue
        temp['queue'] = Queue()

        # Create a publisher
        temp['pub'] = NodePublisher(
            NodePublisher.format_url(
                configs['COMS']
            ),
            temp['queue'],
            name,
            configs['name']
        )

        # Create the managed resource
        temp['resource'] = ManagedResource(
            name = name,
            tag = configs['name']
        )

        # Register the entry point of the app
        temp['entry'] = entry

        self.__apps[
            configs['name']
        ] = temp
        return

    def start_app_coms(self, name):
        """
        Starts the publisher...

        :param name:                The app name
        :return:
        """

        self.__apps[name]['pub'].start()
        return

    def kill_publishers(self):
        """
        Kills the publishers for a plugin.

        :return:
        """

        for app in self.__apps.values():
            app['pub'].stop()
        return

