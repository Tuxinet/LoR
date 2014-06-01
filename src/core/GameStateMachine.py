from core.State import State

__author__ = 'asarium'

from direct.fsm.FSM import FSM


class GameStateMachine(FSM):
    def __init__(self):
        FSM.__init__(self, "GameStateMachine")

        self.states = {}

    def __getattr__(self, item):
        if item.startswith("enter"):
            state = self.getState(item[len("enter"):])

            if state is not None:
                return state.enterState
            else:
                return None

        if item.startswith("exit"):
            state = self.getState(item[len("exit"):])

            if state is not None:
                return state.leaveState
            else:
                return None

    def getState(self, name):
        if name in self.states:
            return self.states[name]
        else:
            return None

    def addState(self, state):
        assert isinstance(state, State)

        state.setStateMachine(self)
        self.states[state.getName()] = state