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

import uuid
import logging

from NetworkMonitor.Base.Resource \
    import ManagedResource
from abc import ABCMeta, abstractmethod
from multiprocessing import Process, Queue

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

    # This is the publishing engine that is used to log the data
    # to the main application process.
    _publisher          = None

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

    # The application queue
    _queue              = None

    # The managed resource that will be published
    _resource           = None

    # App names
    _apps               = {}

    def __init__(self, name, tag):
        """
        This is the base constructor method that receives

        :param name:            The plugin name
        :param tag:             The plugin category
        :return:
        """

        # Setup the internals of the object
        self._logger = logging.getLogger(
            name
        )

        # Setup the queue
        self._queue = Queue()

        # Setup the resource needed to publish the data
        self._resource = ManagedResource(
            name = name,
            tag = tag
        )

        # Override the super class
        Process.__init__(
            self,
            name=name
        )
        return

    @abstractmethod
    def setup(self, info):
        """
        This is the setup method for the process, called before it
        is ran.

        :return:
        """
        raise NotImplemented

    def run(self):
        """
        This is the default process running method.
        :return:
        """

        # We deffer the running task to the _run method.
        self._logger.info(
            "Entering the run loop for plugin: %s"
            %self._name
        )
        while self._running:
            self._run()
        self._logger.info(
            "Killed the run loop for plugin: %s"
            %self._name
        )
        return

    @abstractmethod
    def _run(self):
        """
        The default run method for the process.

        :return:
        """
        raise NotImplemented

    def kill(self):
        """
        This method basically flips the running flag on the
        process to kill it.

        :return:
        """
        self._running = False
        self._logger.info(
            "Killing the plugin: %s"
            %self._name
        )

        # The disconnection method
        self._kill()

        self._queue.close()
        self._queue.join_thread()
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

    def _register_app(self, app, queue):
        """
        Registers a new app in the plugin.

        :param app:                 The app name
        :param queue:               The queue name
        :return:
        """

        self._apps['app'] = queue
        return