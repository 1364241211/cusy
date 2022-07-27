<template>
  <div>
    <van-form>
      <van-search
        v-model="searchValue"
        show-action
        placeholder="请输入身份号码"
        @search="search"
      >
        <template #action>
          <div @click="search">搜索</div>
        </template>
      </van-search>
    </van-form>
    <van-empty image="error" description="查询用户不存在" v-if="!isExist" />
    <van-empty image="network" description="网络错误" v-if="netError" />
    <div class="user-group" v-if="isExist">
      <div class="avatar">
        <van-image
          width="80px"
          height="100px"
          :src="'/static/avatar/' + userInfo.customer_photo"
          fit="cover"
          position="center"
        />
      </div>
      <div class="user-info-div">
        <van-form>
          <van-field
            v-model="userInfo.customer_name"
            readonly
            label="学生姓名"
          ></van-field>
          <van-field
            v-model="userInfo.customer_id"
            readonly
            label="学生身份证"
          ></van-field>
          <van-field
            v-model="userInfo.parent_phone"
            readonly
            label="家长电话"
          ></van-field>
          <van-field
            v-model="userInfo.class_name"
            readonly
            label="学生班级"
          ></van-field>
          <van-field
            v-model="userInfo.is_valided"
            readonly
            label="审核结果"
          ></van-field>
        </van-form>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { AxiosResponse } from "axios";
import { reactive, ref } from "vue";

import { customer } from "../types/index";
import service from "../util/api";

const isExist = ref(true);
const netError = ref(false);
const errorMessage = ref("");
const searchValue = ref("");
const validedColor = ref("green");
const userInfo: customer = reactive({
  id: 0,
  customer_name: "",
  customer_id: "",
  parent_phone: "",
  customer_photo: "",
  class_name: "",
  class_id: 0,
  customer_logtime: "",
  is_valided: "",
});
const setUserInfo = (res: AxiosResponse) => {
  userInfo.id = res.data.info.id;
  userInfo.customer_name = res.data.info.customer_name;
  userInfo.customer_id = res.data.info.customer_id;
  userInfo.parent_phone = res.data.info.parent_phone;
  userInfo.class_name = res.data.info.class_name;
  userInfo.class_id = res.data.info.class_id;
  userInfo.customer_logtime = res.data.info.customer_logtime;
  userInfo.customer_photo = res.data.info.customer_photo;
  switch (res.data.info.is_valided) {
    case 0:
      {
        userInfo.is_valided = "审核中...";
        validedColor.value = "blue";
      }
      break;
    case 1:
      {
        userInfo.is_valided = "审核通过";
        validedColor.value = "green";
      }
      break;
    case 2:
      {
        userInfo.is_valided = "被驳回,请联系管理员";
        validedColor.value = "red";
      }
      break;
  }
};
const search = () => {
  if (searchValue.value !== "") {
    service
      .get(`/customerGeneralApi?customer_id=${searchValue.value}`)
      .then((res) => {
        switch (res.data.code) {
          case 200:
            {
              isExist.value = true;
              netError.value = false;
              setUserInfo(res);
            }
            break;
          case 404:
            {
              isExist.value = false;
              netError.value = false;
            }
            break;
        }
      })
      .catch((err) => {
        netError.value = true;
        isExist.value = true;
        errorMessage.value = err.config;
      });
  }
};
</script>

<style lang="scss" scoped>
.van-search {
  height: 50px;
}
.user-group {
  display: flex;
  background-color: white;
  height: 90vh;
  .avatar {
    width: 25%;
    margin-top: calc(5% + 2px);
    padding: calc(12%) 0;
  }
  .user-info-div {
    width: 75%;
    display: flex;
    flex-direction: column;
    margin-top: 5%;
    padding: 2% 0;
    :deep(.van-field) {
      margin: 10% 0;
      &:last-child {
        margin: 10% 0 5% 0;
        .van-field__control {
          color: v-bind("validedColor");
        }
      }
    }
  }
}
input[type="search"] {
  color: black;
}
:deep(.van-search__field) {
  margin: 0;
}
.van-empty {
  background: white;
}
</style>
