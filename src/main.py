from core.GameShowBase import Instance
from core.states.InitializeState import InitializeState
from core.states.MainMenuState import MainMenuState

__author__ = 'asarium'


def initializeGameStates():
    Instance.gameStateMachine.addState(InitializeState())
    Instance.gameStateMachine.addState(MainMenuState())


initializeGameStates()

Instance.gameStateMachine.request("Initialize")

Instance.run()


