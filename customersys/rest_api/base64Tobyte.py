import base64
import os.path

from django.conf import settings


class base64ToImage:
    def __init__(self, base64str: str, avatarName: str):
        self.base64str = base64str,
        self.avatarName = avatarName

    def toImage(self):
        byteImage = base64.b64decode(str(self.base64str))
        with open(os.path.join(settings.STATICFILES_DIRS[0], "avatar/{}".format(self.avatarName)), "wb") as f:
            f.write(byteImage)
