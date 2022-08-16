from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from .models import Admin


class isLoginJWTAuthentication(JWTAuthentication):
    """
    验证用户是否登录
    """

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            raise AuthenticationFailed("token 无效", code=404)

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return AuthenticationFailed("token 为空", code=404)

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token


class LoginAuthentication(JWTAuthentication):
    """
    用户登录验证，验证传输到密码正确则添加token
    """

    def authenticate(self, request):
        data = request.data
        print(request.session['code'])
        if data.get('code') != request.session['code']:
            raise AuthenticationFailed("验证码错误请重新输入", code="403")
        if data is None:
            raise AuthenticationFailed("验证出错！请检查信息", code="404")
        try:
            admin = Admin.objects.get(admin_account=data.get("admin_account"))
        except Exception as e:
            raise AuthenticationFailed("账号{0}不存在".format(data.get('admin_account')), code=403)
        if admin.check_password(data.get("password")):
            return admin, None
        else:
            raise AuthenticationFailed("密码错误！", code=404)


class customerTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        return None
