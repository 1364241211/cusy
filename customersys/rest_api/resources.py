from import_export import resources
from import_export.fields import Field

from .models import Customers


class customersResources(resources.ModelResource):
    customer_id = Field(attribute="customer_id", column_name="学（工）号")
    customer_name = Field(attribute="customer_name", column_name="客户姓名")
    customer_section_one = Field(column_name="一级部门")
    customer_section_two = Field(column_name="二级部门")
    customer_section_three = Field(column_name="三级级部门")
    customer_section_four = Field(column_name="四级部门")
    customer_id_id = Field(attribute="customer_id", column_name="证件号")
    customer_grant_type = Field(column_name="补助类型（0～29）")
    is_valided = Field(attribute="is_valided", column_name="审核结果")

    class Meta:
        model = Customers
        exclude = ("parent_phone", "customer_photo", "customer_logtime", "class_id", "class_name")
        export_order = ("id",)

    def dehydrate_is_valided(self, customer):
        content = str()
        is_valided = customer.is_valided
        if is_valided == 0:
            return "审核中"
        elif is_valided == 1:
            return "已通过"
        elif is_valided == 2:
            return "已驳回"

    def dehydrate_customer_grant_type(self, customer):
        return "9"

    def dehydrate_customer_section_one(self, customer):
        return "xxx"

    def dehydrate_customer_section_two(self, customer):
        return "xxx"

    def dehydrate_customer_section_three(self, customer):
        return "xxx"

    def dehydrate_customer_section_four(self, customer):
        return "xxx"
