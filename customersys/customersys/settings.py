"""
Django settings for customersys project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import datetime
import os.path
from pathlib import Path

from rest_api.thread import threadPool

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ea7gumtp=b533h6-)x*hgc2rdiy0x!9^c73cw^yka3$q+v!^by'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_api',
    # 导入导出App
    'import_export'
]
APPEND_SLASH = False
REST_FRAMEWORK = {
    # 修改时间格式
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",
    # 配置session_id 认证
    'DEFAULT_AUTHENTICATION_CLASS': (
        # drf 这一阶段主要验证， middleware的auth主要设置session_id和user到request中
        # 默认验证是按照列表从上到下
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}
SIMPLE_JWT = {
    # token存活时间为 1 天
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=1),
    # 修改jwt到验证id为admin_id, 默认为id
    'USER_ID_FIELD': 'admin_id',
    'USER_ID_CLAIM': 'admin_id',
    # 设置每次请求token 更新last login Time
    'UPDATE_LAST_LOGIN': True,
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),

}
# 创建应用程序到验证模型为admin
AUTH_USER_MODEL = 'rest_api.Admin'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 跨域请求中间件
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'customersys.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'customersys.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = False
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'statics')
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# 跨域允许的请求方式，可以使用默认值，默认的请求方式为:
# from corsheaders.defaults import default_methods
CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
)

# 允许跨域的请求头，可以使用默认值，默认的请求头为:
# from corsheaders.defaults import default_headers
# CORS_ALLOW_HEADERS = default_headers

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
    'csrf_token',
    'x-request-with',
    'responseType'
    "Range",
    'transfer-Encoding'
)

# 跨域请求时，是否运行携带cookie，默认为False
CORS_ALLOW_CREDENTIALS = True
# 允许所有主机执行跨站点请求，默认为False
# 如果没设置该参数，则必须设置白名单，运行部分白名单的主机才能执行跨站点请求
CORS_ORIGIN_ALLOW_ALL = True

# 配置白名单
CORS_ORIGIN_WHITELIST = (
    '*'
    # '127.0.0.1:8000',
    # 'localhost:8000',
    # '127.0.0.1:8080',
    # 'localhost:8080',
    # 'ads-cms-api.aataotao.com:8000'  #
    # 'taoduoduo-test.oss-cn-shenzhen.aliyuncs.com:80',  # 线上
    # '10.0.2.187:8080'  # 本地
)

# create global thread pool
GLOBAL_THREAD_POOL = threadPool()
ACCESS_KEY_ID = ""
ACCESS_KEY_SECRET = ""
TEMPLATE_CODE = ""
SIGN_NAME = ""
