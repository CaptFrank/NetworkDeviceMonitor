"""

    :LogStash:
    ==========

    :
    This is the logstash interface. We forward all
    the logs that we have acquired on a timer basis.
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

import zlib
import uuid
import logging

from logstash.handler_amqp \
    import AMQPLogstashHandler
from NetworkMonitor.config \
    import REPORT_MAX_SIZE
from multiprocessing \
    import Process, Queue
from logstash_formatter \
    import LogstashFormatterV1

from NetworkMonitor.Base.ResourceManager \
    import get_client_manager

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

class LogStashForwarder(Process):
    """
    This is the class that will format the messages from the
    processes, create a connection to the logstash broker and
    send the package to the respective logstash entity.

    This class also provides standard template to messages
    for the logstash server.
    """

    # The parent process name
    __name                      = None

    # The application queue needed for the messages
    __queue                     = None

    # The alive bool
    __alive                     = True

    # The Logger
    __logger                    = None

    # Max size
    __size                      = REPORT_MAX_SIZE

    # Log stash logger
    __logstash                  = None

    # The handler
    __handler                   = None

    def __init__(self, name):
        """
        This is the default constructor for the class.

        :param name:            The name of the process needing the iface.
        :return:
        """

        # Set the name
        self.__name = name

        # Set the queue from the resource manager
        self.__queue = get_client_manager().get_queue(
            name
        )

        # Set the logger
        self.__logger  = logging.getLogger(
            "LogStashForwarder"
            + " - "
            + self.__name
        )

        # Override the super class
        Process.__init__(self)
        return

    def setup(self, configs):
        """
        This is the logstash configurations needed to authenticate,
        connect and send reliable messages.

        :param configs:
        :return:
        """

        # Segment the host configs
        host = configs['HOST']

        # Create the logstash handle
        self.__logstash = logging.getLogger(
            configs['name'] +
            '-logstash-handle'
        )
        self.__logstash.setLevel(
            logging.INFO
        )

        # Create a handler
        self.__handler = AMQPLogstashHandler(
                host = host['server'],
                port = host['port'],
                username = host['user'],
                password = self.__getPassword(host),
                durable = True,
                version = 1,
                fqdn = True,
                exchange_routing_key = self.__name
            )

        # Add the formatter
        self.__handler.setFormatter(
            LogstashFormatterV1()
        )

        # Add the handler
        self.__logstash.addHandler(
            self.__handler
        )
        return

    def run(self):
        """
        Process run method.
        We only send the payloads if the queue has more than
        self.__size reports in it.

        :return:
        """

        sentinel    = None
        array       = []
        while self.__alive:

            # Check the size
            if self.__queue.qsize() >= self.__size:
                # Iterate the values to check
                for item in iter(self.__queue.get, sentinel):
                    array.append(
                        item
                    )

                self._send(
                    array
                )
                array = []
        return

    def kill(self):
        """
        Kills the process.

        :return:
        """

        self.__logger.info(
            "Killing the logstash logger for plugin: %s"
            %self.__name
        )
        self.__alive = False
        return

    def _send(self, package, *args):
        """
        Sends the package to the logstash sever.

        :param package:             The data to send
        :param args:                The arg list to send
        :return:
        """

        # Format the data
        # TODO format

        self.__logger.info(
            "Sending a package to the logstash server."
        )

        # Compress the data
        package = zlib.compress(package)

        # Send the data
        self.__logstash.info(
            package,
            args
        )
        return

    def __getPassword(self, configs):
        """
        Converts the password into a plain text password.

        :param configs:             The configs.
        :return:
        """
        import base64
        return str(
            base64.b64decode(
                configs['password']
            ).decode(
                "utf-8"
            )
        )

def get_logstash_message(message):
        """
        Adds a message to the sender queue.

        :param message:             The message payload
        :return:
        """

        # Temp id
        id = uuid.uuid4()
        payload = {
            "id"        :   str(
                id
            ),
            "payload"   :   message
        }
        return payload