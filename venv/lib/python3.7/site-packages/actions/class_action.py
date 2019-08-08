import logging

from .class_action_failed import ActionFailed
from .class_state import State


logger = logging.getLogger(__name__)


class Action(object):
    """Represents an executable action.
    """

    def __init__(self, func, *args, **kwargs):
        """Instantiates a new executable action.

        Args:
            func (function): The funcion to execute. This function must be
            decorated with action.

            *args: Any additional arguments required by func.

            enabled (bool|State): A keyword argument that, if set to False,
            disables the Action from executing. A State instance can also be
            passed in for lazy evaluation. Defaults to True.

            pass_success (bool): A keyword argument that, if set to True,
            passes in the success of all other actions executed thus far as a
            boolean keyword argument to the func function.

            _finally (bool): A keyword argument that, if set to True, makes the
            action execute after all other actions have been executed. This
            will ensure the action is executed even if other actions failed.
            This is typically used for cleanup tasks. Return values from these
            actions are ignored. Defaults to False.

        Raises:
            ValueError: When the given function doesn't have a label set by the
            action decorator.
        """
        self._func = func
        self._args = args
        self._kwargs = {}
        self._enabled = kwargs.get("enabled", True)
        self._pass_success = bool(kwargs.get("pass_success", False))
        self._finally = bool(kwargs.get("_finally", False))

        if not hasattr(func, "label"):
            raise ValueError("%s is missing label. Make sure it uses the "
                "action decorator." % func.__name__)

        self.label = func.label

    def __call__(self, success, state, pre_action, post_action):
        """Perform the action.

        Args:
            success (bool): Whether or not the last action was successful or
            otherwise failed.
            state (dict): A group of values that have been saved by other
            Action instances.

        Raises:
            ActionFailed: When the Action fails during its execution.
        """
        if not self._is_enabled(state):
            logger.debug("Skipping '%s'", self.label)
            return True

        pre_action(self)

        if self._pass_success:
            self._kwargs["success"] = success

        args = self._inject_state_into_args(state, self._args)

        our_success = False
        try:
            our_success = self._func(*args, **self._kwargs)

        except Exception:
            logger.exception("Error running '%s'", self.label)

        if not our_success:
            raise ActionFailed(self.label)

        post_action(self)

    def _is_enabled(self, state):
        """Returns whether or not the Action is enabled.

        This lazy evaluates the enabled flag using the given state.

        Args:
            state (dict): A group of values that have been saved by other
            Action instances.

        Returns:
            bool: True if this Action is enabled. False otherwise.
        """
        enabled = True

        if isinstance(self._enabled, State):
            enabled = bool(state.get(
                self._enabled.name, self._enabled.default))

        else:
            enabled = bool(self._enabled)

        return enabled

    def _inject_state_into_args(self, state, args):
        """Lazy evaluates arguments by injecting state.

        Args:
            state (dict): The storage of state.
            args (list[mixed]): The list of arguments to inject state into.

        Returns:
            list[mixed]: The given args that have been lazy evaluated with
            injected state.
        """
        final_args = []
        for arg in args:
            if isinstance(arg, State):
                try:
                    final_args.append(state[arg.name])

                except KeyError:
                    raise KeyError("'%s' does not exist in saved state for "
                        "Action '%s'. Current state: %s" % (
                            arg.name, self.label, state))

            else:
                final_args.append(arg)

        return final_args
