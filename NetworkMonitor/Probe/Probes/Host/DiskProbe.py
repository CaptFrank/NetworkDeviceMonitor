"""

    :DiskProbe:
    ==========

    :
    This is the probe that monitors the disk usage,
    io counts and partitions.

    We can set the io writes and reads to be monitored.
    In any case this probe provides 2 type of probes, a
    static usage probe and a dynamic usage probe.
    :

    :copyright: (c) 10/23/2015 by fpapinea.
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
    import Probe

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

class DiskProbe(object):
    """
    This the disk probe container that contains both the
    static probe and the dynamic probing agents.
    """

    class StaticDiskProbe(Probe):
        """
        This is the static disk data probe.
        This probe will get certain data pieces such as disk usage,
        disk partitions and disk information.
        """


        # The class name
        name        = "DiskProbe-Static"

        # The probe type
        type        = "Disk"

        # Description
        description = \
        "Gets the static disk data on which this probe is running."

        # Fields for filtering
        fields      = []

        # Groups
        groups      = [
            "disk",
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

            # Setup the base object
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
                            "partitions"    : [],
                            "usage"         : {
                                "path"      : "/",
                                "total"     : "",
                                "used"      : "",
                                "free"      : "",
                                "percent"   : ""
                            },
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

            # Get partitions
            partitions = [
                tuple_to_dict(
                    item
                ) for item in psutil.disk_partitions(
                    all=True
                )
            ]

            usage = tuple_to_dict(
                psutil.disk_usage(
                    path='/'
                )
            )

            template = self.get_template()
            data = template['data']
            data = data.update(
                {
                    "partitions"    : partitions
                }
            )
            data = data.update(
                {
                    "usage"         : usage
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
                usage,      \
                partitions
            gc.collect()
            return

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

    class DynamicDiskProbe(Probe):
        """
        This is the dynamic disk data probe.
        This probe will get certain data pieces such as disk usage,
        disk io read / writes.
        """

        def __init__(self, queue):

            return

    def __init__(self, type, queue):

        return