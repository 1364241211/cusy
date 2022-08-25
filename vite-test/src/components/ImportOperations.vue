<script setup lang="ts">
import { ref } from "vue";
import {
  WarningFilled,
  CircleCheck,
  CircleClose,
  Key,
} from "@element-plus/icons";
import zhCn from "element-plus/lib/locale/lang/zh-cn";
import { useRequest } from "../hooks/useReqest";
import { METHOD, resMessage } from "../types";
import encryPass from "../util/crypto";
import { ElNotification, ElMessage } from "element-plus";

const locale = ref(zhCn);

const deleteDialog = ref(false);
const enterPass = ref("");
const enterDelte = async () => {
  if (enterPass.value.length == 0){
		ElNotification.warning("密码不能为空!")
		return
		}
		
  const { res, error } = await useRequest(
    "/clearAll",
    METHOD.POST,
    JSON.stringify({ password: encryPass(enterPass.value) })
  );
  if (res.value) {
    const serRes = res.value as resMessage;
    switch (serRes.code) {
      case 200:
        {
          ElNotification.success(serRes.info as string);
          deleteDialog.value = false;
        }
        break;
      default:
        {
          ElNotification.error(serRes.info as string);
          enterPass.value = "";
        }
        break;
    }
  } else if (error.value) {
    ElMessage.error(error.value);
  }
};
</script>

<template>
  <el-config-provider :locale="locale">
    <el-header>
      <el-button-group>
        <el-tooltip
          content="<strong style='color:red;'>警告：</strong>点击后<strong style='color:red'><i>删除所有数据(用户信息数据，班级信息数据)<i></strong>"
          raw-content
        >
          <el-button
            type="danger"
            :icon="WarningFilled"
            @click="deleteDialog = true"
            >删除所有数据
          </el-button></el-tooltip
        >
      </el-button-group>
    </el-header>
    <el-dialog v-model="deleteDialog" width="30%" title="警告!">
      <div class="dialog-div">
        <div style="margin: 25px 0; display: flex; align-items: center">
          <el-icon color="red" :size="40"><WarningFilled /></el-icon>
          <strong style="color: red"
            >该操作为重要操作!,在执行前需要检验您的信息!</strong
          >
        </div>
        <el-input
          v-model="enterPass"
          placeholder="请输入您的密码"
          type="password"
          :prefix-icon="Key"
          clearable
          show-password
        >
        </el-input>
      </div>
      <template #footer>
        <el-button-group
          ><el-button type="primary" :icon="CircleCheck" @click="enterDelte"
            >确认</el-button
          ><el-button
            type="danger"
            :icon="CircleClose"
            @click="deleteDialog = false"
            >取消</el-button
          ></el-button-group
        >
      </template>
    </el-dialog>
  </el-config-provider>
</template>

<style scoped lang="scss">
.el-header {
  display: flex;
  margin-bottom: 0.5rem;
  height: min-content;
  padding: 0;
  text-align: left;
  justify-content: space-between;
}
.dialog-div {
  display: flex;
  margin-bottom: 0.5rem;
  height: min-content;
  padding: 0;
  text-align: left;
  flex-direction: column;
  justify-content: space-between;
}
</style>
