from django.db.models import Q
from django.middleware.csrf import get_token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .authentication import isLoginJWTAuthentication, customerTokenAuthentication
from .base64Tobyte import base64ToImage
from .message import message
from .models import Customers, Class
from .pagination import customersPagination
from .serializer import customerSerializer, customerTokenObtainSerializer, classSerializer


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
        try:
            content = {"customer_id": customer.customer_id,
                       "customer_name": customer.customer_name}
            customer.delete()
            return Response(
                message(message="customer already delete", kwargs={"info": content}), status=200)
        except Exception as e:
            content = {"customer_id": customer.customer_id,
                       "customer_name": customer.customer_name}
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
    queryset = Class.objects.all()
    serializer_class = classSerializer
    authentication_classes = [isLoginJWTAuthentication]

    def list(self, request, *args, **kwargs):
        return super().list(request)

    def create(self, request, *args, **kwargs):
        classInfo = request.data
        pass

    def destroy(self, request, *args, **kwargs):
        pass


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
                          request.data.get("avatarName")).toImage()
            return Response(message("success", 200, message="Ok"))
        return Response(message("failed", 404, message="上传头像失败"))


class customerTokenObtainView(TokenObtainPairView):
    serializer_class = customerTokenObtainSerializer
    authentication_classes = [customerTokenAuthentication]
