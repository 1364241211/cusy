<template>
  <div>
    <el-form ref="formInstance" :inline="true" :model="addForm" :rules="rules">
      <el-form-item label="班级组" :inline-message="true" prop="class_group">
        <el-input
          v-model.number="addForm.class_group"
          placeholder="请输入班级组"
          clearable
        >
        </el-input>
      </el-form-item>
      <el-form-item
        label="班级批次"
        required
        inline-message="true"
        prop="class_name"
      >
        <el-input
          v-model="addForm.class_name"
          placeholder="请输入班级批次"
          clearable
        ></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitClass">确认添加</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import { ElMessage } from "element-plus";
import type { FormInstance } from "element-plus";

import type { classType } from "../types";
import { trigger } from "@vue/reactivity";
import service from "../util/api";

const formInstance = ref<FormInstance>();
const addForm = reactive<classType>({
  id: 0,
  class_name: "",
  class_group: 2020,
});
const validateGroup = (rule: any, value: any, callback: any) => {
  if (value === "") {
    callback(new Error("字段内容不为空"));
  } else if (!/\d+/.test(value)) {
    callback(new Error("字段内容必须为整数"));
  } else {
    callback();
  }
};
const validateName = (rule: any, value: any, callback: any) => {
  if (value === "") {
    callback(new Error("字段内容不为空"));
  } else if (!/[a-za-z0-9\u4e00-\u9fa5]+/.test(value)) {
    callback(new Error("字段内容不能含有特殊符号，如！,.。等"));
  } else {
    callback();
  }
};
const rules = reactive({
  class_group: [{ validator: validateGroup, required: true, trigger: "blur" }],
  class_name: [{ validator: validateName, required: true, trigger: "blur" }],
});

// submit the classForm Data
const submitClass = () => {
  formInstance.value
    ?.validate((value: boolean) => {
      if (value) {
        service
          .post(
            "/classes",
            JSON.stringify({
              class_name: addForm.class_name,
              class_group: addForm.class_group,
            })
          )
          .then((res) => {
            switch (res.data.code) {
              case 200:
                {
                  ElMessage.success({
                    type: "success",
                    message: "班级添加成功",
                  });
                }
                break;
              case 403:
                {
                  ElMessage.error("班级已存在");
                }
                break;
            }
          })
          .catch((err) => {
            ElMessage.error("未知错误");
          });
      }
    })
    .catch((err) => {
      ElMessage.error("表单验证失败，请检查");
    });
};
</script>

<style lang="scss" scoped></style>
