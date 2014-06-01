from core.GameShowBase import Instance
from core.State import State

__author__ = 'asarium'


class InitializeState(State):
    def __init__(self):
        super(InitializeState, self).__init__()

    def leaveState(self):
        pass  # Do nothing

    def enterState(self):
        self.gameMachine.forceTransition("MainMenu")


    def getName(self):
        return "Initialize"

