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
        tempZipPath = os.path.join(self.staticPath, "avatar1.zip")
        # avatarImages = os.listdir(self.staticPath)
        if os.path.exists(tempZipPath):
            os.remove(tempZipPath)
        # if filters:
        #     with zipfile.ZipFile(tempZipPath, "w", zipfile.ZIP_DEFLATED) as zipFile:
        #         for avatar in filters:
        #             temp = str(os.path.join(self.staticPath, avatar))
        #             try:
        #                 zipFile.write(temp, arcname=avatar)
        #             except FileNotFoundError:
        #                 continue
        with zipfile.ZipFile(tempZipPath, "w", zipfile.ZIP_DEFLATED) as zipFile:
            temp = os.listdir(self.staticPath)
            for te in temp:
                try:
                    p = os.path.join(self.staticPath, te)
                    zipFile.write(p, arcname=te)
                except FileNotFoundError:
                    continue
        fileSize = os.path.getsize(tempZipPath)
        return tempZipPath, fileSize
