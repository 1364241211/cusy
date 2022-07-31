from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView
)

from .admin_views import (adminApiViewSet,
                          adminTokenObtainView,
                          adminCaptchaImage)
from .customer_view import (customerGeneralApi,
                            customerTokenObtainView,
                            customerApiViewSet,
                            uploadAvatar,
                            uploadMdRes,
                            mdGeneralApi,
                            saveMd,
                            classGeneralApi,
                            classViewSet)

customer_general_api = customerGeneralApi.as_view({
    'get': 'retrieve',
    'post': 'create'
})
customer_detail = customerApiViewSet.as_view({'get': 'retrieve'})
customers = customerApiViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'update',
    'delete': 'destroy'
})
validate_Customer = customerApiViewSet.as_view({'post': 'updateAll'})
customerToken_detail = customerTokenObtainView.as_view()
admin_register = adminApiViewSet.as_view({
    'post': 'create'
})
admin_captcha = adminCaptchaImage.as_view({'get': 'retrieve'})
classes = classViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'delete': 'destroy'
})
app_name = 'rest_api'
urlpatterns = [
    path('customerGeneralApi', customer_general_api, name='customerApi'),
    path('classGeneralApi', classGeneralApi.as_view()),
    path('classes', classes, name='classes'),
    path('uploadAvatar', uploadAvatar.as_view(), name='avatar'),
    path('uploadMdRes', uploadMdRes.as_view(), name='res'),
    path('uploadMd', saveMd.as_view(), name="md"),
    path('mdGeneralApi', mdGeneralApi.as_view()),
    path('validateCustomers', validate_Customer),
    path('customer/<str:param>', customer_detail, name='customer-detail'),
    path('customers', customers, name='customers'),
    path('admin/register', admin_register, name='customer-register'),
    path('login', adminTokenObtainView.as_view(), name='login'),
    path('captcha', admin_captcha, name='captcha'),
    path('token/refresh', TokenRefreshView.as_view(), name='refresh-token'),
    path('customerToken', customerToken_detail, name='customer-token')
]
