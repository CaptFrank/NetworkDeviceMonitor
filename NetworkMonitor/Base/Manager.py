"""

    :Manager:
    ==========

    :
    This is the class that will read the location of the
    plugins and will load them in the context of the application.
    It is the configuration manager.
    :

    :copyright: (c) 2015-10-23 by gammaRay.
    :license: BSD, see LICENSE for more details.

    Author:         gammaRay
    Version:        :1.0:
    Date:           2015-10-23
    
"""

"""
=============================================
Imports
=============================================
"""

import logging

from NetworkMonitor.config \
    import CONFIG_WORKSPACE
from NetworkMonitor.Base.Reader \
    import Reader
from yapsy.PluginManager \
    import PluginManager

"""
=============================================
Constants
=============================================
"""

# Program Attributes
__author__          =   "gammaRay"
__version__         =   "1.0"
__date__            =   "9/28/2015"

# Plugin type reference
PLUGIN_TYPE         =   "PLUGIN_CONFIG"
PLUGIN_DEFAULT      =   "DEFAULT"
PLUGIN_DEFAULT_LOC  =   "./Configs/Plugins"
PLUGIN_EXTENSION    =   "plugin"


"""
=============================================
Source
=============================================
"""

class Manager(PluginManager):
    """
    This class defines the interface to the plugins that are
    loaded dynamically based on the configuration file given
    to this engine.

    From the config file, we can determine which plugins are
    needed and which ones to download from the centralized
    plugin server.
    """

    # The logger engine
    _logger             = None

    # The configurations manager
    # *** Note: this reader is the global reader for the application
    _manager            = None

    # The plugins configuration
    _configs            = None

    # The plugin objects
    _plugins            = None

    # The workspace
    _workspace          = CONFIG_WORKSPACE

    # The running plugins
    _running            = {}

    def __init__(self):
        """
        This is the constructor for the class.
        Here we instantiate a logger and override the super class.

        :return:
        """

        # Set the logger object
        self._logger = logging.getLogger(
            "PluginManager"
        )

        # Override the super class
        PluginManager.__init__(self)
        self.setPluginInfoExtension(PLUGIN_EXTENSION)

        # Set the internal configurations manager - Singleton
        self._manager = Reader()
        return

    def setup(self):
        """
        This is the method that will read the plugins configuration and
        load the ones that are addressed.

        :return:
        """

        # Load configs
        self._load_plugins_configs()

        # Load plugins
        self._load_plugins()
        return

    def run(self, plugin=None):
        """
        Default run method.

        :param plugin:          The runall method is called if None
        :return:
        """

        if plugin is None:
            self.run_all()
        else:
            self.run_plugin(plugin)
        return

    def run_plugin(self, name):
        """
        This only runs one plugin that is passed to the
        method.

        :param name:            The plugin name
        :return:
        """

        # Sanity check
        for plugin in self._plugins:
            if name == plugin.name:

                # We setup and run the plugin
                self._logger.info("[+] Running plugin: %s" %name)
                self._run_plugin(plugin)
                return

        # Couldn't find the plugin with that name
        self._logger.info("[-] Plugin: %s not found." %name)
        return

    def run_all(self):
        """
        This runs all the plugins in the enabled plugins.

        :return:
        """

        # Run all the plugin
        for plugin in self._plugins:
            self.run_plugin(plugin.name)
        return

    def kill_plugin(self, name):
        """
        This only kills one plugin that is passed to the
        method.

        :param name:            The plugin name
        :return:
        """

        # Sanity check
        for plugin in self._plugins:
            if name == plugin.name:

                # We setup and run the plugin
                self._logger.info("[-] Killing plugin: %s" %name)
                self._kill_plugin(plugin)
                return

        # Couldn't find the plugin with that name
        self._logger.info("[-] Plugin: %s not found." %name)
        return

    def kill_all(self):
        """
        This kills all the plugins in the enabled plugins.

        :return:
        """

        # Run all the plugin
        for plugin in self._plugins:
            self.kill_plugin(plugin.name)
        return

    def _run_plugin(self, plugin):
        """
        This is the internal method that calls the runnable plugin
        and sets it up, and starts it.

        :param plugin:          The plugin object that is needed to run
        :return:
        """

        # Activate the plugin
        plugin.plugin_object.activate()
        self._logger.info(
            "[+] Activating plugin: %s"
            %plugin.name
        )

        # Setup the plugin
        self._logger.info(
            "[+] Setting up plugin: %s"
            %plugin.name
        )
        plugin.plugin_object.setup(
            self._find_configs(
                plugin.name
            )
        )

        # Run the plugin
        self._logger.info(
            "[+] Running plugin: %s"
            %plugin.name
        )

        # Store the handle for the future
        self._running[plugin.name] = plugin.plugin_object.run()
        return

    def _kill_plugin(self, plugin):
        """
        This is the internal method that calls the runnable plugin
        and kills it as well as run the finally context.

        :param plugin:          The plugin object that is needed to be killed
        :return:
        """
        # Deactivate the plugin
        plugin.plugin_object.deactivate()
        self._logger.info(
            "[-] Deactivating plugin: %s"
            %plugin.name
        )

        # Kill the process
        self._running[plugin.name].kill()
        self._running[plugin.name].join()
        self._logger.info(
            "[-] Killed plugin: %s"
            %plugin.name
        )

        del self._running[plugin.name]
        return

    def _load_plugins_configs(self, workspace=None):
        """
        This is the configs loading method for the plugin manager.

        :param workspace:       The workspace where the plugins would be
                                located. Typically [./NetworkDeviceMonitor/Configs/App]
        :return:
        """

        # Here we do a sanity check or address the default location
        if workspace is not None:

            # Set the passed directory
            self._workspace = workspace

        # We load the configs
        self._logger.info(
            "[+] Loading the plugin workspace [%s]"
            %self._workspace
        )
        self._manager.load(
            self._workspace
        )

        # We check to see which ones are plugin configs.
        self._logger.info(
            "[+] Filtering plugins configurations."
        )
        self._configs = self._filter_plugin_configs()
        return

    def _load_plugins(self):
        """
        This is the method that will load the plugins based on the
        the Yapsy framework.

        :return:
        """

        self.setPluginPlaces(
            self._get_locations()
        )
        self.collectPlugins()

        def adjust(str1, value): return str1.ljust(20, " ") + value + '\n'
        """
        Adjusts a string to the logging format
        """

        # Set the appropriate plugins
        self._plugins = self._filter_plugins()

        # List the plugins available
        for plugin in self._plugins:

            # Print relevant information about the plugin.
            self._logger.info(
                "\n===========================\n"
                + adjust(
                    "Name: ",
                    plugin.name
                )
                + adjust(
                    "Author: ",
                    plugin.author
                )
                + adjust(
                    "Version: ",
                    str(
                        plugin.version
                    )
                )
                + adjust(
                    "Copyright: ",
                    plugin.copyright
                )
                + adjust(
                    "Website: ",
                    plugin.website
                )
                + adjust(
                    "Category: ",
                    plugin.category
                )
                + adjust(
                    "Path: ",
                    plugin.path
                )
                + adjust(
                    "Description: ",
                    plugin.description
                )
            )
        return

    def _filter_plugin_configs(self):
        """
        This method returns only the plugin configurations.

        :return:
        """

        # Container
        plugins = []

        # Get all plugins
        files = self._manager.get_configs()

        # Filter
        for file in files.values():
            for config in file:
                for plugin in config.values():
                    if plugin['type'] == PLUGIN_TYPE:

                        # Check where the location is
                        if plugin['location'] == PLUGIN_DEFAULT:
                            plugin['location'] = PLUGIN_DEFAULT_LOC

                        self._logger.info(
                            "[+] Found configurations for plugin: %s "
                            %plugin['name'] +
                            "Location: %s"
                            %plugin['location']
                        )

                        plugins.append(
                            plugin
                        )
        return plugins

    def _filter_plugins(self):
        """
        Filters the plugins that are needed and deletes the other ones.

        :return:
        """

        # Container
        filered_plugins = []

        # We need to only get the plugins needed
        plugins = self.getAllPlugins()
        for plugin in plugins:
            for config in self._configs:
                if (plugin.name in config['name']) \
                        and (plugin not in filered_plugins):
                    filered_plugins.append(plugin)
                elif plugin.name not in config['name']:
                    del plugin
        return filered_plugins

    def _find_configs(self, name):
        """
        Finds and returns the configs for a specific plugin.

        :param name:            The plugin name
        :return:
        """

        for plugin in self._configs:
            if name == plugin['name']:
                return plugin
        self._logger.info(
            "[-] Could not find configs for plugin: %s"
            %name
        )
        return

    def _get_locations(self):
        """
        This method returns the locations of the plugins.

        :return:
        """

        # Container
        locations = []

        # We look at the locations of the plugins and set them in the
        # plugin engine
        for plugin in self._configs:
            if plugin['location'] not in locations:
                locations.append(
                    plugin['location']
                )
        return locations
