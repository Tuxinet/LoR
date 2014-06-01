__author__ = 'asarium'

from panda3d.core import loadPrcFile

class Configuration():
    def __init__(self):
        pass

    def loadConfiguration(self):
        loadPrcFile("LoR.prc")
