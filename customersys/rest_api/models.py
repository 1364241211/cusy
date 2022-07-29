# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import hashlib

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class AdminBaseManager(BaseUserManager):
    def get_by_natural_key(self, username):
        try:
            admin = self.get(admin_account=username)
        except Exception as e:
            return None
        return admin


class Admin(AbstractBaseUser):
    objects = AdminBaseManager()
    admin_id = models.AutoField(primary_key=True)
    admin_account = models.IntegerField(unique=True)
    password = models.CharField(
        db_column="admin_password", max_length=255, blank=True, null=True)
    admin_name = models.CharField(max_length=10)
    # Field name made lowercase.
    admin_logTime = models.DateTimeField(
        db_column='admin_logTime', auto_now=True)
    # Field name made lowercase.
    last_login = models.DateTimeField(
        db_column='admin_lastLoginTime', blank=True, null=True)
    REQUIRED_FIELDS = ['admin_name', 'password']
    USERNAME_FIELD = 'admin_account'

    def check_password(self, raw_password):
        raw_password = hashlib.md5(raw_password.encode()).hexdigest()
        if raw_password == self.password:
            return True
        else:
            return False

    class Meta:
        managed = False
        db_table = 'Admin'


class Class(models.Model):
    class_name = models.CharField(db_column='class_Name', unique=True, max_length=255)  # Field name made lowercase.
    class_group = models.CharField(db_column='class_group', max_length=255)

    class Meta:
        managed = False
        db_table = 'Class'


class Customers(models.Model):
    # Field name made lowercase.
    customer_id = models.CharField(
        db_column='customer_ID', unique=True, max_length=18)
    customer_name = models.CharField(max_length=5)
    parent_phone = models.CharField(max_length=11)
    customer_photo = models.TextField()
    # Field name made lowercase.
    customer_logtime = models.DateTimeField(
        db_column='customer_logTime', auto_now=True)
    # Field name made lowercase.
    class_id = models.PositiveIntegerField(db_column='class_Id')
    # Field name made lowercase.
    class_name = models.CharField(db_column='class_Name', max_length=255)
    is_valided = models.IntegerField(db_column='is_valided')

    class Meta:
        managed = False
        db_table = 'Customers'


class Resources(models.Model):
    res_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Resources'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        'DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(Admin, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
