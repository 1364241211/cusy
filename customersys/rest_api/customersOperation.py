import os
import zipfile

from django.conf import settings


class customersOp():
    def __init__(self, customers_photo):
        self.staticPath = os.path.join(settings.STATICFILES_DIRS[0], "avatar")
        self.resPath = os.path.join(self.staticPath, customers_photo)

    def remove(self):
        os.remove(self.resPath)

    def readAvatarZip(self, filters=None):
        tempPath = os.path.join(self.staticPath, "avatar.zip")
        # avatarImages = os.listdir(self.staticPath)
        if os.path.exists(tempPath):
            os.remove(tempPath)
        if filters:
            with zipfile.ZipFile(tempPath, "a", zipfile.ZIP_DEFLATED) as zipFile:
                print(tempPath)
                for avatar in filters:
                    temp = str(os.path.join(self.staticPath, avatar))
                    try:
                        zipFile.write(temp, arcname="avatar")
                    except FileNotFoundError:
                        continue
        fileSize = os.path.getsize(tempPath)
        return tempPath, fileSize
