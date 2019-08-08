import logging

import bunch

from .class_action import Action


logger = logging.getLogger(__name__)


class StatefulAction(Action):
    """Represents an executable action that stores state.

    When called, the `func` is passed in an extra keyword bunch.Bunch argument
    called `result_store`. (Bunch is a dict-like object where values can be set
    via attributes.) This can be used by the callable to store state.

    State can be passed onto other actions by referencing a State instance.
    """

    def __init__(self, func, *args, **kwargs):
        """Instantiates a new executable action. Same as Action parent class.

        Args:
            state (list[str]): Names of states that will be saved in the result
            store. After calling the StatefulAction action, these values will
            be retrievable via the results property.
        """
        self._expected_states = kwargs.get("state", [])
        self._result_store = bunch.Bunch()
        super(StatefulAction, self).__init__(func, *args, **kwargs)
        self._kwargs["result_store"] = self._result_store

    @property
    def results(self):
        """Retrieves all the state saved after calling the StatefulAction.

        If any expected state is missing, it defaults to None.

        Returns:
            dict: A dict representing the saved state of the StatefulAction.
        """
        state = {}

        for expected_state in self._expected_states:
            value = None

            if expected_state in self._result_store:
                value = self._result_store[expected_state]

            else:
                logger.debug("'%s' not found in result store for '%s' "
                    "StatefulAction", expected_state, self.label)

            state[expected_state] = value

        return state
