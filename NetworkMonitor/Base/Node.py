"""

    :Node:
    ==========

    :description:

    :copyright: (c) 2015-10-23 by francispapineau.
    :license: BSD, see LICENSE for more details.

    Author:         francispapineau
    Version:        :version: #TODO
    Date:           2015-10-23
    
"""

"""
=============================================
Imports
=============================================
"""

"""
=============================================
Constants
=============================================
"""

# Program Attributes
__author__ = "francispapineau"
__version__ = ""  # TODO
__date__ = "2015-10-23"

"""
=============================================
Variables
=============================================
"""

"""
=============================================
Source
=============================================
"""

# Start logger


class Node(object):

    def __init__(self):

        # register publisher object
        """
        def main():
        logging.basicConfig(level=logging.DEBUG)
        q = multiprocessing.Queue()

        # Connect to localhost:5672 as guest with the password guest and virtual host "/" (%2F)
        example = NodePublisher('amqp://test:test@localhost:5672/%2F?connection_attempts=3&heartbeat_interval=3600',
                                q)
        try:
            example.start()
            for i in range(0,100):
                q.put({str(i) : str(i)})

        except KeyboardInterrupt:
            example.stop()

        if __name__ == '__main__':
        main()
        """
        # register multiprocessing queue


        return

    def generate_password(self):

        import getpass
        getpass.AskPassword()

        #encode 64