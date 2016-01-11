"""

    :MemoryProbe:
    ==========

    :
    This is the memory monitoring probe.
    This probe reports on a recurring basis
    the memory usage of a host.
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
import psutil
from NetworkMonitor.Probe.HostProbe \
    import HostProbe, PLACEHOLDER_STRING, \
    PLACEHOLDER_ARRAY, PLACEHOLDER_DICT

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

class MemoryProbe(HostProbe):
    """
    This is the memory probing monitor. It
    gets the memory usage of a host that runs this probe.

    extends: HostProbe
    """

    # The class name
    name        = "MemoryProbe"

    # The probe type
    type        = "Memory"

    # Description
    description = \
    "Gets the memory usage of where the probe is running."

    # Fields for filtering
    fields      = []

    # Groups
    groups      = [
        "memory",
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
                "fields"        : PLACEHOLDER_ARRAY,
                "groups"        : PLACEHOLDER_ARRAY,
            }
        )
        self.set_template(
            {
                "definition"    : self.set_definition(),
                "data"          : {
                    {
                        "virtual"   : {
                            "total"     : PLACEHOLDER_STRING,
                            "available" : PLACEHOLDER_STRING,
                            "percent"   : PLACEHOLDER_STRING,
                            "used"      : PLACEHOLDER_STRING,
                            "free"      : PLACEHOLDER_STRING,
                            "active"    : PLACEHOLDER_STRING,
                            "inactive"  : PLACEHOLDER_STRING,
                            "buffers"   : PLACEHOLDER_STRING,
                            "cached"    : PLACEHOLDER_STRING,
                        },
                        "swap"      : {
                            "total"     : PLACEHOLDER_STRING,
                            "used"      : PLACEHOLDER_STRING,
                            "free"      : PLACEHOLDER_STRING,
                            "percent"   : PLACEHOLDER_STRING,
                            "sin"       : PLACEHOLDER_STRING,
                            "sout"      : PLACEHOLDER_STRING
                        }
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

            # Tuple to dict
            def tuple_to_dict(tuple):
                results = dict(
                    zip(
                        tuple._fields,
                        list(
                            tuple
                        )
                    )
                )
                return results

            # Get mem usage
            vmem = tuple_to_dict(
                psutil.virtual_memory()
            )

            swap = tuple_to_dict(
                psutil.swap_memory()
            )

            template = self.get_template()
            data = template['data']
            data.update(
                {
                    "virtual"    : vmem
                }
            )
            data = template['data']
            data.update(
                {
                    "swap"       : swap
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
                data,       \
                vmem,       \
                swap
            gc.collect()
            return