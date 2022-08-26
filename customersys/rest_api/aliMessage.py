# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from typing import List

from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
from django.conf import settings

global_access_key_id = settings.ACCESS_KEY_ID
global_access_key_secret = settings.ACCESS_KEY_SECRET
global_template_code = settings.TEMPLATE_CODE


class aliMessage:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
            access_key_id: str,
            access_key_secret: str,
    ) -> Dysmsapi20170525Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 您的 AccessKey ID,
            access_key_id=access_key_id,
            # 您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = f'dysmsapi.aliyuncs.com'
        return Dysmsapi20170525Client(config)

    @staticmethod
    def main(
            phoneNumberJson: List[str],
            signNameJson: List[str],
    ) -> None:
        client = aliMessage.create_client(global_access_key_id, global_access_key_secret)
        send_batch_sms_request = dysmsapi_20170525_models.SendBatchSmsRequest(
            template_code=global_template_code,
            phone_number_json=str(phoneNumberJson),
            sign_name_json=str(signNameJson)
        )
        runtime = util_models.RuntimeOptions()
        # try:
        # 复制代码运行请自行打印 API 的返回值
        client.send_batch_sms_with_options(send_batch_sms_request, runtime)
        # except Exception as error:
        # 如有需要，请打印 error
        # UtilClient.assert_as_string(error.message)

    @staticmethod
    async def main_async(
            args: List[str],
    ) -> None:
        client = aliMessage.create_client(global_access_key_id, global_access_key_secret)
        send_batch_sms_request = dysmsapi_20170525_models.SendBatchSmsRequest()
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            await client.send_batch_sms_with_options_async(send_batch_sms_request, runtime)
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)
