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


import pika
import json
import multiprocessing

from multiprocessing \
    import Process
from NetworkMonitor.config import *

"""
=============================================
Constants
=============================================
"""

# Program Attributes
__author__          =   "gammaRay"
__version__         =   "1.0"
__date__            =   "9/28/2015"

PUB_AMQP_URL        = 'amqp://{user}:{password}'        \
                      '@{server}:{port}/%2F?'           \
                      'connection_attempts={attempts}'  \
                      '&heartbeat_interval={heartbeat}'

"""
=============================================
Source
=============================================
"""

class NodePublisher(Process):
    """
    This is an example publisher that will handle unexpected interactions
    with RabbitMQ such as channel and connection closures.

    If RabbitMQ closes the connection, it will reopen it. You should
    look at the output, as there are limited reasons why the connection may
    be closed, which usually are tied to permission related issues or
    socket timeouts.

    It uses delivery confirmations and illustrates one way to keep track of
    messages that have been sent and if they've been confirmed by RabbitMQ.

    http://pika.readthedocs.org/en/latest/examples/asynchronous_publisher_example.html
    """

    """
    ===============================
    Constants
    """

    EXCHANGE_TYPE       = 'data'

    """
    ===============================
    Attributes
    """

    # =============================
    # Objects

    # The connection object
    _connection         = None

    # The channel object to issue messages
    _channel            = None

    # The logging engine
    _logger             = None

    # The application queue
    _queue              = None

    # The plugin / app names
    __name              = None
    __app               = None

    # =============================
    # Attributes

    # The number of issues
    _deliveries         = None

    # The message ack flag
    _acked              = None

    # The message nack flag
    _nacked             = None

    # The message number
    _message_number     = None

    # The stop boolean
    _stopping           = None

    # The server url address
    _url                = None

    # The closing flag
    _closing            = None


    def __init__(self, amqp_url, queue, plugin, app):
        """
        Setup the example publisher object, passing in the URL we will use
        to connect to RabbitMQ.

        :param amqp_url:        The URL for connecting to RabbitMQ
        :param plugin:          The plugin name
        :param app:             The app name
        :param queue:           The application queue
        """

        # Set internals
        self._connection        = None
        self._channel           = None
        self._deliveries        = []
        self._acked             = 0
        self._nacked            = 0
        self._message_number    = 0
        self._stopping          = False
        self._url               = amqp_url
        self._closing           = False
        self._queue             = queue

        self.__name             = plugin
        self.__app              = app
        self._logger            = logging.getLogger('NodePublisher - ' + self._queue_type)

        # Super the class
        multiprocessing.Process.__init__(self)
        return

    def connect(self):
        """
        This method connects to RabbitMQ, returning the connection handle.
        When the connection is established, the on_connection_open method
        will be invoked by pika. If you want the reconnection to work, make
        sure you set stop_ioloop_on_close to False, which is not the default
        behavior of this adapter.

        :rtype: pika.SelectConnection
        """

        self._logger.info('Connecting to %s', self._url)
        return pika.SelectConnection(
            pika.URLParameters(
                self._url
            ),
            self.on_connection_open,
            stop_ioloop_on_close=False
        )

    def on_connection_open(self, unused_connection):
        """
        This method is called by pika once the connection to RabbitMQ has
        been established. It passes the handle to the connection object in
        case we need it, but in this case, we'll just mark it unused.

        :type unused_connection:        pika.SelectConnection
        """
        self._logger.info(
            'Connection opened'
        )
        self.add_on_connection_close_callback()
        self.open_channel()
        return

    def add_on_connection_close_callback(self):
        """
        This method adds an on close callback that will be invoked by pika
        when RabbitMQ closes the connection to the publisher unexpectedly.
        """

        self._logger.info(
            'Adding connection close callback'
        )
        self._connection.add_on_close_callback(
            self.on_connection_closed
        )
        return

    def on_connection_closed(self, connection, reply_code, reply_text):
        """
        This method is invoked by pika when the connection to RabbitMQ is
        closed unexpectedly. Since it is unexpected, we will reconnect to
        RabbitMQ if it disconnects.

        :param pika.connection.Connection connection: The closed connection obj
        :param int reply_code:      The server provided reply_code if given
        :param str reply_text:      The server provided reply_text if given
        """
        self._channel = None

        # Check to see if the connection is closing
        if self._closing:
            self._connection.ioloop.stop()
        else:
            self._logger.warning(
                'Connection closed, reopening in 5 seconds: (%s) %s',
                reply_code,
                reply_text
            )
            self._connection.add_timeout(
                5,
                self.reconnect
            )
        return

    def reconnect(self):
        """
        Will be invoked by the IOLoop timer if the connection is
        closed. See the on_connection_closed method.
        """

        # Re-init variables
        self._deliveries        = []
        self._acked             = 0
        self._nacked            = 0
        self._message_number    = 0

        # This is the old connection IOLoop instance, stop its ioloop
        self._connection.ioloop.stop()

        # Create a new connection
        self._connection = self.connect()

        # There is now a new connection, needs a new ioloop to run
        self._connection.ioloop.start()
        return

    def open_channel(self):
        """
        This method will open a new channel with RabbitMQ by issuing the
        Channel.Open RPC command. When RabbitMQ confirms the channel is open
        by sending the Channel.OpenOK RPC reply, the on_channel_open method
        will be invoked.
        """

        self._logger.info(
            'Creating a new channel'
        )
        self._connection.channel(
            on_open_callback=self.on_channel_open
        )
        return

    def on_channel_open(self, channel):
        """
        This method is invoked by pika when the channel has been opened.
        The channel object is passed in so we can make use of it.

        Since the channel is now open, we'll declare the exchange to use.

        :param pika.channel.Channel channel: The channel object
        """
        self._logger.info('Channel opened')
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(
            self.__name         # Exchange is the plugin name
        )
        return

    def add_on_channel_close_callback(self):
        """
        This method tells pika to call the on_channel_closed method if
        RabbitMQ unexpectedly closes the channel.
        """
        self._logger.info('Adding channel close callback')
        self._channel.add_on_close_callback(
            self.on_channel_closed
        )
        return

    def on_channel_closed(self, channel, reply_code, reply_text):
        """
        Invoked by pika when RabbitMQ unexpectedly closes the channel.
        Channels are usually closed if you attempt to do something that
        violates the protocol, such as re-declare an exchange or queue with
        different parameters. In this case, we'll close the connection
        to shutdown the object.

        :param pika.channel.Channel: The closed channel
        :param int reply_code: The numeric reason the channel was closed
        :param str reply_text: The text reason the channel was closed

        """
        self._logger.warning(
            'Channel was closed: (%s) %s',
            reply_code,
            reply_text
        )
        if not self._closing:
            self._connection.close()
        return

    def setup_exchange(self, exchange_name):
        """
        Setup the exchange on RabbitMQ by invoking the Exchange.Declare RPC
        command. When it is complete, the on_exchange_declareok method will
        be invoked by pika.

        :param str|unicode exchange_name: The name of the exchange to declare
        """
        self._logger.info(
            'Declaring exchange %s',
            exchange_name
        )
        self._channel.exchange_declare(
            self.on_exchange_declareok,
            exchange_name,
            self.EXCHANGE_TYPE
        )
        return

    def on_exchange_declareok(self, unused_frame):
        """
        Invoked by pika when RabbitMQ has finished the Exchange.Declare RPC
        command.

        :param pika.Frame.Method unused_frame: Exchange.DeclareOk response frame
        """
        self._logger.info(
            'Exchange declared'
        )
        self.setup_queue(
            self.__name
            + "."
            + self.__app
        )
        return

    def setup_queue(self, queue_name):
        """
        Setup the queue on RabbitMQ by invoking the Queue.Declare RPC
        command. When it is complete, the on_queue_declareok method will
        be invoked by pika.

        :param str|unicode queue_name: The name of the queue to declare.
        """
        self._logger.info(
            'Declaring queue %s',
            queue_name
        )
        self._channel.queue_declare(
            self.on_queue_declareok,
            queue_name
        )
        return

    def on_queue_declareok(self, method_frame):
        """Method invoked by pika when the Queue.Declare RPC call made in
        setup_queue has completed. In this method we will bind the queue
        and exchange together with the routing key by issuing the Queue.Bind
        RPC command. When this command is complete, the on_bindok method will
        be invoked by pika.

        :param pika.frame.Method method_frame: The Queue.DeclareOk frame

        """
        self._logger.info(
            'Binding %s to %s with %s',
            self.__name,
            (
                self.__name
                + "."
                + self.__app
            ),
            self.__name
        )
        self._channel.queue_bind(
            self.on_bindok,
            (
                self.__name
                + "."
                + self.__app
            ),
            self.__name,
            self.__name
        )
        return

    def on_bindok(self, unused_frame):
        """
        This method is invoked by pika when it receives the Queue.BindOk
        response from RabbitMQ. Since we know we're now setup and bound, it's
        time to start publishing.
        """
        self._logger.info(
            'Queue bound'
        )
        self.start_publishing()
        return

    def start_publishing(self):
        """
        This method will enable delivery confirmations and schedule the
        first message to be sent to RabbitMQ
        """
        self._logger.info(
            'Issuing consumer related RPC commands'
        )
        self.enable_delivery_confirmations()
        self.schedule_next_message()
        return

    def enable_delivery_confirmations(self):
        """
        Send the Confirm.Select RPC method to RabbitMQ to enable delivery
        confirmations on the channel. The only way to turn this off is to close
        the channel and create a new one.

        When the message is confirmed from RabbitMQ, the
        on_delivery_confirmation method will be invoked passing in a Basic.Ack
        or Basic.Nack method from RabbitMQ that will indicate which messages it
        is confirming or rejecting.
        """
        self._logger.info(
            'Issuing Confirm.Select RPC command'
        )
        self._channel.confirm_delivery(
            self.on_delivery_confirmation
        )
        return

    def on_delivery_confirmation(self, method_frame):
        """
        Invoked by pika when RabbitMQ responds to a Basic.Publish RPC
        command, passing in either a Basic.Ack or Basic.Nack frame with
        the delivery tag of the message that was published. The delivery tag
        is an integer counter indicating the message number that was sent
        on the channel via Basic.Publish. Here we're just doing house keeping
        to keep track of stats and remove message numbers that we expect
        a delivery confirmation of from the list used to keep track of messages
        that are pending confirmation.

        :param pika.frame.Method method_frame: Basic.Ack or Basic.Nack frame
        """
        confirmation_type = method_frame.method.NAME.split('.')[1].lower()
        self._logger.info(
            'Received %s for delivery tag: %i',
            confirmation_type,
            method_frame.method.delivery_tag
        )

        if confirmation_type == 'ack':
            self._acked += 1

        elif confirmation_type == 'nack':
            self._nacked += 1

        self._deliveries.remove(
            method_frame.method.delivery_tag
        )
        self._logger.info(
            'Published %i messages, %i have yet to be confirmed, '
            '%i were acked and %i were nacked',
            self._message_number,
            len(
                self._deliveries
            ),
            self._acked,
            self._nacked
        )
        return

    def schedule_next_message(self):
        """
        If we are not closing our connection to RabbitMQ, schedule another
        message to be delivered in PUBLISH_INTERVAL seconds.
        """
        if self._stopping:
            return
        self._logger.info(
            'Scheduling next message for %0.1f seconds',
            PUBLISH_INTERVAL
        )
        self._connection.add_timeout(
            PUBLISH_INTERVAL,
            self.publish_message
        )
        return

    def publish_message(self):
        """If the class is not stopping, publish a message to RabbitMQ,
        appending a list of deliveries with the message number that was sent.
        This list will be used to check for delivery confirmations in the
        on_delivery_confirmations method.

        Once the message has been sent, schedule another message to be sent.
        The main reason I put scheduling in was just so you can get a good idea
        of how the process is flowing by slowing down and speeding up the
        delivery intervals by changing the PUBLISH_INTERVAL constant in the
        class.

        """
        if self._stopping:
            return


        if not self._queue.empty():

            message = self._queue.get()

            # Get a message to publish
            properties = pika.BasicProperties(
                app_id=self.__name + '-publisher',
                content_type='application/json',
                headers=message
            )

            self._channel.basic_publish(
                self.__name,
                self.__name,
                json.dumps(
                    message,
                    ensure_ascii=False
                ),
                properties
            )
            self._message_number += 1
            self._deliveries.append(
                self._message_number
            )
            self._logger.info(
                'Published message # %i',
                self._message_number
            )
        self.schedule_next_message()
        return

    def close_channel(self):
        """
        Invoke this command to close the channel with RabbitMQ by sending
        the Channel.Close RPC command.
        """
        self._logger.info(
            'Closing the channel'
        )
        if self._channel:
            self._channel.close()
        return

    def run(self):
        """
        Run the example code by connecting and then starting the IOLoop.
        """
        self._connection = self.connect()
        self._connection.ioloop.start()
        return

    def stop(self):
        """
        Stop the example by closing the channel and connection. We
        set a flag here so that we stop scheduling new messages to be
        published. The IOLoop is started because this method is
        invoked by the Try/Catch below when KeyboardInterrupt is caught.
        Starting the IOLoop again will allow the publisher to cleanly
        disconnect from RabbitMQ.
        """

        self._logger.info(
            'Stopping'
        )
        self._stopping = True
        self.close_channel()
        self.close_connection()
        self._connection.ioloop.start()
        self._logger.info(
            'Stopped'
        )
        return

    def close_connection(self):
        """
        This method closes the connection to RabbitMQ.
        """
        self._logger.info(
            'Closing connection'
        )
        self._closing = True
        self._connection.close()
        return

    @staticmethod
    def format_url(kwargs):
        """
        Formats the amqp url to the server.

        :param kwargs:          The dict with the params to format.
        :return:
        """
        import base64

        password = kwargs['password']
        kwargs['password'] = base64.b64decode(
            password
        )
        return PUB_AMQP_URL.format(
            **kwargs
        )

    def publish(self, message):
        """
        Add a message to send

        :param message:         The message to send
        :return:
        """

        self._queue.put(
            message
        )
        return
