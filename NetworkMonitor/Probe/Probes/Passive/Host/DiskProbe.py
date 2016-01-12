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
class StaticDiskProbe(HostProbe):
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
                    "definition"    : self.get_definition(),
                    "data"          : {
                        "partitions"    : PLACEHOLDER_ARRAY,
                        "usage"         : {
                            "path"      : "/",
                            "total"     : PLACEHOLDER_STRING,
                            "used"      : PLACEHOLDER_STRING,
                            "free"      : PLACEHOLDER_STRING,
                            "percent"   : PLACEHOLDER_STRING,
                        },
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
            data.update(
                {
                    "partitions"    : partitions
                }
            )
            data = template['data']
            data.update(
                {
                    "usage"         : usage
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
                usage,      \
                partitions
            return

class DynamicDiskProbe(HostProbe):
        """
        This is the dynamic disk data probe.
        This probe will get certain data pieces such as disk usage,
        disk io read / writes.
        """

        # The class name
        name        = "DiskProbe-Dynamic"

        # The probe type
        type        = "Disk"

        # Description
        description = \
        "Gets the dynamic disk data on which this probe is running."

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
                        {
                            "usage"         : {
                                "path"          : "/",
                                "total"         : PLACEHOLDER_STRING,
                                "used"          : PLACEHOLDER_STRING,
                                "free"          : PLACEHOLDER_STRING,
                                "percent"       : PLACEHOLDER_STRING
                            },
                            "io"            : {
                                "reads_count"   : PLACEHOLDER_STRING,
                                "writes_count"  : PLACEHOLDER_STRING,
                                "read_bytes"    : PLACEHOLDER_STRING,
                                "write_bytes"   : PLACEHOLDER_STRING,
                                "read_time"     : PLACEHOLDER_STRING,
                                "write_time"    : PLACEHOLDER_STRING
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

            usage = tuple_to_dict(
                psutil.disk_usage(
                    path='/'
                )
            )

            io = tuple_to_dict(
                psutil.disk_io_counters(perdisk=False)
            )

            template = self.get_template()
            data = template['data']
            data.update(
                {
                    "io"            : io
                }
            )
            data = template['data']
            data.update(
                {
                    "usage"         : usage
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
                usage,      \
                io
            return

class DiskProbe(MutableProbe):
    """
    This the disk probe container that contains both the
    static probe and the dynamic probing agents.
    """

    # Check the probe types
    __types         = {
        "dynamic"   : DynamicDiskProbe,
        "static"    : StaticDiskProbe
    }

    def __init__(self, type, queue):
        """
        This is the constructor that will set the self
        object to the appropriate object type.

        :param type:        Probe type
        :param queue:       Application queue
        :return:
        """

        # Override the class
        MutableProbe.__init__(self, self.__types)

        # Run the object
        self.run(type, queue)
        return