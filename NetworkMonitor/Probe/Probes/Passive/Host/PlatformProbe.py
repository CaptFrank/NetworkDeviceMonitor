"""

    :PlatformProbe:
    ==========

    :
    This probe monitor that gets teh platform information
    of the system that it is running on.
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
import platform
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

class PlatformProbe(HostProbe):
    """
    This is the platform probe that gets the
    platform that is used to run this probe.

    extends: Probe
    """

    # The class name
    name        = "PlatformProbe"

    # The probe type
    type        = "Platform"

    # Description
    description = \
    "Gets the platform on which this probe is running."

    # Fields for filtering
    fields      = []

    # Groups
    groups      = [
        "platform",
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
                        "system"        : PLACEHOLDER_STRING,
                        "node"          : PLACEHOLDER_STRING,
                        "release"       : PLACEHOLDER_STRING,
                        "version"       : PLACEHOLDER_STRING,
                        "machine"       : PLACEHOLDER_STRING,
                        "processor"     : PLACEHOLDER_STRING,
                        "architecture"  : PLACEHOLDER_STRING,
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

        results = dict(
            zip(
                platform.uname()._fields,
                list(
                    platform.uname()
                )
            )
        )

        template = self.get_template()
        data = template['data']
        data.update(
            results
        )
        data = template['data']
        data.update(
           {
               "architecture" : platform.architecture()
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
            data,       \
            results
        gc.collect()
        return


