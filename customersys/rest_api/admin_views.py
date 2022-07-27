from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .captchaImage import captchaImage
from .authentication import isLoginJWTAuthentication, LoginAuthentication
from .serializer import (adminSerializer,
                         adminTokenObtainSerializer
                         )
from .models import (Customers,
                     Admin)
from .message import message


class adminApiViewSet(ModelViewSet):
    """
    admin用户视图集，用于注册登录
    """
    serializer_class = adminSerializer
    queryset = Customers.objects.all()

    # 注册
    def create(self, request, *args, **kwargs):
        if len(request.data) != 0:
            serializer = adminSerializer(data=request.data)
            if serializer.is_valid(True):
                try:
                    serializer.save()
                    return Response(
                        message('success', 201, "create admin successfully", kwargs={"info": serializer.data}),
                        status=201)
                except Exception as e:
                    return Response(message('failed', 403, "fail to create admin", kwargs={"info": e.args[0]}))
        return Response(message('failed', 404, 'failed to create admin', kwargs={"admin_info": request.data}))


class adminCaptchaImage(ModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        image_value, image = captchaImage().get_randomImage()
        request.session['code'] = image_value
        return Response(message('success', 200, "OK", kwargs={"image": image}))


class adminTokenObtainView(TokenObtainPairView):
    """
    admin 用户登录验证视图
    """
    serializer_class = adminTokenObtainSerializer
    authentication_classes = [LoginAuthentication]
