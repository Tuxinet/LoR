from direct.showbase.ShowBase import ShowBase
from core.GameStateMachine import GameStateMachine
from core.Configuration import Configuration

__author__ = 'asarium'


class GameShowBase(ShowBase):
    def __init__(self, fStartDirect=True, windowType=None):
        # This has to be done before ShowBase is initialized
        self.configuration = Configuration()
        self.configuration.loadConfiguration()

        ShowBase.__init__(self, fStartDirect, windowType)

        self.gameStateMachine = GameStateMachine()

Instance = GameShowBase()