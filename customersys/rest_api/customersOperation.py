import os
import zipfile
from concurrent.futures import CancelledError
from threading import Lock

from django.conf import settings
from django.utils.timezone import now

from .models import ZipfilesInfo
from .thread import futureInfo, singleEnum


class customersOp():
    def __init__(self, customers_photo):
        self.staticPath = os.path.join(settings.STATICFILES_DIRS[0], "avatar")
        self.zipFilePath = os.path.join(settings.STATICFILES_DIRS[0], "zipFile")
        self.resPath = os.path.join(self.staticPath, customers_photo)
        self.sync_lock = Lock()

    def remove(self):
        os.remove(self.resPath)

    def readAvatarZip(self, zipFileName: str, filters: list = None, ):
        tempName = zipFileName
        tempZipPath = os.path.join(self.zipFilePath, "{0}.zip".format(tempName))
        future: futureInfo = settings.GLOBAL_THREAD_POOL.future_dict.get(zipFileName)
        zipInfoList = ZipfilesInfo.objects.all()
        newZipInfo = ZipfilesInfo()
        if zipInfoList.count() == 3:
            minZipInfo = ZipfilesInfo()
            minTime = min([t.last_modified_time for t in zipInfoList])
            for i, v in enumerate(zipInfoList):
                if v.last_modified_time == minTime:
                    minZipInfo: ZipfilesInfo = zipInfoList[i]
                    break
            newZipInfo = minZipInfo
            if newZipInfo.download == 0:
                tempFuture: futureInfo = settings.GLOBAL_THREAD_POOL.future_dict.get(
                    os.path.splitext(newZipInfo.zip_name)[0])
                tempFuture.single = singleEnum.SHUTDOWN
            with self.sync_lock:
                tempRemoveFilePath = os.path.join(self.zipFilePath, newZipInfo.zip_name)
                if os.path.exists(tempRemoveFilePath):
                    os.remove(tempRemoveFilePath)
        newZipInfo.zip_name = "{0}.zip".format(tempName)
        newZipInfo.zip_size = 0
        newZipInfo.last_modified_time = now()
        newZipInfo.download = 0
        newZipInfo.save()
        if filters:
            with zipfile.ZipFile(tempZipPath, "w", zipfile.ZIP_DEFLATED) as zipFile:
                for avatar in filters:
                    temp = str(os.path.join(self.staticPath, avatar))
                    fileSize = os.path.getsize(tempZipPath)
                    newZipInfo.zip_size = fileSize
                    try:
                        zipFile.write(temp, arcname=avatar)
                        newZipInfo.save()
                        if future.single == singleEnum.SHUTDOWN:
                            raise CancelledError("线程已终止")
                    except FileNotFoundError:
                        continue
                    except CancelledError:
                        with self.sync_lock:
                            if os.path.exists(tempZipPath):
                                os.remove(tempZipPath)
                                newZipInfo.download = 0
                                newZipInfo.save()
                        break

        # zipInfoList = ZipfilesInfo.objects.all()
        # newZipInfo = ZipfilesInfo()
        # if zipInfoList.count() == 3:
        #     minZipInfo = ZipfilesInfo()
        #     minTime = min([t.last_modified_time for t in zipInfoList])
        #     for i, v in enumerate(zipInfoList):
        #         if v.last_modified_time == minTime:
        #             minZipInfo: ZipfilesInfo = zipInfoList[i]
        #             break
        #     newZipInfo = minZipInfo
        #     if newZipInfo.download == 0:
        #         tempFuture: futureInfo = settings.GLOBAL_THREAD_POOL.future_dict.get(
        #             os.path.splitext(newZipInfo.zip_name)[0])
        #         tempFuture.single = singleEnum.SHUTDOWN
        #     with self.sync_lock:
        #         tempRemoveFilePath = os.path.join(self.zipFilePath, newZipInfo.zip_name)
        #         if os.path.exists(tempRemoveFilePath):
        #             os.remove(tempRemoveFilePath)
        # newZipInfo.zip_name = "{0}.zip".format(tempName)
        # newZipInfo.zip_size = 0
        # newZipInfo.last_modified_time = now()
        # newZipInfo.download = 0
        # newZipInfo.save()
        # a = os.listdir(self.staticPath)
        # with zipfile.ZipFile(tempZipPath, "w", zipfile.ZIP_DEFLATED) as zipFile:
        #     for at in a:
        #         temp = str(os.path.join(self.staticPath, at))
        #         fileSize = os.path.getsize(tempZipPath)
        #         newZipInfo.zip_size = fileSize
        #         try:
        #             zipFile.write(temp, arcname=at)
        #             newZipInfo.save()
        #             if future.single == singleEnum.SHUTDOWN:
        #                 raise CancelledError("线程已终止")
        #         except FileNotFoundError:
        #             continue
        #         except CancelledError:
        #             with self.sync_lock:
        #                 if os.path.exists(tempZipPath):
        #                     os.remove(tempZipPath)
        #                     newZipInfo.download = 0
        #                     newZipInfo.save()
        #             break
        newZipInfo.download = 1
        newZipInfo.save()
        return tempZipPath, fileSize
