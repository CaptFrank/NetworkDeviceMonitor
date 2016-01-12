"""

    :ProcessProbe:
    ==========

    :
    This is the process monitoring probe.
    This reports on a reoccurring basis the memory
    usage of the host.:

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

import os
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

class ProcessProbe(HostProbe):
    """
    This is the process probing monitor. It gets multiple aspects
    of the process from this probe.

    extends: HostProbe
    """

    # The class name
    name        = "ProcessProbe"

    # The probe type
    type        = "Process"

    # Description
    description = \
    "Gets the process attributes of where the probe is running."

    # Fields for filtering
    fields      = []

    # Groups
    groups      = [
        "process",
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

        # Check if ran as root
        if not os.geteuid() == 0:

            # If not root delete the self object and return
            self.logger.error(
                "To run the process probe, you need to run the "
                "plugin framework as root!. Deleting the probe "
                "and returning."
            )
            del self
            gc.collect()
            return

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
                "data"          : PLACEHOLDER_ARRAY,
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

            # database
            database = {}

            # Get the pids
            pids = self.__getpids()

            template = self.get_template()
            data = template['data']

            # We construct a database of attributes
            for pid in pids:
                data = self.__getattrs(
                    pid
                )
                database[pid] = data

            data.update(
                {
                    'data' : database,
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
                pids,       \
                database
            return

    def __getpids(self):
        """
        This method gets the running pids.

        :return:            An array of running pids
        """
        return psutil.pids()

    def __getattrs(self, pid):
        """
        This is the attributes getter method that does all the
        retrieval of all data.

        :param pid:         The process pid
        :return:            The data as a dict
        """

        # The data
        data = {}

        # Get the process
        process = psutil.Process(pid)
        if process is None:
            return None

        # Tuple to dict
        def tuple_to_dict(data):
            results = dict(
                zip(
                    data._fields,
                    list(
                        data
                    )
                )
            )
            return results

        # Get the attributes
        data['name']        = process.name()
        data['exec']        = process.exe()
        data['cwd']         = process.cwd()
        data['cmdline']     = process.cmdline()
        data['status']      = process.status()
        data['username']    = process.username()
        data['created']     = process.create_time()
        data['terminal']    = process.terminal()
        data['uids']        = tuple_to_dict(
            process.uids()
        )
        data['gids']        = tuple_to_dict(
            process.gids()
        )
        data['cputimes']    = tuple_to_dict(
            process.cpu_times()
        )
        data['cpupercent']  = process.cpu_percent(
            interval=1.0
        )
        data['cpuaffinity'] = process.cpu_affinity()
        data['memusage']    = process.memory_percent()
        data['meminfo']     = tuple_to_dict(
            process.memory_info()
        )
        data['memextern']   = tuple_to_dict(
            process.memory_info_ex()
        )
        data['memmap']      = [
            tuple_to_dict(
                memmap
            ) for memmap in process.memory_maps()
        ]
        data['io']          = tuple_to_dict(
            process.io_counters()
        )
        data['openfiles']   = [
            tuple_to_dict(
                file
            ) for file in process.open_files()
        ]
        data['connections'] = [
            tuple_to_dict(
                connection
            ) for connection in process.connections()
        ]
        data['threads']     = [
            tuple_to_dict(
                thread
            ) for thread in process.threads()
        ]
        data['ctxswitches'] = [
            tuple_to_dict(
                switch
            ) for switch in process.num_ctx_switches()
        ]
        data['nice']        = process.nice()
        data['ionice']      = tuple_to_dict(
            process.ionice()
        )
        data['rlimit']      = process.rlimit(
            psutil.RLIMIT_NOFILE
        )

        # Return the data
        return data




