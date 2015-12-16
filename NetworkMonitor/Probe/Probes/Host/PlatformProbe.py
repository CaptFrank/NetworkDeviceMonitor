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

class PlatformProbe(Probe):
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
                        "system"        : PLACEHOLDER,
                        "node"          : PLACEHOLDER,
                        "release"       : PLACEHOLDER,
                        "version"       : PLACEHOLDER,
                        "machine"       : PLACEHOLDER,
                        "processor"     : PLACEHOLDER,
                        "architecture"  : PLACEHOLDER,
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

        with platform.uname() as data:
            results = dict(
                zip(
                    data._fields,
                    list(
                        data
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
            results
        gc.collect()
        return


