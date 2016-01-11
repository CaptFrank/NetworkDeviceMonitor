"""

    :UserProbe:
    ==========

    :
    This is the user probe that gets all
    users on a system. We use this probe to gain
    a comprehensive view of who is on the system.
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

class UserProbe(HostProbe):
    """
    This is the user probe that scans what users are on
    a specific system.

    extends: Probe
    """

    # The class name
    name        = "UserProbe"

    # The probe type
    type        = "Users"

    # Description
    description = \
    "Gets the users on the probe that is running."

    # Fields for filtering
    fields      = []

    # Groups
    groups      = [
        "users",
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
                    "users"     : PLACEHOLDER_STRING,
                    "boot"      : PLACEHOLDER_STRING
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
            users = [
                tuple_to_dict(
                    item
                ) for item in psutil.users()
            ]

            boot_time = psutil.boot_time()

            template = self.get_template()
            data = template['data']
            data.update(
                {
                    "users"    : users
                }
            )
            data = template['data']
            data.update(
                {
                    "boot"     : boot_time
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
                users,      \
                boot_time
            gc.collect()
            return