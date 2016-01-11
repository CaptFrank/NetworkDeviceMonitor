"""

    :Subscriber:
    ==========

    :
    This is the subscriber that looks for all Rabbitmq queues.
    Once it has found a queue, it then reads content that is in the queue.
    Once the size limit is reached, the package is then sent to the logstash
    with the format defined in the Logstash interface object.

    The search algorithm that is utilized to find queues and information,
    is a round robin style algorithm.
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
import logging
import multiprocessing

from multiprocessing \
    import Process

from NetworkMonitor.Interface.Distributed.LogStash \
    import get_logstash_message

"""
=============================================
Constants
=============================================
"""

# Program Attributes
__author__          =   "gammaRay"
__version__         =   "1.0"
__date__            =   "9/28/2015"

SUB_AMQP_URL        = 'amqp://{user}:{password}'    \
                      '@{server}:{port}/%2F'

"""
=============================================
Source
=============================================
"""

class NodeConsumer(Process):
    """
    This is an example consumer that will handle unexpected interactions
    with RabbitMQ such as channel and connection closures.

    If RabbitMQ closes the connection, it will reopen it. You should
    look at the output, as there are limited reasons why the connection may
    be closed, which usually are tied to permission related issues or
    socket timeouts.

    If the channel is closed, it will indicate a problem with one of the
    commands that were issued and that should surface in the output as well.

    http://pika.readthedocs.org/en/latest/examples/asynchronous_consumer_example.html
    """

    """
    ===============================
    Constants
    """

    # Exchange engine type.
    EXCHANGE_TYPE       = 'topic'

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

    # The plugin
    __name              = None

    # The apps that are needed to run
    __apps              = []

    # The logstash queue
    __queue             = None

    # =============================
    # Attributes

    # The number of issues
    _deliveries         = None

    # The server url address
    _url                = None

    # The closing flag
    _closing            = None

    # Consumer tag
    _consumer_tag       = None

    # Manager
    _manager            = None

    def __init__(self, amqp_url, plugin, apps):
        """
        Create a new instance of the consumer class, passing in the AMQP
        URL used to connect to RabbitMQ.

        :param str amqp_url:    The AMQP url to connect with
        :param plugin:          The plugin name to bind to
        :param apps:            The apps
        """

        self._connection        = None
        self._channel           = None
        self._closing           = False
        self._consumer_tag      = None
        self._url               = amqp_url
        self.__name             = plugin
        self.__apps             = apps

        self._logger            = logging.getLogger('NodeConsumer')

        # Super the class
        multiprocessing.Process.__init__(self)
        return

    def connect(self):
        """
        This method connects to RabbitMQ, returning the connection handle.
        When the connection is established, the on_connection_open method
        will be invoked by pika.

        :rtype: pika.SelectConnection
        """

        self._logger.info(
            '[+] Connecting to %s',
            self._url
        )
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

        :type unused_connection: pika.SelectConnection
        """

        self._logger.info(
            '[+] Connection opened'
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
            '[+] Adding connection close callback'
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
        :param int reply_code: The server provided reply_code if given
        :param str reply_text: The server provided reply_text if given
        """

        from NetworkMonitor.config import CONNECTION_TIMEOUT

        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            self._logger.warning(
                '[-] Connection closed, reopening in 5 seconds: (%s) %s',
                reply_code,
                reply_text
            )
            self._connection.add_timeout(
                CONNECTION_TIMEOUT,
                self.reconnect
            )
            return

    def reconnect(self):
        """
        Will be invoked by the IOLoop timer if the connection is
        closed. See the on_connection_closed method.
        """

        # This is the old connection IOLoop instance, stop its ioloop
        self._connection.ioloop.stop()

        if not self._closing:

            # Create a new connection
            self._connection = self.connect()

            # There is now a new connection, needs a new ioloop to run
            self._connection.ioloop.start()
            return

    def open_channel(self):
        """
        Open a new channel with RabbitMQ by issuing the Channel.Open RPC
        command. When RabbitMQ responds that the channel is open, the
        on_channel_open callback will be invoked by pika.
        """

        self._logger.info(
            '[+] Creating a new channel'
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

        self._logger.info(
            '[+] Channel opened'
        )
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(
            self.__name
        )
        return

    def add_on_channel_close_callback(self):
        """
        This method tells pika to call the on_channel_closed method if
        RabbitMQ unexpectedly closes the channel.
        """

        self._logger.info(
            '[+] Adding channel close callback'
        )
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
            '[-] Channel %i was closed: (%s) %s',
            channel,
            reply_code,
            reply_text
        )
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
            '[+] Declaring exchange %s',
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
            '[+] Exchange declared'
        )
        self.setup_queue(
            self.get_queue_name()
        )
        return

    def setup_queue(self, queue_name):
        """Setup the queue on RabbitMQ by invoking the Queue.Declare RPC
        command. When it is complete, the on_queue_declareok method will
        be invoked by pika.

        :param str|unicode queue_name: The name of the queue to declare.

        """
        self._logger.info(
            '[+] Declaring queue %s',
            queue_name
        )
        self._channel.queue_declare(
            self.on_queue_declareok,
            queue_name
        )
        return

    def on_queue_declareok(self, method_frame):
        """
        Method invoked by pika when the Queue.Declare RPC call made in
        setup_queue has completed. In this method we will bind the queue
        and exchange together with the routing key by issuing the Queue.Bind
        RPC command. When this command is complete, the on_bindok method will
        be invoked by pika.

        :param pika.frame.Method method_frame: The Queue.DeclareOk frame
        """

        for app in self.__apps.keys():

            self._logger.info(
                '[+] Binding %s to %s with %s',
                self.get_queue_name(),
                self.__name,
                app
            )
            self._channel.queue_bind(
                self.on_bindok,
                self.get_queue_name(),
                self.__name,
                app
            )
        return

    def on_bindok(self, unused_frame):
        """
        Invoked by pika when the Queue.Bind method has completed. At this
        point we will start consuming messages by calling start_consuming
        which will invoke the needed RPC commands to start the process.

        :param pika.frame.Method unused_frame: The Queue.BindOk response frame
        """

        self._logger.info(
            '[+] Queue bound'
        )
        self.start_consuming()
        return

    def start_consuming(self):
        """
        This method sets up the consumer by first calling
        add_on_cancel_callback so that the object is notified if RabbitMQ
        cancels the consumer. It then issues the Basic.Consume RPC command
        which returns the consumer tag that is used to uniquely identify the
        consumer with RabbitMQ. We keep the value to use it when we want to
        cancel consuming. The on_message method is passed in as a callback pika
        will invoke when a message is fully received.
        """

        self._logger.info(
            '[+] Issuing consumer related RPC commands'
        )
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(
            self.on_message,
            self.get_queue_name()
        )
        return

    def add_on_cancel_callback(self):
        """
        Add a callback that will be invoked if RabbitMQ cancels the consumer
        for some reason. If RabbitMQ does cancel the consumer,
        on_consumer_cancelled will be invoked by pika.
        """

        self._logger.info(
            '[+] Adding consumer cancellation callback'
        )
        self._channel.add_on_cancel_callback(
            self.on_consumer_cancelled
        )
        return

    def on_consumer_cancelled(self, method_frame):
        """
        Invoked by pika when RabbitMQ sends a Basic.Cancel for a consumer
        receiving messages.

        :param pika.frame.Method method_frame: The Basic.Cancel frame
        """

        self._logger.info(
            '[-] Consumer was cancelled remotely, shutting down: %r',
            method_frame
        )
        if self._channel:
            self._channel.close()
        return

    def on_message(self, unused_channel, basic_deliver, properties, body):
        """
        Invoked by pika when a message is delivered from RabbitMQ. The
        channel is passed for your convenience. The basic_deliver object that
        is passed in carries the exchange, routing key, delivery tag and
        a redelivered flag for the message. The properties passed in is an
        instance of BasicProperties with the message properties and the body
        is the message that was sent.

        :param pika.channel.Channel unused_channel: The channel object
        :param pika.Spec.Basic.Deliver: basic_deliver method
        :param pika.Spec.BasicProperties: properties
        :param str|unicode body: The message body
        """

        self._logger.info(
            '[+] Received message # %s from %s: %s',
            basic_deliver.delivery_tag,
            properties.app_id,
            body
        )
        self.acknowledge_message(
            basic_deliver.delivery_tag
        )

        # Get the managed queue and add the entry in it
        queue = self.__apps['client'].get_queue(
            self.__name
        )

        # Put the data in the queue
        queue.put(
            get_logstash_message(
                body
            )
        )
        return

    def acknowledge_message(self, delivery_tag):
        """
        Acknowledge the message delivery from RabbitMQ by sending a
        Basic.Ack RPC method for the delivery tag.

        :param int delivery_tag: The delivery tag from the Basic.Deliver frame
        """

        self._logger.info(
            '[+] Acknowledging message %s',
            delivery_tag
        )
        self._channel.basic_ack(
            delivery_tag
        )
        return

    def stop_consuming(self):
        """
        Tell RabbitMQ that you would like to stop consuming by sending the
        Basic.Cancel RPC command.
        """

        if self._channel:
            self._logger.info(
                '[-] Sending a Basic.Cancel RPC command to RabbitMQ'
            )
            self._channel.basic_cancel(
                self.on_cancelok,
                self._consumer_tag
            )
        return

    def on_cancelok(self, unused_frame):
        """
        This method is invoked by pika when RabbitMQ acknowledges the
        cancellation of a consumer. At this point we will close the channel.
        This will invoke the on_channel_closed method once the channel has been
        closed, which will in-turn close the connection.

        :param pika.frame.Method unused_frame: The Basic.CancelOk frame
        """

        self._logger.info(
            '[+] RabbitMQ acknowledged the cancellation of the consumer'
        )
        self.close_channel()
        return

    def close_channel(self):
        """
        Call to close the channel with RabbitMQ cleanly by issuing the
        Channel.Close RPC command.
        """

        self._logger.info(
            '[-] Closing the channel'
        )
        self._channel.close()
        return

    def run(self):
        """
        Run the example consumer by connecting to RabbitMQ and then
        starting the IOLoop to block and allow the SelectConnection to operate.
        """

        self._connection = self.connect()
        self._connection.ioloop.start()
        return

    def stop(self):
        """
        Cleanly shutdown the connection to RabbitMQ by stopping the consumer
        with RabbitMQ. When RabbitMQ confirms the cancellation, on_cancelok
        will be invoked by pika, which will then closing the channel and
        connection. The IOLoop is started again because this method is invoked
        when CTRL-C is pressed raising a KeyboardInterrupt exception. This
        exception stops the IOLoop which needs to be running for pika to
        communicate with RabbitMQ. All of the commands issued prior to starting
        the IOLoop will be buffered but not processed.
        """

        self._logger.info(
            '[-] Stopping'
        )
        self._closing = True
        self.stop_consuming()
        self._connection.ioloop.start()
        self._logger.info(
            '[-] Stopped'
        )
        return

    def close_connection(self):
        """
        This method closes the connection to RabbitMQ.
        """
        self._logger.info(
            '[-] Closing connection'
        )
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
        kwargs['password'] = str(
            base64.b64decode(
                password
            ).decode(
                "utf-8"
            )
        )
        return SUB_AMQP_URL.format(**kwargs)

    def get_queue_name(self):
        """
        Gets the queue for use

        :return:
        """

        return "{name}.*".format(
            name = self.__name,
        )