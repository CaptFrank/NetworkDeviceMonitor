"""

    :Reader:
    ==========

    :
    This is the config reader. It is used to configure
    each probe and main application.
    :

    :copyright: (c) 8/5/2015 by gammaRay.
    :license: BSD, see LICENSE for more details.

    Author:         gammaRay
    Version:        :1.0:
    Date:           8/5/2015
"""

"""
=============================================
Imports
=============================================
"""

import os
import logging

from configobj import ConfigObj
from .Singleton import Singleton

"""
=============================================
Constants
=============================================
"""

""" The supported configs extensions """
SUPPORTED_EXT   = [
    '.ext',
    '.net',
    '.setup'
]

"""
=============================================
Source
=============================================
"""

def add_extension(ext):
    """
    This is the public access method to add
    a supported configs extension to the config reader
    framework.

    :param ext:                 The extension string to add
    :return:
    """

    SUPPORTED_EXT.append(ext)
    return

class Reader(Singleton):
    """
    This class object is the base configuration reader for
    the framework. We use this class to read in config files from
    each workspace and attribute them to a particular object.
    """

    # The internal reference to the configs
    _configs        = {}

    # Config extension
    _ext            = SUPPORTED_EXT

    # The logger object
    _logger         = None

    def __init__(self):
        """
         This is the default constructor for the class. We do not pass
         arguments to this object as it is a singleton object that is used
         within the entire context of the application.
        :return:
        """

        # Create a logger
        self._logger = logging.getLogger("Reader")

        # Make the class now a singleton class
        Singleton.__init__(self)
        return

    def load(self, workspace):
        """
        This method returns a kwarg argument after reading the contents of
        the config files in the workspace.

        :param workspace:           The workspace to read from
        :return: kwarg              The kwarg arguments
        """

        # Set the root directory to walk
        root = workspace

        self._logger.info(
            """
            ===========================
                   -- READER --
            ===========================
            """
        )

        # Go through the folders and look for the configs
        for dir, subdirs, files in os.walk(root):
            self._logger.info("Reading configs in: %s" %dir)

            # Get the directory name
            dirname = (dir.split("/")[-1]).lower()
            self._configs[dirname] = []

            # Go through the file one after another
            for file in files:


                # Check the extension
                if self.__check_extension(file):
                    self._logger.info("\t Found config: %s" %file)

                    # Read the args
                    args = self.read(dir + "/" + file)

                    # Check if none
                    if args is not None:

                        # Add the config to the internals
                        self._configs[dirname].append(args)
                        self._logger.info("\t\t Added config: %s" %file)

        self._logger.info(
            """
            ===========================
                   -- READER --
            ===========================
            """
        )
        return

    def read(self, file):
        """
        This is the default read mechanism for the Reader class.
        We use this method to read configurations based on the given file
        path.

        :param file:                The file path to read
        :return: kwargs             The dict for the attributes
        """

        # Check the extension
        if self.__check_extension(file):
            return ConfigObj(os.path.abspath(file))

    def get_configs(self):
        """
        This is the getter method for the read configurations
        internally stored.
        :return:
        """
        return self._configs

    def __check_extension(self, file):
        """
        This method returns true is the extension is a supported configs
        extension.

        :param file:                The file to read
        :return:                    True is supported
        """

        filename, ext = os.path.splitext(file)
        if ext in self._ext:
            return True
        else:
            return False