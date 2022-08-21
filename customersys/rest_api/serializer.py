import time
from hashlib import md5

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Admin, Customers, Class, Resources, ZipfilesInfo


# admin用户序列化器
class adminSerializer(serializers.ModelSerializer):
    admin_account = serializers.RegexField(regex=r"\d{6}", required=True)
    password = serializers.RegexField(regex=r'[A-Za-z0-9]{32}', required=True)
    admin_name = serializers.CharField(required=True, max_length=10)

    def create(self, validated_data):
        password = validated_data['password']
        fisrtEncryption = md5(password.encode()).hexdigest()
        validated_data['password'] = fisrtEncryption
        return Admin.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.admin_account = validated_data.get(instance, 'admin_account')
        instance.admin_password = validated_data.get(
            instance, 'admin_password')
        instance.admin_name = validated_data.get(instance, 'admin_name')
        instance.save()
        return instance

    class Meta:
        model = Admin
        fields = '__all__'
        read_only_fields = ('admin_id', 'admin_account',
                            'admin_name', 'admin_logtime')


# customer用户序列化器
class customerSerializer(serializers.ModelSerializer):
    # 身份证验证
    customer_id = serializers.RegexField(
        regex=r"^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$")
    customer_name = serializers.CharField(max_length=5)
    # 手机号验证
    parent_phone = serializers.RegexField(regex=r"^1[35678]\d{9}$")
    customer_photo = serializers.CharField()
    class_id = serializers.IntegerField()
    class_name = serializers.CharField()
    is_valided = serializers.IntegerField()

    def create(self, validated_data):
        return Customers.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.customer_id = validated_data.get("customer_id")
        instance.customer_name = validated_data.get("customer_name")
        instance.parent_phone = validated_data.get("parent_phone")
        instance.customer_photo = validated_data.get("customer_photo")
        instance.class_id = validated_data.get("class_id")
        instance.class_name = validated_data.get("class_name")
        instance.is_valided = validated_data.get("is_valided")
        instance.save()
        return instance

    class Meta:
        model = Customers
        fields = '__all__'
        read_only_fields = ('customer_logtime', 'id')


# class 班级序列化器
class classSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField()
    class_group = serializers.IntegerField()

    def create(self, validated_data):
        return Class.objects.create(**validated_data)

    class Meta:
        model = Class
        fields = '__all__'
        read_only_field = ('id',)


class mdResSerializer(serializers.ModelSerializer):
    res_name = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return Resources.objects.create(**validated_data)

    class Meta:
        model = Resources
        fields = '__all__'
        read_only_field = ('id',)


class zipFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZipfilesInfo
        fields = '__all__'


# admin用户token序列化器
class adminTokenObtainSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # 添加用户到token中
        token['admin_account'] = user.admin_account
        token['admin_name'] = user.admin_name
        token['is_active'] = True
        return token


class customerTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['customer_id'] = int(time.time())
        token['is_customer'] = True
        return token
