from functools import wraps


def action(label):
    """Decorator to convert a function to a callable usable by the Action
    class.

    Args:
        label (str): The label to show before executing the action.
    """

    def wrapper(f):
        """
        Returns:
            bool: Indicates whether or not the action was successful. Returns
            True if the function returned True (or does not have a return
            value). Otherwise returns False.
        """
        f.label = label

        @wraps(f)
        def wrap(*args, **kwargs):
            result = f(*args, **kwargs)

            if result is None:
                result = True

            return bool(result)

        return wrap

    return wrapper
