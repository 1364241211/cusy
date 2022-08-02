<template>
  <div class="main">
    <header>东辰饭卡登记表</header>
    <van-form
      colon
      label-width="8em"
      ref="formInstance"
      :scroll-to-error="true"
      :show-error="true"
    >
      <van-cell-group inset>
        <van-field
          v-model="form.customer_name"
          name="customer_name"
          label="学生姓名"
          placeholder="请输入学生姓名"
          :rules="formRules.customer_name"
          required
        >
        </van-field>
        <van-field
          v-model="form.customer_id"
          name="customer_id"
          label="学生身份证号码"
          placeholder="请输入学生身份证号码"
          :rules="formRules.customer_id"
          required
        >
        </van-field>
        <van-field
          type="tel"
          v-model="form.par_phone"
          name="parent_phone"
          label="家长手机号码"
          placeholder="请输入家长手机号码"
          :rules="formRules.par_phone"
          required
        >
        </van-field>
        <van-field
          v-model="form.class_name"
          name="class_name"
          label="学生批次"
          placeholder="请选择学生班级"
          required
          :rules="formRules.class_name"
          is-link
          readonly
          @click="showPicker = true"
        >
        </van-field>
        <van-popup
          :show="showPicker"
          round
          position="bottom"
          style="width: 100vw"
        >
          <van-picker
            title="学生批次"
            :columns="
              classes.map((ele) => {
                return ele.class_name;
              })
            "
            @cancel="showPicker = false"
            @confirm="onConfirm"
          />
        </van-popup>
        <van-field
          name="customer_photo"
          type="file"
          required
          label="学生照片"
          input-align="left"
          center
        >
          <template #input>
            <van-icon
              name="plus"
              size="2rem"
              style="
                display: flex;
                justify-content: center;
                align-items: center;
                background-color: #d4d1d1;
                width: 5rem;
                height: 5rem;
              "
              v-if="!fileInputExist"
              color="white"
              @click="chooseFile"
            />
            <input
              ref="fileInput"
              type="file"
              name="customer_photo"
              color="white"
              accept="image/jpg,image/jpeg,image/png"
              v-show="false"
            />
            <div class="van-image-div">
              <van-icon
                name="cross"
                style="
                  height: 14px;
                  width: 14px;
                  display: flex;
                  justify-content: center;
                  align-items: center;
                  position: absolute;
                  z-index: 999;
                  top: -7px;
                  right: -7px;
                  background: rgba(0, 0, 0, 0.4);
                  border-radius: 50%;
                "
                color="rgba(255,255,255,.5)"
                v-if="fileInputExist"
                @click="clearImage"
              />
              <van-image
                fit="cover"
                position="center"
                :src="previewAvatar"
                height="5rem"
                width="5rem"
                style="border: 1px rgba(0, 0, 0, 0.3) solid"
                v-if="fileInputExist"
              >
              </van-image>
            </div>
          </template>
        </van-field>

        <van-cell :center="true">
          <van-button
            type="primary"
            round
            size="normal"
            icon="success"
            :disabled="wait"
            :loading="wait"
            loading-text="提交中，请稍等..."
            @click="submitForm"
            >提交
          </van-button>
        </van-cell>
      </van-cell-group>
    </van-form>
    <van-popup
      :show="idIsExist"
      position="bottom"
      :close-on-click-overlay="false"
      style="height: 40vh;width: 100vw; }"
    >
      <div class="wrapper">
        <h2>通知！</h2>
        <div class="block">
          您好，系统检测到身份证号码：<span>{{ form.customer_id }}</span
          >的用户以提交申请，是否再次提交?
        </div>
        <div class="button-group">
          <van-button type="success" @click="enterUpdateCus">是</van-button>
          <van-button type="danger" @click="router.push({ name: 'success' })"
            >否
          </van-button>
        </div>
      </div>
    </van-popup>
    <van-popup
      v-model:show="dialogShow"
      :close-on-click-overlay="false"
      :closeable="dialogCancelBtn"
      round
      teleport="body"
      style="text-align: center; padding: 1vh 1vw"
    >
      <h2 style="padding: 0; margin: 0.5vh 0vw; color: #2c3e50">通知!</h2>
      <component :is="PreviewMdVue"></component>
    </van-popup>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, reactive, ref } from "vue";
import { FieldRule, FormInstance, Notify } from "vant";
import PreviewMdVue from "./PreviewMd.vue";

import router from "../router";
import checkID from "../util/RegexVaild";
import service from "../util/api";
import type { classType, resMessage } from "../types";
import { useRequest } from "../hooks/useReqest";
import { METHOD } from "../types";
import { useImageCompress } from "../hooks/useImageCompress";

const dialogShow = ref(false);
const dialogCancelBtn = ref(false);
const wait = ref<boolean>(false);
const classes = ref<Array<classType>>([]);
const showPicker = ref(false);
const fileInputExist = ref(false);
const fileInput = ref<HTMLInputElement>();
const previewAvatar = ref("");
const formInstance = ref<FormInstance>();
const form = reactive({
  customer_name: "",
  customer_id: "",
  par_phone: "",
  class_name: "",
  class_id: 0,
  customer_photo: "",
});

const onConfirm = (value: any) => {
  showPicker.value = false;
  form.class_name = value;
  classes.value.forEach((ele: classType) => {
    if (ele.class_name == value) {
      form.class_id = ele.class_group;
    }
  });
  console.log(form.class_id);
};

const vaildName = (value: any) => {
  if (value === "") {
    return "请输入姓名！";
  } else if (!/^[\u4e00-\u9fa5]{0,10}$/.test(value)) {
    return "请输入10个内的汉字!";
  } else {
    return "";
  }
};

const vaildId = (value: any) => {
  if (value === "") {
    return "请输入身份号码！";
  } else if (!checkID(value)) {
    return "身份证验证未通过，请检查!";
  } else {
    return "";
  }
};

const vaildphone = (value: any) => {
  if (value === "") {
    return "请输入手机号码！";
  } else if (
    !/^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$/.test(
      value
    )
  ) {
    return "请输入合法的手机号码!";
  } else {
    return "";
  }
};

const formRules = reactive({
  customer_name: [
    { validator: vaildName, trigger: "onChange", required: true },
  ] as FieldRule[],
  customer_id: [
    { validator: vaildId, trigger: "onChange", required: true },
  ] as FieldRule[],
  par_phone: [
    { validator: vaildphone, trigger: "onChange", required: true },
  ] as FieldRule[],
  class_name: [{ required: true }],
});

// 点击图标触发input选择文件
const chooseFile = () => {
  fileInput.value?.addEventListener("change", () => {
    const IMAGE_TYPE = ["image/png", "image/jpg", "image/jpeg"];
    const file = fileInput.value?.files?.item(0);
    if (IMAGE_TYPE.includes(file?.type as string)) {
      useImageCompress(file!).then(({ realUrl }) => {
        fileInputExist.value = true;
        previewAvatar.value = realUrl.value as string;
        console.log(previewAvatar.value);
      });
    } else {
      Notify({ type: "danger", message: "图片类型只能为.jpg .jpeg .png" });
    }
  });
  fileInput.value?.click();
};

// 点击关闭图标 清除图片
const clearImage = () => {
  previewAvatar.value = "";
  fileInputExist.value = false;
  if (fileInput.value?.value) {
    fileInput.value!.value = "";
  }
};

// 用户身份身份证是否存在
const idIsExist = ref(false);

// 提交post请求到服务器
const subPost = async () => {
  const { res, error } = await useRequest(
    "/customerGeneralApi",
    METHOD.POST,
    JSON.stringify({
      customer_id: form.customer_id,
      customer_name: form.customer_name,
      parent_phone: form.par_phone,
      class_id: form.class_id,
      class_name: form.class_name,
      customer_photo: `${form.customer_id}.${fileInput.value?.files?.item(0)?.type.replace(
        "image/",
        ""
      )}`,
    })
  );
  if (res.value) {
    switch ((res.value as resMessage).code) {
      case 200:
        {
          // 上传用户信息成功时，上传用户头像
          await uploadImage();
          Notify({ type: "success", message: "提交成功,两秒后跳转。" });
          setTimeout(() => {
            router.push({ name: "success" });
          }, 2000);
          wait.value = false;
        }
        break;
      case 400:
        {
          Notify({
            type: "danger",
            message: "提交失败，可能网路有波动,请稍后提交!",
          });
        }
        break;
    }
  } else if (error.value) {
    Notify({ type: "danger", message: error.value });
  }
};

// 当用户点击是按钮时触发事件
const enterUpdateCus = async () => {
  idIsExist.value = false;
  await subPost();
};

// 当用户点击提交时，提交表单继续规则检验
const submitForm = () => {
  if (fileInput.value?.value.length === 0) {
    Notify({ type: "danger", message: "请选择学生照片" });
    return;
  }
  wait.value = true;
  formInstance.value
    ?.validate()
    .then(() => {
      service
        .get(`/customerGeneralApi?customer_id=${form.customer_id}`)
        .then((res) => {
          switch (res.data.code) {
            case 404:
              {
                subPost();
              }
              break;
            case 200:
              {
                idIsExist.value = true;
              }
              break;
          }
        });
    })
    .catch(() => {
      Notify({ type: "danger", message: "表单字段验证失败，请检查后提交!" });
      wait.value = false;
    });
};

const uploadImage = async () => {
const uploadImage = async (): Promise<void> => {
  const file = fileInput.value?.files?.item(0);
  const { dataUrl, size } = await useImageCompress(file as Blob);
  const { res, error } = await useRequest(
    "./uploadAvatar",
    METHOD.POST,
    JSON.stringify({
      avatarName: `${form.customer_id}.${file?.type.replace("image/", "")}`,
      avatarSize: size.value,
      avatar: dataUrl.value,
    })
  );
  if (res.value) {
    switch ((res.value as resMessage).code) {
      case 200:
    }
  } else if (error.value) {
    Notify({ type: "danger", message: error.value });
  }
};

// 组件挂载时钩子函数
onMounted(() => {
  service.get("/customerGeneralApi");
  service.get("/classGeneralApi").then((res) => {
    classes.value = res.data;
  });
  dialogShow.value = true;
  setTimeout(() => {
    dialogCancelBtn.value = true;
  }, 100);
});
</script>
<style lang="scss" scoped>
.main {
  height: 90vh;

  header {
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin-bottom: 2%;
  }

  .stuPhoto {
    width: 8em;
    color: var(--van-field-label-color);
    text-align: left;
    word-wrap: break-word;
    display: block;

    &::before {
      content: "*";
      color: red;
    }
  }

  .van-cell {
    margin: 2rem 0;

    &::deep(.van-cell__value) {
      .van-cell__value--alone {
        text-align: center;
      }
    }

    .stuPhoto {
      margin-bottom: 0.5rem;
    }
  }

  .van-button {
    width: 8rem;
    height: 2rem;
  }
}

.wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-around;
  width: 40vmax;
  height: 100%;
  border-radius: 15px;
  margin: 0 auto;

  .block {
    text-align: left;
    // flex-basis: 50%;
    padding: 0 2rem;

    span {
      color: red;
    }
  }

  .button-group {
    // flex-basis: 24%;

    .van-button {
      width: 5rem;
      margin: 0 1rem;
    }
  }
}
.van-image-div {
  position: relative;
  width: fit-content;
  height: fit-content;
}
</style>
