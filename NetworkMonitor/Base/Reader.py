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

from configobj import ConfigObj
from .Singleton import Singleton

"""
=============================================
Source
=============================================
"""

class Reader(Singleton):
    """
    This class object is the base configuration reader for
    the framework. We use this class to read in config files from
    each workspace and attribute them to a particular object.
    """

    # The internal reference to the configs
    _configs        = {}

    # Config extension
    _ext            = ".net"

    def __init__(self):
        """
         This is the default constructor for the class. We do not pass
         arguments to this object as it is a singleton object that is used
         within the entire context of the application.
        :return:
        """

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

        # Go through the folders and look for the configs
        for dir, subdirs, files in os.walk(root):
            print("[+] Reading configs in: %s" %dir)

            # Get the directory name
            dirname = (dir.split("/")[-1]).lower()
            self._configs[dirname] = []

            # Go through the file one after another
            for file in files:
                print("\t [+] Config: %s" %file)

                # Read the args
                args = self.read(dir + "/" + file)

                # Check if none
                if args is not None:

                    # Add the config to the internals
                    self._configs[dirname].append(args)
                    print("\t\t[+] Added Config: %s" %file)
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
        filename, ext = os.path.splitext(file)
        if ext == self._ext:
            return ConfigObj(os.path.abspath(file))
