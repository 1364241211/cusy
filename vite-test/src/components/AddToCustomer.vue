<template>
  <div>
    <el-config-provider :locale="locale">
      <el-form
        ref="formInstance"
        status-icon
        :model="forms"
        label-position="top"
        :rules="rules"
      >
        <el-form-item label="id">
          <el-input v-model="forms.id" disabled></el-input>
        </el-form-item>
        <el-form-item label="学生姓名" prop="customer_name">
          <el-input v-model="forms.customer_name"></el-input>
        </el-form-item>
        <el-form-item label="学生身份证号码" prop="customer_id">
          <el-input v-model="forms.customer_id"></el-input>
        </el-form-item>
        <el-form-item label="家长电话" prop="parent_phone">
          <el-input v-model="forms.parent_phone"></el-input>
        </el-form-item>
        <el-form-item label="学生照片">
          <el-upload
            action="#"
            ref="upload"
            v-model:file-list="updateCustomerPhoto"
            list-type="picture-card"
            :limit="1"
            :on-exceed="handleExceed"
            :auto-upload="false"
            :before-upload="beforeAvatarUpload"
            :http-request="uploadAvatar"
            :on-preview="previewImage"
            class="avatar-uploader"
          >
            <el-icon><Plus /></el-icon>
            <!---<img
              class="avatar"
              :src="updateCustomerPhoto.at(0)?.url"
              style="width: 80px; height: 100px"
            />-->
          </el-upload>
        </el-form-item>
        <el-form-item label="学生班级">
          <el-select v-model="forms.class_name" placeholder="请选择班级">
            <el-option
              v-for="option in classes"
              :key="option.id"
              :label="option.class_name"
              :value="option.class_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="学生登记时间">
          <el-date-picker
            v-model="forms.customer_logtime"
            type="datetime"
            placeholder="请选择时间"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="updateCustomer">修改</el-button>
        </el-form-item>
      </el-form>
      <el-dialog
        v-model="dialogVisible"
        :title="updateCustomerPhoto.at(0)?.name"
        center
      >
        <img
          :src="dialogImageUrl"
          alt="Preview Image"
          style="max-height: 400px; max-width: 320px"
        />
      </el-dialog>
    </el-config-provider>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref, inject, onMounted } from "vue";
import zhCn from "element-plus/lib/locale/lang/zh-cn";
import { ElForm, ElMessage, UploadFile, UploadUserFile } from "element-plus";
import type {
  UploadRawFile,
  UploadProps,
  UploadInstance,
  FormInstance,
} from "element-plus";

import service from "../util/api";
import checkID from "../util/RegexVaild";
import type { classType, resMessage } from "../types/index";
import { UploadRequestOptions } from "element-plus/lib/components";
import { useImageCompress } from "../hooks/useImageCompress";
import { useRequest } from "../hooks/useReqest";
import { AxiosError } from "axios";

interface customer {
  id: number;
  customer_id: string;
  customer_name: string;
  customer_photo: string;
  parent_phone: string;
  class_name: string;
  class_id: number;
  customer_logtime: string;
}

const classes = ref<classType[]>([]);
const reload = inject("reload", Function, true);
const dialogVisible = ref(false);
const dialogImageUrl = ref("");
const locale = ref(zhCn);
const props = defineProps<{ itemProps: customer }>();

const formInstance = ref<FormInstance>();

const forms = reactive({
  id: props.itemProps.id,
  customer_name: props.itemProps.customer_name,
  customer_id: props.itemProps.customer_id,
  customer_photo: "",
  parent_phone: props.itemProps.parent_phone,
  class_name: props.itemProps.class_name,
  customer_logtime: new Date(props.itemProps.customer_logtime),
  class_id: 0,
});

// 用户头像
const updateCustomerPhoto = ref<UploadUserFile[]>([
  {
    name: props.itemProps.customer_photo,
    url: `${import.meta.env.VITE_APP_STATIC_URL}/avatar/${
      props.itemProps.customer_photo
    }`,
  },
]);

const vaildName = (rule: any, value: any, callback: any) => {
  value = forms.customer_name;
  if (value === "") {
    callback(new Error("请输入姓名！"));
  } else if (!/^[\u4e00-\u9fa5]{0,10}$/.test(value)) {
    callback(new Error("请输入10个内的汉字!"));
  } else {
    callback();
  }
};
const vaildId: (rule: any, value: any, callback: any) => void = async (
  rule: any,
  value: any,
  callback: any
) => {
  value = forms.customer_id;
  if (value == props.itemProps.customer_id) {
    callback();
  } else if (value === "") {
    callback(new Error("请输入身份号码！"));
  } else if (!checkID(value)) {
    callback(new Error("身份证验证未通过，请检查!"));
  } else {
    const { res, error } = await useRequest(
      `/customerGeneralApi?customer_id=${value}`
    );
    if (res.value) {
      switch ((res.value as resMessage).code) {
        case 200:
          callback(new Error("该身份证号码已存在"));
          break;
        case 403:
          callback();
          break;
      }
    } else if (error.value) {
      callback(error.value);
    }
  }
  callback();
  return;
};
const vaildphone = (rule: any, value: any, callback: any) => {
  value = forms.parent_phone;
  if (value === "") {
    callback(new Error("请输入手机号码！"));
  } else if (
    !/^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$/.test(
      value
    )
  ) {
    callback(new Error("请输入合法的手机号码!"));
  } else {
    callback();
  }
};

const rules = reactive({
  customer_id: [{ validator: vaildId, trigger: "blur", required: true }],
  customer_name: [{ validator: vaildName, trigger: "blur", required: true }],
  parent_phone: [{ validator: vaildphone, trigger: "blur", required: true }],
});

// 判断更改前是否是同一张图片
const isSame = ref(true);

// 上传组件实例
const upload = ref<UploadInstance>();
const TYPES = ["image/jpg", "image/png", "image/jpeg"];

// 修改界面图片预览
const previewImage = (file: UploadFile) => {
  dialogVisible.value = true;
  dialogImageUrl.value = file.url!;
};

// 当用户重新点击时图片时进行处理
const handleExceed: UploadProps["onExceed"] = (files) => {
  if (!TYPES.includes(files.at(0)?.type as string)) {
    ElMessage.error("上传头像的格式为,jpg,jpeg,png");
  } else {
    upload.value!.clearFiles();
    const file = files[0] as UploadRawFile;
    upload.value!.handleStart(file);
    updateCustomerPhoto.value.at(0)!.url = URL.createObjectURL(file);
    avatarType.value = file.type.replace("image/", "");
    console.log(updateCustomerPhoto.value.at(0));
    isSame.value = false;
  }
};

// 上传头像base64编码地址
const vdataUrl = ref("");
// 上传头像的类型
const avatarType = ref("");

// 上传图片进行处理
const beforeAvatarUpload: UploadProps["beforeUpload"] = async (rawFile) => {
  if (!TYPES.includes(rawFile.type as string)) {
    ElMessage.error("上传头像的格式为,jpg,jpeg,png");
    return false;
  } else {
    const { dataUrl } = await useImageCompress(rawFile);
    vdataUrl.value = dataUrl.value as string;
    return true;
  }
};

// 上传图片
const uploadAvatar = async (item: UploadRequestOptions): Promise<unknown> => {
  if (!isSame.value) {
    return service
      .post(
        "/uploadAvatar",
        JSON.stringify({
          avatarName: `${forms.customer_id}.${avatarType.value}`,
          avatarSize: vdataUrl.value.length,
          avatar: vdataUrl.value,
        })
      )
      .then((res) => {
        switch (res.data.code) {
          case 200:
            {
              ElMessage.success("图片上传成功！");
              reload();
            }
            break;
          case 404:
            ElMessage.error(res.data.message);
            break;
        }
      })
      .catch((err: AxiosError) => {
        ElMessage.error(err.message);
      });
  } else {
    reload();
  }
};

// 点击修改按钮提交请求
const updateCustomer = () => {
  formInstance.value?.validate((value: any) => {
    if (value) {
      classes.value.map((ele) => {
        if (ele.class_name == forms.class_name) {
          forms.class_id = ele.class_group;
        }
      });
      let formData = {
        customer_id: forms.customer_id,
        customer_name: forms.customer_name,
        parent_phone: forms.parent_phone,
        class_id: forms.class_id,
        class_name: forms.class_name,
        customer_photo: `${forms.customer_id}.${avatarType.value}`,
      };
      if (isSame.value) {
        formData.customer_photo = `${props.itemProps.customer_id}`;
      }
      const UpdateInfo = service
        .put(
          `/customers?customer_id=${props.itemProps.customer_id}`,
          JSON.stringify(formData)
        )
        .then((res) => {
          switch (res.data.code) {
            case 200:
              {
                // upload.value?.submit();
                ElMessage.success(res.data.message);
              }
              break;
            case 404: {
              ElMessage.error(res.data.message);
            }
          }
        })
        .catch((err) => {
          ElMessage.error(err.message);
        });
      const uploadImage = upload.value?.submit();
      Promise.all([UpdateInfo, uploadImage])
        .then((values) => {
          ElMessage.success("用户信息更新成功!");
        })
        .catch((err) => {
          ElMessage.error(err.value);
        });
    }
  });
};
// 组件加载时请求班级信息
onMounted(async () => {
  const { res, error } = await useRequest("classGeneralApi");
  if (res.value) {
    classes.value = res.value as classType[];
    classes.value.map((ele) => {
      if (ele.class_name == forms.class_name) {
        forms.class_id = ele.class_group;
      }
    });
  } else if (error.value) {
    ElMessage.error("班级信息获取失败！");
  }
});
</script>

<style lang="scss" scoped>
.el-form {
  border: whitesmoke 1px solid;
  border-radius: 15px;
  box-shadow: 1px 1px 1px 1px white;
  padding: 5px;
}
.avatar-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}
:deep(.el-dialog--center) {
  .el-dialog__body {
    text-align: center;
  }
}
</style>
