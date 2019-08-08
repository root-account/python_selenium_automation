import logging

from .class_stateful_action import StatefulAction


logger = logging.getLogger(__name__)


def _null(action):
    pass


class Actions(object):
    """Represents a group of actions that performs tasks.
    """

    def __init__(self, *actions):
        """Instantiates a new group of actions.

        Args:
            actions (*Action): A list of actions to perform.
        """
        self._actions = [action for action in actions if not action._finally]
        self._finally = [action for action in actions if action._finally]
        self._state = {}
        self.success = False

    def __call__(self, pre_action=_null, post_action=_null):
        """Perform all actions.

        Args:
            pre_action (callable): An optional callable to call before an
            Action is executed. This function receives the Action as the first
            argument. Defaults to doing nothing.
            post_action (callable): An optional callable to call after an
            Action is executed. This function receives the Action as the first
            argument. Defaults to doing nothing.

        Raises:
            ActionFailed: When any Action fails during its execution.
        """
        self.success = False

        try:
            for action in self._actions:
                action(True, self._state, pre_action, post_action)
                self._save_state(action)

            self.success = True

        finally:
            for action in self._finally:
                try:
                    action(self.success, self._state, pre_action, post_action)
                    self._save_state(action)

                except Exception:
                    logger.exception("Failed running %s", action.label)

    def _save_state(self, action):
        if isinstance(action, StatefulAction):
            self._state.update(action.results)
