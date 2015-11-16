"""

    :Probe:
    ==========

    :
    This is the poller worker process that will
    continuously scan the network for new devices and
    include the results in an indexed database (Mongodb).

    This process also issues alarms to the alarm queue based on
    access control lists identified in the ACL db.
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
import gc
import abc
import logging
import threading

"""
=============================================
Constants
=============================================
"""

# Program Attributes
__author__  =   "gammaRay"
__version__ =   "1.0"
__date__    =   "9/28/2015"

PLACEHOLDER = ""

"""
=============================================
Source
=============================================
"""

class Probe(threading.Thread):
    """
    This is the base class for each probe object. It contains the
    necessary methods to bootstrap the probe into the probing
    framework.
    """

    # Set the class to an abstract class
    __metaclass__   = abc.ABCMeta

    # The probe name
    __name          = None

    # The probe type
    __type          = None

    # Probe definition
    __definition    = None

    # The sensor data
    __data          = None

    # Monitored / Continuous
    __continuous    = False

    # Data template
    __template      = None

    # Probe alive?
    __alive         = True

    # The logger object
    logger        = None

    # The data queue
    _queue       = None

    def __init__(self, name, queue, continuous):
        """
        The default constructor for the class.
        We pass the name of the probe to the class and
        set it.

        :param name:            The name of the probe
        :param queue:           The application queue
        :param continuous:      The continuous flag
        :return:
        """

        self.__name = name
        self._queue = queue
        self.__continuous = continuous
        self.logger = logging.getLogger(
            "Probe - " + name
        )
        threading.Thread.__init__(
            self
        )
        return

    @abc.abstractmethod
    def setup(self):
        """
        This is the default setup method.

        :return:
        """
        raise NotImplemented

    def run(self):
        """
        This is the default run method for the probe.

        :return:
        """

        # While the thread is alive
        if self.__continuous:

            # If the probe is in fact a reoccurring probe.
            while self.__alive:

                # Run the differed processed
                self._run()
                self.update()

            # Kill the threads
            self.join()

        else:
            # The probe is not a recurring probe.
            self._run()
            self.update()
        return

    def kill(self):
        """
        Kills the threads

        :return:
        """
        self.__alive = False
        return

    @abc.abstractmethod
    def _run(self):
        """
        This is the deferred running method for the class.

        :return:
        """
        raise NotImplemented

    def update(self):
        """
        Updates the fields in the object.
        :return:
        """
        # Update the data queue
        self._queue.put(
            self.get_data()
        )
        return

    # Properties

    def register_type(self, type):
        """
        This is the registration of the type of probe

        :param type:            The probe type
        :return:
        """

        self.__type = type
        return

    def get_type(self):
        """
        Returns the type

        :return:
        """
        return self.__type

    __type_prop = property(
        fget=get_type,
        fset=register_type
    )

    def set_definition(self, definition):
        """
        This is the method that sets teh definition of the
        probe.

        :param definition:      The definition of the probe
        :return:
        """

        self.__definition = definition
        return

    def get_definition(self):
        """
        Returns the definition

        :return:
        """
        return self.__definition

    __def_prop = property(
        fget=get_definition,
        fset=set_definition
    )

    def set_data(self, data):
        """
        This is the method that sets the data read from the
        probe.

        :param data:            The data from the probe
        :return:
        """

        self.__data = data
        return

    def get_data(self):
        """
        Returns the data

        :return:
        """
        return {
            "id"    : self.__name,
            "data"  : self.__data
        }

    __data_prop = property(
        fget=get_data,
        fset=set_data
    )

    def set_template(self, template):
        """
        This method registers the data export template
        to the probe.

        :param template:        The template to adhere to.
        :return:
        """

        self.__template = template
        return

    def get_template(self):
        """
        Returns the template

        :return:
        """
        return self.__template

    __template_prop = property(
        fget=get_template,
        fset=set_template
    )

    def set_continuous(self, continuous):
        """
        This method registers the continuous flag
        to the probe.

        :param continuous:        The continuous fla
        :return:
        """

        self.__continuous = continuous
        return

    def get_continuous(self):
        """
        Returns the continuous

        :return:
        """
        return self.__continuous

    __continuous_prop = property(
        fget=get_continuous,
        fset=set_continuous
    )
