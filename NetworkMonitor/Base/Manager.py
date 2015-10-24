"""

    :Manager:
    ==========

    :
    This is the class that will read the location of the
    plugins and will load them in the context of the application.
    It is the plugin manager.
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
from yapsy.MultiprocessPluginManager \
    import MultiprocessPluginManager

"""
=============================================
Constants
=============================================
"""

# Program Attributes
__author__      =   "gammaRay"
__version__     =   "1.0"
__date__        =   "9/28/2015"


"""
=============================================
Source
=============================================
"""

class PluginManager(MultiprocessPluginManager):
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

    def __init__(self):
        """
        This is the constructor for the class.
        Here we instantiate a logger and override the super class.

        :return:
        """

        self._logger = logging.getLogger("PluginManager")
        MultiprocessPluginManager.__init__(self)
        return

    def setup(self):

        return


