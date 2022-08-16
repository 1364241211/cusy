import base64
import os.path

from django.conf import settings


class base64ToImage:
    def __init__(self, base64str: str, avatarName: str, fileType: str):
        self.base64str = base64str,
        self.avatarName = avatarName
        self.fileType = fileType

    def toImage(self):
        byteImage = base64.b64decode(str(self.base64str))
        with open(os.path.join(settings.STATICFILES_DIRS[0], "avatar/{}".format(self.avatarName)), "wb") as f:
            f.write(byteImage)

    def toMdImage(self):
        byteImage = base64.b64decode(str(self.base64str))
        with open(os.path.join(settings.STATICFILES_DIRS[0], "md/image/{}.{}".format(self.avatarName, self.fileType)),
                  "wb") as f:
            f.write(byteImage)
        mdImagePath = "/md/image/{}.{}".format(self.avatarName, self.fileType)
        return mdImagePath

    def toMdVideo(self):
        byteImage = base64.b64decode(str(self.base64str))
        with open(os.path.join(settings.STATICFILES_DIRS[0], "md/video/{}.{}".format(self.avatarName, self.fileType)),
                  "wb") as f:
            f.write(byteImage)
        mdVideoPath = "/md/video/{}.{}".format(self.avatarName, self.fileType)
        return mdVideoPath

    def saveMd(self, mdType):
        # byteContent = bytes(self.base64str[0], encoding="ascii")
        # content = byteContent.decode('unicode-escape')
        content = self.base64str[0]
        if mdType == 1:
            with open(os.path.join(settings.STATICFILES_DIRS[0], "md/{}.{}".format(self.avatarName, self.fileType)),
                      "w") as f:
                f.write(str(content))
        elif mdType == 2:
            with open(os.path.join(settings.STATICFILES_DIRS[0], "md/{}.{}".format(self.avatarName, self.fileType)),
                      "w") as f:
                f.write(str(content))

    def readMd(self, mdType: int = 1):
        if mdType == 1:
            with open(os.path.join(settings.STATICFILES_DIRS[0], "md/ad.md"), "r") as f:
                content = f.read()
        elif mdType == 2:
            with open(os.path.join(settings.STATICFILES_DIRS[0], "md/recharge.md"), "r") as f:
                content = f.read()
        return content
