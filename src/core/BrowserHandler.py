from core.GameShowBase import Instance

__author__ = 'asarium'

from cefpython3 import cefpython

Initialized = False
UpdateTask = None


def updateFunc(task):
    cefpython.MessageLoopWork()

    return task.cont


def initializeBrowser(settings=None):
    global Initialized
    global UpdateTask

    if Initialized:
        return

    if settings is None: settings = {}

    cefpython.Initialize(settings)

    UpdateTask = Instance.taskMgr.add(updateFunc, "ChromiumUpdateTask")

    Instance.finalExitCallbacks.append(shutdownBrowser)

    Initialized = True


def shutdownBrowser():
    Instance.taskMgr.remove(UpdateTask)

    cefpython.Shutdown()
