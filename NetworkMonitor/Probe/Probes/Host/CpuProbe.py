"""

    :CPUProbe:
    ==========

    :
    This probe monitors the cpu load and the cpu
    attributes in the system continuously.
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

import gc
import time
import psutil
from NetworkMonitor.Probe.Probe \
    import Probe, PLACEHOLDER

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

class CPUProbe(Probe):
    """
    This is the CPU load, utilisation probe object.
    We use this object as a reoccurring object that
    polls the CPU attributes or time.

    extends: Probe
    """

    # The class name
    name        = "CPUProbe"

    # The probe type
    type        = "CPU"

    # Description
    description = \
    "Monitors CPU load avg and CPU attributes on the system " \
    "this probe is running on."

    # Fields for filtering
    fields      = []

    # Groups
    groups      = [
        "cpu",
        "performance",
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
    interval    = 5

    def __init__(self, queue):
        """
        We call the constructor for the class.

        :return:
        """

        # Setup the class object
        Probe.__init__(
            self,
            self.name,
            queue,
            self.continuous
        )
        self.logger.info(
            "Created a new Probe of type: %s" %self.type
        )
        gc.enable()
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
                "fields"        : [],
                "groups"        : [],
            }
        )
        self.set_template(
            {
                "definition"    : self.set_definition(),
                "data"          : {
                    "users"     : {
                        "user"      : PLACEHOLDER,
                        "system"    : PLACEHOLDER,
                        "idle"      : PLACEHOLDER,
                        "nice"      : PLACEHOLDER,
                        "iowait"    : PLACEHOLDER,
                        "irq"       : PLACEHOLDER,
                        "softirq"   : PLACEHOLDER,
                        "steal"     : PLACEHOLDER,
                        "guest"     : PLACEHOLDER,
                        "guest_nice": PLACEHOLDER,
                    },
                    "usage"     : {
                        "percentage": PLACEHOLDER,
                        "interval"  : PLACEHOLDER,
                        "load"      : PLACEHOLDER
                    },
                    "cpu"       : {
                        "count"     : PLACEHOLDER,
                        "logical"   : PLACEHOLDER
                    }
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

        # Gets the data from the psutil
        with psutil.cpu_times() as data:
            users = dict(
                zip(
                    data._fields,
                    list(
                        data
                    )
                )
            )

        # Try to get the avrg load
        try:
            load = self.__read_cpu(
                    '/proc/loadavg'
            )
        except Exception as e:
            self.logger.info("Error in data retrieval of cpu characteristics.")
            load = ""

        # Get the CPU counts
        counts = {
            "count"     : psutil.cpu_count(),
            "logical"   : psutil.cpu_count(
                logical=False
            ),
            "load"      : load
        }

        # Get the cpu usage
        usage = psutil.cpu_percent(
            self.interval,
            percpu=True
        )

        # Set the data
        template = self.get_template()
        data = template['data']
        data['users'] = data['users'].update(
            users
        )
        data = template['data']
        data['cpu'].update(
            counts
        )
        data = template['data']
        data['usage'].update(
            usage
        )
        template['data'].update(
            data
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
            data,       \
            users,      \
            counts,     \
            usage
        gc.collect()

        # Sleep the interval
        time.sleep(
            self.interval
        )
        return

    # Utility methods
    @staticmethod
    def __read_cpu(path):
        """
        Reads the cpu attributes.

        :param path:        Path to read
        :return:
        """
        cpu = open(path, "r")
        data = []

        # Get all lines in the cpu doc
        for line in cpu:
            for element in line.split(" "):
                data.append(element)

        # Create the channel list
        channel_list = [
            {
                "name": "Load Average 1min",
                "mode": "float",
                "kind": "Custom",
                "customunit": PLACEHOLDER,
                "value": float(
                    data[0]
                )
            },
            {
                "name": "Load Average 5min",
                "mode": "float",
                "kind": "Custom",
                "customunit": PLACEHOLDER,
                "value": float(
                    data[1]
                )
            },
            {
                "name": "Load Average 10min",
                "mode": "float",
                "kind": "Custom",
                "customunit": PLACEHOLDER,
                "value": float(
                    data[2]
                )
            }
        ]

        # Close the file
        cpu.close()

        # Return the channel list
        return channel_list



