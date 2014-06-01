import mimetypes
import urllib
import urlparse

__author__ = 'asarium'

from cefpython3 import cefpython

from panda3d.core import VirtualFile, VirtualFileSystem

mimetypes.add_type("application/font-woff", ".woff")


def getMimeType(url):
    parts = urlparse.urlparse(url)
    mimeType = mimetypes.guess_type(parts.path, strict=False)

    if mimeType[0] is not None:
        return mimeType[0]
    else:
        return "application/octet-stream"


class VFSResourceHandler():
    def __init__(self, clientHandler):
        self.clientHandler = clientHandler

        self.contents = None
        self.filePath = None
        self.url = None
        self.clientHandler = None
        self.offset = 0

    def ProcessRequest(self, request, callback):
        """


        :type callback: cefpython.PyCallback
        :type request: cefpython.PyRequest
        """

        self.url = request.GetUrl()
        parts = urlparse.urlparse(self.url)

        self.filePath = urllib.unquote_plus(parts.path[1:])

        # We are done immediately
        callback.Continue()

        return True

    def GetResponseHeaders(self, response, responseLengthOut, redirectUrlOut):
        """

        :type response: cefpython.PyResponse
        """
        response.SetMimeType(getMimeType(self.url))

        file = VirtualFileSystem.getGlobalPtr().getFile(self.filePath)

        if file is None:
            response.SetStatus(404)
            response.SetStatusText("File not found")

            return

        responseLengthOut[0] = file.getFileSize()

    def ReadResponse(self, dataOut, bytesToRead, bytesReadOut, callback):
        if self.contents is None:
            self.contents = VirtualFileSystem.getGlobalPtr().readFile(self.filePath, False)

        if self.offset < len(self.contents):
            dataOut[0] = self.contents[self.offset:self.offset + bytesToRead]
            bytesReadOut[0] = bytesToRead

            self.offset += bytesToRead

            return True

        # We are done
        self.clientHandler._ReleaseStrongReference(self)
        return False

    def Cancel(self):
        pass

    def CanGetCookie(self, cookie):
        # Return true if the specified cookie can be sent
        # with the request or false otherwise. If false
        # is returned for any cookie then no cookies will
        # be sent with the request.
        return True

    def CanSetCookie(self, cookie):
        # Return true if the specified cookie returned
        # with the response can be set or false otherwise.
        return True
