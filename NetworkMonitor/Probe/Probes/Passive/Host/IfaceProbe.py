"""

    :IfaceProbe:
    ==========

    :
    This is the interfaces probe. It schedules threads to monitor
    both the counts and the static interface stats.
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

import time
import psutil
from NetworkMonitor.Probe.HostProbe \
    import HostProbe, PLACEHOLDER_STRING, \
    PLACEHOLDER_ARRAY, PLACEHOLDER_DICT
from NetworkMonitor.Probe.MutableProbe \
    import MutableProbe

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

class StaticIfaceProbe(HostProbe):
    """
    This is the user probe that scans what interface are on
    a specific system.

    extends: Probe
    """

    # The class name
    name        = "IfaceProbe"

    # The probe type
    type        = "Iface"

    # Description
    description = \
    "Gets the interfaces on the probe that is running."

    # Fields for filtering
    fields      = []

    # Groups
    groups      = [
        "iface",
        "reconnaissance"
    ]

    # Definition
    definition  = {}

    # Template
    template    = {}

    # Data
    data        = {}

    # Continuous flag
    continuous  = False

    def __init__(self, queue):
        """
        We call the constructor for the class.

        :return:
        """

        # Setup the class object
        HostProbe.__init__(
            self,
            self.name,
            queue,
            self.continuous
        )
        self.logger.info(
            "Created a new Probe of type: %s" %self.type
        )
        return

    def setup(self):
        """
        Setup the probe.

        :return:
        """

        # Register all handles
        self.set_data(
            self.data
        )
        self.register_type(
            self.type
        )
        self.set_definition(
            {
                "type"          : self.get_type(),
                "name"          : self.name,
                "description"   : self.description,
                "default"       : "yes",
                "help"          : self.description,
                "tag"           : self.name,
                "fields"        : PLACEHOLDER_ARRAY,
                "groups"        :PLACEHOLDER_ARRAY,
            }
        )
        self.set_template(
            {
                "definition"    : self.get_definition(),
                "data"          : {
                    "ifaddrs"   : PLACEHOLDER_STRING,
                    "ifstats"   : PLACEHOLDER_STRING
                }
            }
        )
        self.logger.info(
            "Setup complete for probe: %s"
            %self.name
        )
        return

    def _run(self):
            """
            Runs the data collection.

            :return:
            """

            self.logger.info(
                "Running the data collection."
            )

            # Get Addreses
            address = psutil.net_if_addrs()

            # Get stats
            stats = psutil.net_if_stats()

            # Set the data
            template = self.get_template()
            data = template['data']
            data['ifaddrs'].update(
                {
                    'ifaddrs' : address,
                }
            )
            data = template['data']
            data['ifstats'].update(
                {
                    'ifstats' : stats,
                }
            )
            template['data'].update(
                {
                    'data' : data
                }
            )

            # Update the data
            self.set_data(
                template
            )
            self.logger.info(
                "Data collection complete."
            )
            # Delete the temp objects
            del template,   \
                address,    \
                stats,      \
                data
            return

class DynamicIfaceProbe(HostProbe):
    """
    This is the user probe that scans what interface are on
    a specific system.

    extends: Probe
    """

    # The class name
    name        = "IfaceProbe"

    # The probe type
    type        = "Iface"

    # Description
    description = \
    "Gets the interfaces on the probe that is running."

    # Fields for filtering
    fields      = []

    # Groups
    groups      = [
        "iface",
        "reconnaissance"
    ]

    # Definition
    definition  = {}

    # Template
    template    = {}

    # Data
    data        = {}

    # Continuous flag
    continuous  = True

    # Interval
    interval    = 3

    def __init__(self, queue):
        """
        We call the constructor for the class.

        :return:
        """

        # Setup the class object
        HostProbe.__init__(
            self,
            self.name,
            queue,
            self.continuous
        )
        self.logger.info(
            "Created a new Probe of type: %s" %self.type
        )
        return

    def setup(self):
        """
        Setup the probe.

        :return:
        """

        # Register all handles
        self.set_data(
            self.data
        )
        self.register_type(
            self.type
        )
        self.set_definition(
            {
                "type"          : self.get_type(),
                "name"          : self.name,
                "description"   : self.description,
                "default"       : "yes",
                "help"          : self.description,
                "tag"           : self.name,
                "fields"        : PLACEHOLDER_ARRAY,
                "groups"        : PLACEHOLDER_ARRAY,
            }
        )
        self.set_template(
            {
                "definition"    : self.set_definition(),
                "data"          : {
                    "counter"   : PLACEHOLDER_STRING,
                    "cnxs"      : PLACEHOLDER_STRING,
                    "netstats"  : PLACEHOLDER_STRING,
                }
            }
        )
        self.logger.info(
            "Setup complete for probe: %s"
            %self.name
        )
        return

    def _run(self):
            """
            Runs the data collection.

            :return:
            """

            self.logger.info(
                "Running the data collection."
            )

            # Get stats
            stats = psutil.net_if_stats()

            # Get the counters
            counters = psutil.net_io_counters(pernic=True)

            # Get the connections
            connections = psutil.net_connections()

            # Set the data
            template = self.get_template()
            data = template['data']
            data['counter'].update(
                {
                    'counters' : counters,
                }
            )
            data = template['data']
            data['cnxs'].update(
                {
                    'cnxs' : connections,
                }
            )
            data = template['data']
            data['netstats'].update(
                {
                    'netstats' : stats,
                }
            )
            template['data'].update(
                {
                    'data' : data,
                }
            )

            # Update the data
            self.set_data(
                template
            )
            self.logger.info(
                "Data collection complete."
            )
            # Delete the temp objects
            del template,   \
                counters,   \
                stats,      \
                connections,\
                data

            time.sleep(
                self.interval
            )
            return

class IfaceProbe(MutableProbe):
    """
    This is the interface probe container that contains both the
    static probe and the dynamic probeing agents.
    """

    # Check the probe type
    __types         = {
        "dynamic"   : DynamicIfaceProbe,
        "static"    : StaticIfaceProbe
    }

    def __init__(self, type, queue):
        """
        This is the constructor that will set the self
        object to the appropriate object type.

        :param type:            Probe type
        :param queue:           Application queue
        :return:
        """

        # Override the class
        MutableProbe.__init__(self, self.__types)

        # Run the object
        self.run(type, queue)
        return