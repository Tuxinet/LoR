__author__ = 'asarium'

from abc import ABCMeta, abstractmethod


class State(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.gameMachine = None

    @abstractmethod
    def enterState(self):
        pass

    @abstractmethod
    def leaveState(self):
        pass

    @abstractmethod
    def getName(self):
        pass

    def setStateMachine(self, gameMachine):
        """

        :type gameMachine: core.GameStateMachine.GameStateMachine
        """
        self.gameMachine = gameMachine