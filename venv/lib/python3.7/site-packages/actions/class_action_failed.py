class ActionFailed(Exception):
    """Exception that's thrown when an Action fails.

    The label of the Action is stored publically in the `label` attribute.
    """

    def __init__(self, label):
        """Instantiates the instance.

        Args:
            label (str): The label of the Action that failed.
        """
        self.label = label
