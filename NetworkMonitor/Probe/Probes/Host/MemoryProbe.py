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

class MemoryProbe(Probe):
    """
    This is the memory probing monitor. It
    gets the memory usage of a host that runs this probe.

    extends: Probe
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
                    {
                        "virtual"   : {
                            "total"     : PLACEHOLDER,
                            "available" : PLACEHOLDER,
                            "percent"   : PLACEHOLDER,
                            "used"      : PLACEHOLDER,
                            "free"      : PLACEHOLDER,
                            "active"    : PLACEHOLDER,
                            "inactive"  : PLACEHOLDER,
                            "buffers"   : PLACEHOLDER,
                            "cached"    : PLACEHOLDER,
                        },
                        "swap"      : {
                            "total"     : PLACEHOLDER,
                            "used"      : PLACEHOLDER,
                            "free"      : PLACEHOLDER,
                            "percent"   : PLACEHOLDER,
                            "sin"       : PLACEHOLDER,
                            "sout"      : PLACEHOLDER
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
                with tuple as data:
                    results = dict(
                        zip(
                            data._fields,
                            list(
                                data
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
            data = data.update(
                {
                    "virtual"    : vmem
                }
            )
            data = data.update(
                {
                    "swap"       : swap
                }
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
                vmem,       \
                swap
            gc.collect()
            return