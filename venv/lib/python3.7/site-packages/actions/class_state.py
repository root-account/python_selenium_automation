class State(object):
    """Represents a value that was created in one StatefulAction and passed
    into another Action.

    This allows for Actions to be declarative and lazy evaluated.
    """

    def __init__(self, name, default=None):
        """Instantiates the instance.

        Args:
            name (str): The name of the value that this State represents.
            default (bool): The default value to use when the evaluated value
            is missing. Defaults to None.
        """
        self.name = name
        self.default = default
