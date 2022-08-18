import os.path
import re
import time

from django.conf import settings
from django.db.models import Q
from django.http.response import HttpResponse
from django.middleware.csrf import get_token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .authentication import isLoginJWTAuthentication, customerTokenAuthentication
from .base64Tobyte import base64ToImage
from .customersOperation import customersOp
from .message import message
from .models import Customers, Class
from .pagination import customersPagination
from .resources import customersResources, customersMTResources
from .serializer import (customerSerializer, classSerializer, mdResSerializer, customerTokenObtainSerializer)


class customerApiViewSet(ModelViewSet):
    """
    用户视图集合，包含查询所有，查询单个用户，创建用户，删除用户，更改用户
    需要admin用户登录才能使用以上功能
    """
    serializer_class = customerSerializer
    queryset = Customers.objects.filter(is_valided=1).order_by("id")
    pagination_class = customersPagination
    authentication_classes = [isLoginJWTAuthentication]

    def list(self, request, *args, **kwargs):
        if "ex_is_valided" in request.GET:
            ex_is_valided = request.GET.get("ex_is_valided")
            self.queryset = Customers.objects.exclude(is_valided=ex_is_valided).order_by("id")
        return super().list(request)

    def create(self, request, *args, **kwargs):
        try:
            self.get_queryset().get(customer_id=request.data.get('customer_id'))
            return Response(message('failed', 403, message="customer is existed"))
        except Exception as e:
            serializer = customerSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    message('failed', 400, message="customer failed to create!", kwargs={"info": serializer.errors}))
            serializer.save()
            serializer = customerSerializer(self.get_queryset().get(
                customer_id=request.data.get('customer_id')))
            return Response(
                message('success', 200, message="create a new customers", kwargs={"info": serializer.data}))

    def retrieve(self, request, param, *args, **kwargs):
        try:
            if "ex_is_valided" in request.GET:
                ex_is_valided = request.GET.get("ex_is_valided")
                self.queryset = Customers.objects.all().exclude(is_valided=ex_is_valided).filter(
                    Q(customer_id__icontains=param) | Q(
                        customer_name__icontains=param) | Q(parent_phone__icontains=param))
            else:
                self.queryset = self.get_queryset().filter(Q(customer_id__icontains=param) | Q(
                    customer_name__icontains=param) | Q(parent_phone__icontains=param))
        except Exception as e:
            return Response(message('failed', 404, e.args[0]), status=200)
        return super(customerApiViewSet, self).list(request)

    def update(self, request, *args, **kwargs):
        if "customer_id" not in request.GET:
            return Response(message(status="failed", code=404, message="身份证号码是必须的!"))
        customer_id = request.GET.get("customer_id")
        request.data.update({"is_valided": 1})
        newData = request.data
        try:
            customer = self.get_queryset().get(customer_id=customer_id)
        except Exception as e:
            return Response(message('failed', 404, e.args[0]), status=200)
        if customer is not None:
            serializer = customerSerializer(customer, newData)
            if not serializer.is_valid():
                return Response(message(status='failed', code=403, message=serializer.errors), status=200)
            serializer.save()
            return Response(
                message("success", code=200, message="customer update successfully ", kwargs={"info": serializer.data}))

    def destroy(self, request, *args, **kwargs):
        id = request.query_params.get('id')
        try:
            customer = self.get_queryset().get(pk=id)
        except Exception as e:
            return Response(message(status='failed', code=404, message=e.args[0]), status=200)
        content = {"customer_id": customer.customer_id,
                   "customer_name": customer.customer_name,
                   "customer_photo": customer.customer_photo}
        try:
            customer.delete()
            customersOp(content.get("customer_photo")).remove()
            return Response(
                message(message="customer already delete", kwargs={"info": content}), status=200)
        except Exception as e:
            return Response(
                message(status='failed', code=403, message=e.args[0], kwargs={"info": content}), status=200)

    def updateAll(self, request):
        if "status" not in request.GET:
            return Response(message("failed", code=403, message="status字段是必须的!"))
        status = request.GET.get("status")
        dataList = request.data.get("idList")
        messageList = list()
        try:
            if dataList:
                for data in dataList:
                    customer = Customers.objects.get(pk=data)
                    customer.is_valided = status
                    customer.save()
                    newMessage = message(
                        status="success", code=200, message="OK")
                    messageList.append(newMessage)
            return Response(message(status="success", code=200, message="Ok", kwargs={"results": messageList}),
                            status=200)
        except Exception as e:
            return Response(message(status="failed", code=400, message=e.args[0], kwargs={"info": messageList}),
                            status=200)


class customerGeneralApi(ModelViewSet):
    """
    开放给提交用户的api接口不用验证token
    """
    queryset = Customers.objects.all().order_by("id")
    serializer_class = customerSerializer

    def retrieve(self, request, *args, **kwargs):
        if len(request.GET) == 0:
            get_token(request)
            return Response(message(status="success", code=200, message="OK"))
        else:
            customer_id = request.GET.get('customer_id')
            try:
                customer = Customers.objects.get(customer_id=customer_id)
            except Exception as e:
                return Response(message(status="failed", code=404, message="don't exist"))
            customer = customerSerializer(customer).data
            print(customer)
            return Response(message(status="success", code=200, message="exist", kwargs={"info": customer}))

    def create(self, request, *args, **kwargs):
        try:
            self.get_queryset().get(customer_id=request.data.get('customer_id'))
            # return Response(message('failed', 403, message="customer is existed"))
            return self.update(request, *args, **kwargs)
        except Exception as e:
            # 为用户添加未验证字段
            request.data.update({"is_valided": 0})
            serializer = customerSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    message('failed', 400, message="customer failed to create!", kwargs={"info": serializer.errors}))
            serializer.save()
            serializer = customerSerializer(self.get_queryset().get(
                customer_id=request.data.get('customer_id')))
            return Response(
                message('success', 200, message="create a new customers", kwargs={"info": serializer.data}))

    def update(self, request, *args, **kwargs):
        try:
            customer = self.get_queryset().get(customer_id=request.data.get('customer_id'))
        except Exception as e:
            return Response(message('failed', 404, e.args[0]), status=200)
        if customer is not None:
            request.data.update({"is_valided": customer.is_valided})
            serializer = customerSerializer(customer, request.data)
            if not serializer.is_valid():
                return Response(message(status='failed', code=403, message=serializer.errors), status=200)
            serializer.save()
            return Response(
                message("success", code=200, message="customer update successfully ", kwargs={"info": serializer.data}))


class classViewSet(ModelViewSet):
    """
    班级内容api
    """
    queryset = Class.objects.all().order_by("id")
    serializer_class = classSerializer
    authentication_classes = [isLoginJWTAuthentication]

    def list(self, request, *args, **kwargs):
        return super().list(request)

    def create(self, request, *args, **kwargs):
        classInfo = request.data
        try:
            self.get_queryset().get(class_name=classInfo.get('class_name'))
            return Response(message("failed", 403, "class is exist"))
        except Exception as e:
            classSer = classSerializer(data=classInfo)
            if not classSer.is_valid():
                return Response(message("failed", "403", "failed to add Class", kwargs={"info": classSer.errors}))
            classSer.save()
            return Response(message("success", 200, "create class successfully"))

    def destroy(self, request, *args, **kwargs):
        if "idList" not in request.data:
            return Response("failed", 404, "idList param is necessary")
        idList = request.data.get("idList")
        try:
            if idList:
                for id in idList:
                    classInfo = self.get_queryset().get(pk=id)
                    classInfo.delete()
                return Response(message("success", 200, "classes is already deleted"))
            return Response(message("failed", 404, "idList 列表为空"))
        except Exception as e:
            return Response(message("failed", 404, "class is not exist"))


class classGeneralApi(APIView):
    """
    为普通用户开放的班级接口，不需要验证
    """

    def get(self, request):
        return Response(classSerializer(Class.objects.all(), many=True).data)


class uploadAvatar(APIView):
    def post(self, request):
        if "avatarSize" in request.data and request.data.get("avatarSize") != 0:
            base64ToImage(request.data.get("avatar"),
                          request.data.get("avatarName"), 'png').toImage()
            return Response(message("success", 200, message="Ok"))
        return Response(message("failed", 404, message="上传头像失败"))


class uploadMdRes(APIView):
    authentication_classes = [isLoginJWTAuthentication]

    def post(self, request):
        if not "file" in request.data:
            return Response(message("failed", 400, "file 参数是必须的"))
        IMAGE_TYPE = ("png", "jpg", "jpeg")
        VIDEO_TYPE = ("mp4",)
        file = request.data.get("file")
        if file.get("fileType") in IMAGE_TYPE:
            mdImagePath = base64ToImage(file.get("body"), str(int(time.time())), file.get("fileType")).toMdImage()
            res = mdResSerializer(data={"res_name": mdImagePath})
            if not res.is_valid():
                return Response(message("failed", 400, res.errors))
            res.save()
            return Response(message("success", 200, "图片上传成功!", kwargs={"info": mdImagePath}))
        elif file.get("fileType") in VIDEO_TYPE:
            mdVideoPath = base64ToImage(file.get("body"), str(int(time.time())), file.get("fileType")).toMdVideo()
            res = mdResSerializer(data={"res_name": mdVideoPath})
            if not res.is_valid():
                return Response(message("failed", 400, res.errors))
            res.save()
            return Response(message("success", 200, "视频上传成功!", kwargs={"info": mdVideoPath}))
        return Response(message("failed", 403, "文件类型不允许上传"))


class saveMd(APIView):
    authentication_classes = [isLoginJWTAuthentication]

    def get(self, request):
        mdType = 1
        if request.GET.__contains__("type"):
            mdType = request.GET.get("type")
        try:
            info = base64ToImage("1", "1", "1").readMd(int(mdType))
            return Response(message("success", 200, "请求成功", kwargs={"info": info}))
        except ValueError as ve:
            return Response(message("failed", 403, "参数不合法", kwargs={"info": ve.args[0]}))

    def post(self, request):
        if not request.data.__contains__("file") or not request.data.__contains__("type"):
            return Response(message("failed", 400, "file 参数和type 参数是必须的"))
        try:
            file = request.data.get("file")
            mdType = request.data.get("type")
            if int(mdType) == 1:
                base64ToImage(file.get("body"), "ad", "md").saveMd(mdType)
            elif int(mdType) == 2:
                base64ToImage(file.get("body"), "recharge", "md").saveMd(mdType)
            return Response(message("success", 200, "文件保存成功!"))
        except ValueError as ve:
            return Response(message("failed", 403, "参数不合法", kwargs={"info": ve.args[0]}))


class mdGeneralApi(APIView):
    def get(self, request):
        mdType = 1
        if request.GET.__contains__("type"):
            mdType = request.GET.get("type")
        try:
            info = base64ToImage("1", "1", "1").readMd(int(mdType))
            return Response(message("success", 200, "请求成功", kwargs={"info": info}))
        except ValueError as ve:
            return Response(message("failed", 403, "参数不合法", kwargs={"info": ve.args[0]}))


class exportResources(APIView):
    """
    导出模版数据1
    """
    authentication_classes = [isLoginJWTAuthentication]

    def get(self, request):
        if ("page" or "pageSize") not in request.GET:
            return Response(message("failed", 404, "请求参数不全，请检查"))
        try:
            page = int(request.GET.get("page"))
            pageSize = int(request.GET.get("pageSize"))
            querySet = Customers.objects.filter(is_valided=1)[(page - 1) * pageSize:page * pageSize]
            customersData = customersResources().export(queryset=querySet)
            response = HttpResponse(customersData.xlsx,
                                    content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response["Content-Disposition"] = "attachment;filename=\"customers({}).xls\"".format(page)
            return response
        except Exception as e:
            return Response(message("failed", 403, "参数不合法", kwargs={"info": e.args[0]}))

    def post(self, request):
        data = customersResources().export()
        response = HttpResponse(data.xlsx,
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = "attachment;filename=\"customers.xlsx\""
        return response


class exportMTResources(APIView):
    """
    导出模版数据2
    """
    authentication_classes = [isLoginJWTAuthentication]

    def get(self, request):
        if ("page" or "pageSize") not in request.GET:
            return Response(message("failed", 404, "请求参数不全，请检查"))
        try:
            page = int(request.GET.get("page"))
            pageSize = int(request.GET.get("pageSize"))
            querySet = Customers.objects.filter(is_valided=1)[(page - 1) * pageSize:page * pageSize]
            customersData = customersMTResources().export(queryset=querySet)
            response = HttpResponse(customersData.xlsx,
                                    content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response["Content-Disposition"] = "attachment;filename=\"customers({}).xls\"".format(page)
            return response
        except Exception as e:
            return Response(message("failed", 403, "参数不合法", kwargs={"info": e.args[0]}))

    def post(self, request):
        customersMTData = customersMTResources().export()
        response = HttpResponse(customersMTData.xlsx,
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = "attachment;filename=\"customers.xlsx\""
        return response


class exportAvatarRes(APIView):
    authentication_classes = [isLoginJWTAuthentication]
    customersList = Customers.objects.filter(is_valided=1)

    def get(self, request):
        tempPath, length = customersOp("").readAvatarZip([c.customer_photo for c in self.customersList])
        return Response(message("success", 200, "请求成功", kwargs={"info": length}))

    def post(self, request):
        if not request.headers.__contains__("range"):
            return Response(400, message("failed", 400, "参数不合法", kwargs={"info": "range头缺失"}))
        try:
            rangeB = request.headers.get("range")
            starts = re.findall(r"\d+", rangeB)
            start, end = map(lambda x: int(x), starts)
            # if end > self.length:
            #    raise ValueError("切片范围不合法")
            with open(os.path.join(settings.STATICFILES_DIRS[0], "avatar/avatar.zip"), "rb") as f:
                f.seek(start)
                sliceF = f.read(end - start + 1)
            resp = HttpResponse(sliceF)
            resp['content-type'] = 'application/octet-stream'
            resp['Content-Range'] = "bytes {0}-{1}/*".format(start, end)
            resp['accept-Ranges'] = "bytes"
            return resp
        except ValueError as ve:
            return Response(416, message("failed", 416, "参数不合法", kwargs={"info": ve.args[0]}))
        except Exception as e:
            return Response(400, message("failed", 400, "参数不合法", kwargs={"info": e.args[0]}))


class customerTokenObtainView(TokenObtainPairView):
    serializer_class = customerTokenObtainSerializer
    authentication_classes = [customerTokenAuthentication]
