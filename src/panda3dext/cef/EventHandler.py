
from cefpython3 import cefpython
from direct.showbase.DirectObject import DirectObject

__author__ = 'Marius'


class EventHandler(DirectObject):
    def __init__(self, browser):
        """

        :type browser: cefpython.PyBrowser
        """
        DirectObject.__init__(self)
        self.keyModifiers = 0
        self.modifierKeys = {
            "shift": cefpython.VK_SHIFT,
            "ctrl": cefpython.VK_CONTROL,
            "alt": cefpython.VK_MENU
        }
        self.translateKeys = {
            "f1": cefpython.VK_F1, "f2": cefpython.VK_F2,
            "f3": cefpython.VK_F3, "f4": cefpython.VK_F4,
            "f5": cefpython.VK_F5, "f6": cefpython.VK_F6,
            "f7": cefpython.VK_F7, "f8": cefpython.VK_F8,
            "f9": cefpython.VK_F9, "f10": cefpython.VK_F10,
            "f11": cefpython.VK_F11, "f12": cefpython.VK_F12,

            "arrow_left": cefpython.VK_LEFT,
            "arrow_up": cefpython.VK_UP,
            "arrow_down": cefpython.VK_DOWN,
            "arrow_right": cefpython.VK_RIGHT,

            "enter": cefpython.VK_RETURN,
            "tab": cefpython.VK_TAB,
            "space": cefpython.VK_SPACE,
            "escape": cefpython.VK_ESCAPE,
            "backspace": cefpython.VK_BACK,
            "insert": cefpython.VK_INSERT,
            "delete": cefpython.VK_DELETE,
            "home": cefpython.VK_HOME,
            "end": cefpython.VK_END,
            "page_up": cefpython.VK_PAGEUP,
            "page_down": cefpython.VK_PAGEDOWN,

            "num_lock": cefpython.VK_NUMLOCK,
            "caps_lock": cefpython.VK_CAPITAL,
            "scroll_lock": cefpython.VK_SCROLL,

            "lshift": cefpython.VK_LSHIFT,
            "rshift": cefpython.VK_RSHIFT,
            "lcontrol": cefpython.VK_LCONTROL,
            "rcontrol": cefpython.VK_RCONTROL,
            "lalt": cefpython.VK_LMENU,
            "ralt": cefpython.VK_RMENU,
        }

        self.lastY = None
        self.lastX = None
        self.browser = browser

    def getMousePixelCoordinates(self, mouse):
        # This calculation works only for the browser area.
        x = (mouse.getX() + 1) / 2.0 * base.win.getXSize()
        y = (-mouse.getY() + 1) / 2.0 * base.win.getYSize()

        return x, y

    def mouseEvent(self, button, up):
        if base.mouseWatcherNode.hasMouse():
            mouse = base.mouseWatcherNode.getMouse()
            (x, y) = self.getMousePixelCoordinates(mouse)

            type = None
            if button == 1:
                type = cefpython.MOUSEBUTTON_LEFT
            elif button == 2:
                type = cefpython.MOUSEBUTTON_MIDDLE
            else:
                type = cefpython.MOUSEBUTTON_RIGHT

            self.browser.SendMouseClickEvent(x, y, type, up, 1)

    def mouseWheelEvent(self, up):
        if base.mouseWatcherNode.hasMouse():
            mouse = base.mouseWatcherNode.getMouse()
            (x, y) = self.getMousePixelCoordinates(mouse)

            if up:
                self.browser.SendMouseWheelEvent(x, y, 0, 120)
            else:
                self.browser.SendMouseWheelEvent(x, y, 0, -120)

    def updateMouseTask(self, task):
        if base.mouseWatcherNode.hasMouse():
            mouse = base.mouseWatcherNode.getMouse()
            (x, y) = self.getMousePixelCoordinates(mouse)

            if x != self.lastX or y != self.lastY:
                self.browser.SendMouseMoveEvent(x, y, False)

                self.lastX = x
                self.lastY = y

        return task.cont


    def installMouseHandlers(self):
        self.accept("mouse1", self.mouseEvent, [1, False])
        self.accept("mouse2", self.mouseEvent, [2, False])
        self.accept("mouse3", self.mouseEvent, [3, False])

        self.accept("mouse1-up", self.mouseEvent, [1, True])
        self.accept("mouse2-up", self.mouseEvent, [2, True])
        self.accept("mouse3-up", self.mouseEvent, [3, True])

        self.accept("wheel_up", self.mouseWheelEvent, [True])
        self.accept("wheel_down", self.mouseWheelEvent, [False])

        taskMgr.add(self.updateMouseTask, 'ChromiumMouseUpdateTask')


    def initKeyboardHandlers(self):
        base.buttonThrowers[0].node().setKeystrokeEvent('keystroke')
        base.buttonThrowers[0].node().setButtonDownEvent('button-down')
        base.buttonThrowers[0].node().setButtonUpEvent('button-up')
        base.buttonThrowers[0].node().setButtonRepeatEvent('button-repeat')

        self.accept("keystroke", self.onKeystroke)
        self.accept("button-down", self.onButtonDown)
        self.accept("button-up", self.onButtonUp)
        self.accept("button-repeat", self.onButtonDown)

        self.keyModifiers = 0

    def keyInfo(self, key):
        if self.translateKeys.has_key(key):
            return self.translateKeys[key]
        else:
            return ord(key)

    def onKeystroke(self, key):
        event = {
            "type": cefpython.KEYEVENT_CHAR,
            "modifiers": self.keyModifiers,
            "windows_key_code": self.keyInfo(key),
            "native_key_code": self.keyInfo(key),
        }

        self.browser.SendKeyEvent(event)

    def onButtonDownOrUp(self, keyType, key):
        if self.modifierKeys.has_key(key):
            self.keyModifiers |= self.modifierKeys[key]
        else:
            if self.translateKeys.has_key(key):
                event = {
                    "type": keyType,
                    "modifiers": self.keyModifiers,
                    "windows_key_code": self.keyInfo(key),
                    "native_key_code": self.keyInfo(key),
                }

                self.browser.SendKeyEvent(event)

    def onButtonDown(self, key):
        self.onButtonDownOrUp(cefpython.KEYEVENT_KEYDOWN, key)

    def onButtonUp(self, key):
        self.onButtonDownOrUp(cefpython.KEYEVENT_KEYUP, key)

    def installEventHandlers(self):
        self.installMouseHandlers()
        self.initKeyboardHandlers()

    def removeEventHandlers(self):
        self.ignoreAll()