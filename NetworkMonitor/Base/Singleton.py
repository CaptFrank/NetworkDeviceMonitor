"""

    :Singleton:
    ==========

    :
    The classical singleton class
    :

    :copyright: (c) 8/18/2015 by gammaRay.
    :license: BSD, see LICENSE for more details.

    Author:         gammaRay
    Version:        :1.0:
    Date:           8/18/2015
"""

"""
=============================================
Source
=============================================
"""

class Singleton:
    """
    This is the base Singleton class object that is used in the
    application context. We use this class to allow for the use of
    only one object definition without having the need to reallocate
    space for another object.
    """

    class __Singleton:
        """
        This class is the attributes class. It contains all the attributes
        within the singleton class. We use this to access all the variables in
        a singleton object.
        """
        def __init__(self, arg):
            """
            This is the attribute singleton class default constructor.

            :param arg:             The argument to attribute to teh singleton
            """
            self.val = arg
            return

        def __str__(self):
            """
            The default string converter method for the singleton
            class object.

            :return:                The string representation of the object
            """
            return repr(self) + self.val

    # The class instance
    instance = None

    def __init__(self, arg=None):
        """
        This is the singleton top object class default constructor.
        We pass the arguments to it in order to attribute them to the
        singleton object.

        :param arg:                 The arguments to attribute to the object.
        """

        # Check to see if the singleton was already created.
        if not Singleton.instance:

            # If not created, create it and set the internals
            Singleton.instance = Singleton.__Singleton(arg)

        # If it was created use it
        else:
            Singleton.instance.val = arg

    def __getattr__(self, name):
        """
        This default method gets an attribute from the singleton instance and
        returns it if defined.

        :param name:                The attribute name
        :return:                    The attribute / null
        """
        return getattr(self.instance, name)
