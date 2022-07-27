<template>
  <el-main>
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
        <van-popup :show="showPicker" round position="bottom">
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
          required
          label="学生照片"
          :rules="formRules.customer_photo"
        >
          <template #input>
            <van-uploader
              v-model="form.customer_photo"
              upload-icon="plus"
              accept="image/jpg,image/png,image/jpeg"
              :max-count="1"
              result-type="dataUrl"
            >
            </van-uploader>
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
            >提交</van-button
          >
        </van-cell>
      </van-cell-group>
    </van-form>
    <van-popup
      :show="idIsExist"
      position="bottom"
      :close-on-click-overlay="false"
      :style="{ height: '40vh' }"
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
            >否</van-button
          >
        </div>
      </div>
    </van-popup>
  </el-main>
</template>

<script lang="ts" setup>
import { reactive, ref } from "vue";
import { FieldRule, FormInstance, Notify } from "vant";
import type { UploaderFileListItem } from "vant/lib/uploader/types";
import router from "../router";

import checkID from "../util/RegexVaild";
import service from "../util/api";
import type { classType } from "../types";
import { compressAccurately, filetoDataURL } from "image-conversion";

const wait = ref<boolean>(false);
const classes = ref<Array<classType>>([]);
const showPicker = ref(false);
const formInstance = ref<FormInstance>();
const form = reactive({
  customer_name: "",
  customer_id: "",
  par_phone: "",
  class_name: "",
  class_id: 0,
  customer_photo: new Array<UploaderFileListItem>(),
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
  customer_photo: [{ required: true }],
});
// 用户身份身份证是否存在
const idIsExist = ref(false);

// 提交post请求到服务器
const subPost = async () => {
  await service
    .post(
      "/customerGeneralApi",
      JSON.stringify({
        customer_id: form.customer_id,
        customer_name: form.customer_name,
        parent_phone: form.par_phone,
        class_id: form.class_id,
        class_name: form.class_name,
        customer_photo: `${form.customer_id}.${form.customer_photo
          .at(0)
          ?.file?.type.replace("image/", "")}`,
      })
    )
    .then((res) => {
      switch (res.data.code) {
        case 200:
          {
            // 上传用户信息成功时，上传用户头像
            uploadImage(form.customer_photo.at(0) as UploaderFileListItem);
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
    })
    .catch((err) => {
      Notify({ type: "danger", message: err.message });
    });
};
// 当用户点击是按钮时触发事件
const enterUpdateCus = () => {
  idIsExist.value = false;
  subPost();
};
// 当用户点击提交时，提交表单继续规则检验
const submitForm = () => {
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
      Notify({ type: "danger", message: "字段验证失败，请检查后提交!" });
      wait.value = false;
    });
};
// 上传头像到服务器,用户头像大于2M时进行压缩
const uploadImage = async (file: UploaderFileListItem) => {
  file.status = "uploading";
  file.message = "上传中...";
  if (file.file?.type === "image/jpg" || "image/jpeg" || "image/png") {
    if ((file.file?.size as number) > 1024 * 1024 * 2) {
      file.message = "压缩中...";
      compressAccurately(file.file as Blob, 1000).then((value) => {
        filetoDataURL(value).then((dataUrl) => {
          service
            .post(
              "./uploadAvatar",
              JSON.stringify({
                avatarName: `${form.customer_id}.${file.file?.type.replace(
                  "image/",
                  ""
                )}`,
                avatarSize: dataUrl.length,
                avatar: dataUrl.replace(/data:image\/\w+;base64,/, ""),
              })
            )
            .then((res) => {
              switch (res.data.code) {
                case 200:
                  file.status = "done";
              }
            })
            .catch((err) => {
              file.message = "上传失败";
              file.status = "failed";
            });
        });
      });
    } else {
      service
        .post(
          "./uploadAvatar",
          JSON.stringify({
            avatarName: `${form.customer_id}.${file.file?.type.replace(
              "image/",
              ""
            )}`,
            avatarSize: file.content?.length,
            avatar: file.content?.replace(/data:image\/\w+;base64,/, ""),
          })
        )
        .then((res) => {
          switch (res.data.code) {
            case 200:
              file.status = "done";
          }
        })
        .catch((err) => {
          file.message = "上传失败";
          file.status = "done";
        });
    }
  } else {
    Notify({ type: "danger", message: "文件类型为jpg,jpeg,png" });
  }
};

service.get("/customerGeneralApi");
service.get("/classGeneralApi").then((res) => {
  classes.value = res.data;
});
// service.post("/customerToken")
</script>
<style lang="scss" scoped>
.el-main {
  /**display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
**/
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
:deep(.van-popup) {
  width: 100vw;
}
</style>
