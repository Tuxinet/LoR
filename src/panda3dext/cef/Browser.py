__author__ = 'asarium'

from panda3dext.cef.ClientHandler import ClientHandler
from panda3dext.cef.EventHandler import EventHandler

from cefpython3 import cefpython

from panda3d.core import Texture, VirtualFileSystem, CardMaker, NodePath


class Browser():
    def __init__(self):
        self.texture = None
        self.width = -1
        self.height = -1
        self.initialURL = None
        self.browser = None
        self.jsBindings = None
        self.eventHandler = None

    def setSize(self, width, height):
        if self.texture is None:
            self.texture = Texture()

        self.width = width
        self.height = height

        self.texture.setup2dTexture(width, height, Texture.TUnsignedByte, Texture.FRgba)

        if self.browser is not None:
            self.browser.WasResized()

    def create(self, window, settings=None, transparent=True):
        """
        Creates the browser and returns a NodePath which can be used to display the browser

        :type window: libpanda.GraphicsWindow
        :type settings: dict
        :type transparent: bool
        :return: The new nodepath
        """
        if not settings: settings = {}

        windowInfo = cefpython.WindowInfo()

        if window is not None:
            windowHandle = window.getWindowHandle().getIntHandle()
            windowInfo.SetAsOffscreen(windowHandle)
        else:
            windowInfo.SetAsChild(0)

        windowInfo.SetTransparentPainting(transparent)

        if self.texture is None:
            if window is None:
                raise RuntimeError("Texture is not initialized and no window was given!")
            else:
                self.setSize(window.getXSize(), window.getYSize())

        self.browser = cefpython.CreateBrowserSync(windowInfo, settings, self.initialURL)
        self.browser.SendFocusEvent(True)
        self.browser.SetClientHandler(ClientHandler(self.browser, self.texture))
        self.browser.WasResized()

        self.jsBindings = cefpython.JavascriptBindings(bindToFrames=False, bindToPopups=True)

        self.browser.SetJavascriptBindings(self.jsBindings)

        # Now create the node
        cardMaker = CardMaker("browser2d")
        cardMaker.setFrameFullscreenQuad()
        node = cardMaker.generate()

        nodePath = NodePath(node)
        nodePath.setTexture(self.texture)

        return nodePath

    def installEventHandler(self):
        self.eventHandler = EventHandler(self.browser)
        self.eventHandler.installEventHandlers()

    def removeEventHandler(self):
        if self.eventHandler is None:
            raise RuntimeError("Event handler was never installed!")

        self.eventHandler.removeEventHandlers()
        del self.eventHandler

    def updateJSBindings(self):
        self.browser.SetJavascriptBindings(self.jsBindings)

    @staticmethod
    def initializeChromium(settings, debug=False):
        cefpython.g_debug = debug
        cefpython.Initialize(settings)

    @staticmethod
    def doMessageLoopWork(task):
        cefpython.MessageLoopWork()
        return task.cont

    @staticmethod
    def shutdownChromium():
        cefpython.Shutdown()
