from direct.showbase.DirectObject import DirectObject
from core import BrowserHandler
from core.GameShowBase import Instance
from core.State import State

from cefpython3 import cefpython
from js.JavaScriptAPI import JavaScriptAPI
from js.MainMenuAPI import MainMenuAPI
from panda3dext.cef.Browser import Browser

__author__ = 'asarium'

global_settings = {
    "log_severity": cefpython.LOGSEVERITY_INFO,  # LOGSEVERITY_VERBOSE
    #"log_file": GetApplicationPath("debug.log"), # Set to "" to disable.
    "release_dcheck_enabled": True,  # Enable only when debugging.
    # This directories must be set on Linux
    "locales_dir_path": cefpython.GetModuleDirectory() + "/locales",
    "resources_dir_path": cefpython.GetModuleDirectory(),
    "browser_subprocess_path": "%s/%s" % (cefpython.GetModuleDirectory(), "subprocess"),
    "remote_debugging_port": 12345,
}

browser_settings = {
    "javascript_close_windows_disallowed": True,
    "javascript_open_windows_disallowed": True,
    "plugins_disabled": True,
    "java_disabled": True
}


class MainMenuState(State, DirectObject):
    def __init__(self):
        super(MainMenuState, self).__init__()
        self.browser = None

        self.jsAPI = JavaScriptAPI()
        self.menuAPI = MainMenuAPI(self)

        self.browserNodePath = None

        self.lastSize = (-1, -1)

        BrowserHandler.initializeBrowser(global_settings)

    def enterState(self):
        self.lastSize = (Instance.win.getXSize(), Instance.win.getYSize())

        self.browser = Browser()
        self.browser.initialURL = "http://vfs/data/html/mainMenu.html"
        self.browser.setSize(Instance.win.getXSize(), Instance.win.getYSize())
        self.browserNodePath = self.browser.create(Instance.win, browser_settings, transparent=False)
        self.browserNodePath.reparentTo(Instance.render2d)

        self.browser.installEventHandler()

        self.browser.jsBindings.SetObject("jsapi", self.jsAPI)
        self.browser.jsBindings.SetObject("menuAPI", self.menuAPI)

        self.browser.updateJSBindings()

        self.accept("window-event", self.windowEvent)

    def leaveState(self):
        self.ignoreAll()

        self.browser.removeEventHandler()

        self.browserNodePath.removeNode()

    def windowEvent(self, win):
        if win == Instance.win:
            newSize = (Instance.win.getXSize(), Instance.win.getYSize())

            if newSize[0] != self.lastSize[0] or newSize[1] != self.lastSize[1]:
                self.lastSize = newSize

                self.wasResized()

    def getName(self):
        return "MainMenu"

    def wasResized(self):
        self.browser.setSize(self.lastSize[0], self.lastSize[1])

