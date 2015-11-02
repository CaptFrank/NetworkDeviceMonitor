"""

    :Publisher:
    ==========

    :
    This is the object that will publish the objects to the message
    server.
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

import uuid
import time
import pickle
import logging
import multiprocessing
from multiprocessing \
    import Process, Queue

import snakemq.link
import snakemq.message
import snakemq.packeter
import snakemq.messaging

from snakemq.message \
    import FLAG_PERSISTENT
from snakemq.storage.sqlite \
    import SqliteQueuesStorage

from NetworkMonitor.Interface.Internal.Snakemq.LocalCommands \
    import *


"""
=============================================
Constants
=============================================
"""

# Program Attributes
__author__          =   "gammaRay"
__version__         =   "1.0"
__date__            =   "9/28/2015"

UNUSED              = ''

"""
=============================================
Source
=============================================
"""

class SnakePublisher(Process):
    """
    This is an example publisher that will handle unexpected interactions
    with RabbitMQ such as channel and connection closures.

    If RabbitMQ closes the connection, it will reopen it. You should
    look at the output, as there are limited reasons why the connection may
    be closed, which usually are tied to permission related issues or
    socket timeouts.

    It uses delivery confirmations and illustrates one way to keep track of
    messages that have been sent and if they've been confirmed by RabbitMQ.

    - Exchange is the plugin name
    - Routing key is the application
    """

    # The logging engine
    __logger             = None

    # The application queue
    __queue              = None

    # The plugin / app names
    __name              = None
    __app               = None

    # The application alive bool
    __alive             = True

    # The message id
    __id                = 0

    # The message uuid
    __uuid              = None

    # =========================
    # Communication attributes
    __link              = None
    __packet_engine     = None
    __message_storage   = None
    __messenger         = None
    __message           = None
    __last              = None

    def __init__(self, name, app, queue):
        """
        This is the default constructor for the class.

        :param name:            This is the name of the plugin
        :param app:             This is the name of the application within the plugin
        :param queue:           This is the application queue
        :return:
        """

        # Set internal references
        self.__name = name
        self.__app = app
        self.__queue = queue

        self._logger            = logging.getLogger(
            'NodePublisher - %s.%s'
            %(
                self.__name,
                self.__app
            )
        )

        # Super the class
        multiprocessing.Process.__init__(
            self
        )
        return

    def setup(self, configs):
        """
        This is the setup method for the class based on the server
        attributes.

        :param configs:         The server attributes.
        :return:
        """

        self._logger.info(
            "[+] Creating the messenger interface for %s:%s"
            %(
                self.__name,
                self.__app
            )
        )

        try:
            # Setup a link
            self.__link = snakemq.link.Link()

            # Setup a packet engine
            self.__packet_engine = snakemq.packeter.Packeter(
                self.__link
            )

            # Setup a messenger
            self.__message_storage = SqliteQueuesStorage(
                configs['storage']
            )

            # Setup messaging engine
            self.__messenger = snakemq.messaging.Messaging(
                self.__get_queue_name(),
                UNUSED,
                self.__packet_engine,
                self.__message_storage
            )


            # Add a listener... This is done for remote operation.
            self._logger.info(
                "[+] Adding a listener for system wide events on port: %i"
                %configs['SUBSCRIBE']['listen']
            )

            # Add Callbacks
            self.__messenger.on_message_recv.add(self.__rx_message)
            self.__messenger.on_message_sent.add(self.__tx_message)
            self.__messenger.on_connect.add(self.__on_connect)
            self.__messenger.on_disconnect.add(self.__on_disconnect)
            self.__messenger.on_error.add(self.__on_error)

            # Add the listener
            self.__link.add_listener(
                (
                    configs['SUBSCRIBE']['server'],
                    configs['SUBSCRIBE']['port']
                ),
                ssl_config=configs['ssl']
            )

            self._logger.info(
                "[+] Adding a connector to %s:%i"
                %(
                    configs['PUBLISH']['server'],
                    configs['PUBLISH']['port']
                 )
            )

            # Add the connector to the server
            self.__link.add_connector(
                (
                    configs['PUBLISH']['server'],
                    configs['PUBLISH']['port']
                )
            )

        except IOError:
            self._logger.error(
                "[-] IOError... Stopping Publisher engine..."
            )
        return

    def run(self):
        """
        This is the default process run.

        :return:
        """

        # Loop until killed
        while self.__alive:

            # Check the application queue
            if not self.__queue.empty():

                # Get an object and publish it to the server
                obj = self.__queue.get()
                self._logger.info(
                    "[+] Got a new object to send: %s"
                    %obj
                )
                self.__send_message(obj)
                self._logger.info(
                    "[+] Sent message #%i"
                    %self.__id
                )

                # Increment the message id
                self.__id += 1

            # Advance the stack
            self.__link.loop()

        # Join the contexts.
        self.join()
        return

    def kill(self):
        """
        Kills the application.

        :return:
        """

        # Not alive anymore
        self.__alive = False
        return

    def publish(self, message):
        """
        Publishes a message to the necessary queue.

        :param message:
        :return:
        """

        # Puts a message in the queue.
        self.__queue.put(
            {
                'payload'   :   message,
                'uuid'      :   str(
                    uuid.uuid4()
                ),
                'time'      :   time.strftime(
                    "%s/%m/%y %H:%M:%S"
                )
            }
        )
        self._logger.info(
            "[+] Added a new message to the queue..."
        )
        return

    def __rx_message(self, conn, ident, message):
        """
        Triggers when receiving a message

        :param conn:            The connection
        :param ident:           The message identity
        :param message:         The message payload
        :return:
        """

        # We have received a new message... Act upon it.

        unpickled = pickle.loads(
            message
        )

        # Assert the event
        self._logger.info(
            "Received a message payload from: %s\n"
            "With identity: %s\n"
            "Payload: %s"
            %(
                str(
                    conn
                ),
                str(
                    ident
                ),
                str(
                    unpickled
                )
             )
        )

        # Take action on the commands
        act_command(
            unpickled
        )
        return

    def __tx_message(self, conn, ident, message):
        """
        Triggers when transmitting a message

        :param conn:            The connection
        :param ident:           The message identity
        :param message:         The message payload uuid
        :return:
        """

        # Assert the event
        self._logger.info(
            "Sent a message payload to: %s\n"
            "With identity: %s\n"
            "Payload: %s"
            %(
                str(
                    conn
                ),
                str(
                    ident
                ),
                str(
                    message
                )
             )
        )
        return

    def __on_connect(self, conn, ident):
        """
        Triggers when connected to a device

        :param conn:            The connection
        :param ident:           The message identity
        :return:
        """

        # Assert the event
        self._logger.info(
            "Connected to a remote node: %s\n"
            "With id: %s"
            %(
                str(
                    conn
                ),
                str(
                    ident
                )
             )
        )

        return

    def __on_disconnect(self, conn, ident):
        """
        Triggers when disconnecting for a device

        :param conn:            The connection
        :param ident:           The message identity
        :return:
        """

        # Assert the event
        self._logger.info(
            "Disconnected from the remote node: %s\n"
            "With id: %s"
            %(
                str(
                    conn
                ),
                str(
                    ident
                )
             )
        )
        return

    def __on_error(self, conn, error):
        """
        Triggered when there is an error

        :param conn:            The connection
        :param ident:           The message identity
        :param message:         The message payload
        :return:
        """

        # Assert the error and kill the engine
        self._logger.error(
            "There has been an error from connection: %s\n"
            "Error code: %s"
            %(
                str(
                    conn
                ),
                str(
                    error
                )
             )
        )
        self._logger.error(
            "[-] Killing the publish engine..."
        )
        self.kill()
        return

    def __send_message(self, obj):
        """
        Sends the message.

        :param obj:         The managed resource.
        :return:
        """

        # Pickle the obj
        pikle = pickle.dumps(
            obj
        )

        # Create the message
        message = snakemq.message.Message(
            pikle,
            ttl = 600,
            flags = FLAG_PERSISTENT
        )

        self._logger.info(
            "[+] Sending pickled message: %s"
            %str(obj)
        )
        return

    def __get_queue_name(self):
        """
        Gets the queue for use

        :return:
        """

        return "{name}.{app}".format(
            name = self.__name,
            app = self.__app
        )