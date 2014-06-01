import urlparse
from cefpython3 import cefpython
from panda3dext.cef.VFSResourceHandler import VFSResourceHandler

from panda3d.core import VirtualFileSystem

__author__ = 'Marius'

from panda3d.core import PStatCollector

class ClientHandler:
    """A client handler is required for the browser to do built in callbacks back into the application."""

    def __init__(self, browser, texture):
        self.browser = browser
        self.texture = texture
        self.vfs = VirtualFileSystem.getGlobalPtr()

    def OnPaint(self, browser, paintElementType, dirtyRects, buffer, width, height):
        img = self.texture.modifyRamImage()
        if paintElementType == cefpython.PET_POPUP:
            print("width=%s, height=%s" % (width, height))
        elif paintElementType == cefpython.PET_VIEW:
            img.setData(buffer.GetString(mode="bgra", origin="bottom-left"))
        else:
            raise Exception("Unknown paintElementType: %s" % paintElementType)


    def GetViewRect(self, browser, rect):
        width = self.texture.getXSize()
        height = self.texture.getYSize()
        rect.append(0)
        rect.append(0)
        rect.append(width)
        rect.append(height)
        return True

    def OnBeforePopup(self):
        return True  # Always disallow popups

    def GetResourceHandler(self, browser, frame, request):
        url = request.GetUrl()
        parts = urlparse.urlparse(url)

        if parts.netloc.upper() == "VFS":
            vfsHandler = VFSResourceHandler(self)
            self._AddStrongReference(vfsHandler)

            return vfsHandler

        return None

    # A strong reference to ResourceHandler must be kept
    # during the request. Some helper functions for that.
    # 1. Add reference in GetResourceHandler()
    # 2. Release reference in ResourceHandler.ReadResponse()
    #    after request is completed.

    _resourceHandlers = {}
    _resourceHandlerMaxId = 0

    def _AddStrongReference(self, resHandler):
        self._resourceHandlerMaxId += 1
        resHandler._resourceHandlerId = self._resourceHandlerMaxId
        self._resourceHandlers[resHandler._resourceHandlerId] = resHandler

    def _ReleaseStrongReference(self, resHandler):
        if resHandler._resourceHandlerId in self._resourceHandlers:
            del self._resourceHandlers[resHandler._resourceHandlerId]
        else:
            print("_ReleaseStrongReference() FAILED: resource handler "
                  "not found, id = %s" % resHandler._resourceHandlerId)