<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { Download, Refresh } from "@element-plus/icons";
import zhCn from "element-plus/lib/locale/lang/zh-cn";
import { ElMessage } from "element-plus";
import DownloadProgress from "./DownloadProgress.vue";

import type { zipFileInfo } from "../types";
import { useRequest } from "../hooks/useReqest";
import { METHOD } from "../types";
import { resMessage } from "../types";
import service from "../util/api";

const locale = ref(zhCn);

const downloadLoadingList = ref([false, false, false]);
const exportButtonLoading = ref(false);
const avatarFileInfo = ref<Array<zipFileInfo>>([]);
const totalProgressLsit = ref<Array<Array<number>>>([]);

// 分片下载图片压缩包
const downloadZipFile = async (index: number) => {
  downloadLoadingList.value[index] = true;
  let fileDataList: Array<Blob> = [];
  let taskQueen = [];
  const fileLength: number = avatarFileInfo.value.at(index)?.zip_size!;
  const fileName: string = avatarFileInfo.value.at(index)?.zip_name!;
  const uuid = fileName.split(".")[0];
  const SLICE_COUNT = 10;
  const Q: number = Math.floor(fileLength / SLICE_COUNT);
  for (let i = 0; i < SLICE_COUNT; i++) {
    /* const progress = ref<number | undefined>(); */
    if (i == SLICE_COUNT - 1)
      taskQueen.push(
        serq(`/exportAvatar?uuid=${uuid}`, i * Q, fileLength, index, i)
      );
    else
      taskQueen.push(
        serq(`/exportAvatar?uuid=${uuid}`, i * Q, (i + 1) * Q - 1, index, i)
      );
    /* totalProgressLsit.value.at(index).value[i] = progress; */
  }

  try {
    for (let i = 0; i < 2; i++) {
      const values = await Promise.all(taskQueen.slice(i * 5, (i + 1) * 5));
      values.forEach((value) => {
        fileDataList.push(value.data);
      });
    }
    const file = new Blob(fileDataList);
    const a = document.createElement("a");
    a.href = window.URL.createObjectURL(file);
    a.download = fileName;
    a.click();
    window.URL.revokeObjectURL(a.href);
  } catch (errors: any) {
    ElMessage.error(errors.message);
  }
  downloadLoadingList.value[index] = false;
};

// 发送导出图片请求
const exportAvatar = async () => {
  exportButtonLoading.value = true;
  const { res: f1, error: f2 } = await useRequest(
    "/exportAvatar",
    METHOD.PATCH
  );
  if (f1.value) {
  } else if (f2.value) {
    ElMessage.error(f2.value);
    return;
  }
  await refreshPage();
  setTimeout(() => {
    exportButtonLoading.value = false;
  }, 3000);
};

const serq = (
  url: string,
  start: number,
  end: number,
  index: number,
  currIndex: number
) => {
  const headers = {
    /* "transfer-encoding": "chunked", */
    Range: `bytes=${start}-${end}`,
  };
  const s = service.post(url, undefined, {
    responseType: "blob",
    headers: headers,
    timeout: 300000,
    onDownloadProgress(progressEvent) {
      totalProgressLsit.value[index][currIndex] = Math.round(
        (progressEvent.loaded / progressEvent.total) * 100
      );
    },
  });
  return s;
};

// 刷新页面
const refreshPage = async () => {
  const { res: f1, error: f2 } = await useRequest("/exportAvatar", METHOD.GET);
  if (f1.value) {
    avatarFileInfo.value = (f1.value as resMessage).info as zipFileInfo[];
  } else if (f2.value) {
    ElMessage.error(f2.value);
    return;
  }
};

// 将文件大小冲b转换到Mb
const convToMb = (row: any, column: any, cellValue: any, index: any) => {
  cellValue = (cellValue / 1024 / 1024).toFixed(2);
  return cellValue;
};

const timeId = ref();

onMounted(async () => {
  const progress1 = new Array(10).fill(0);
  const progress2 = new Array(10).fill(0);
  const progress3 = new Array(10).fill(0);
  totalProgressLsit.value?.push(progress1);
  totalProgressLsit.value?.push(progress2);
  totalProgressLsit.value?.push(progress3);
  await refreshPage();
  // 每隔两秒刷新页面
  timeId.value = setInterval(async () => {
    await refreshPage();
  }, 3000);
});

onUnmounted(() => {
  clearInterval(timeId.value);
});

// code...
</script>

<template>
  <div>
    <el-config-provider :locale="locale">
      <el-header>
        <el-button-group>
          <el-tooltip
            content="点击后生成一个任务用于后台压缩图片，压缩成功后即可下载<br/><strong style='color:red'><i>文件内容过大，请耐心等待!<i></strong>"
            raw-content
          >
            <el-button
              type="primary"
              :icon="Download"
              @click="exportAvatar"
              :loading="exportButtonLoading"
              >导出所有图片
            </el-button></el-tooltip
          >
          <el-tooltip
            content="点击后<strong style='color:red'><i>刷新页面!<i></strong>的数据"
            raw-content
          >
            <el-button type="warning" :icon="Refresh" @click="refreshPage"
              >刷新</el-button
            ></el-tooltip
          >
        </el-button-group>
      </el-header>

      <el-table
        :data="avatarFileInfo"
        ref="tableInstance"
        max-height="800"
        border
        stripe
      >
        <el-table-column
          label="Id"
          width="70"
          height="10"
          prop="id"
          fit
          align="center"
        >
        </el-table-column>
        <el-table-column
          prop="zip_name"
          label="文件名"
          align="center"
          width="400"
        ></el-table-column>
        <el-table-column
          prop="zip_size"
          label="文件大小(mb)"
          align="center"
          :formatter="convToMb"
        ></el-table-column>
        <el-table-column
          prop="last_modified_time"
          label="文件生成时间"
          align="center"
        ></el-table-column>
        <el-table-column align="center" label="下载进度条">
          <template #default="scoped">
            <div class="progress-group">
              <component
                v-for="cur in totalProgressLsit?.at(scoped.$index)"
                :is="DownloadProgress"
                :currentProgress="`${cur ? cur : 0}`"
              >
              </component>
            </div>
          </template>
        </el-table-column>
        <el-table-column align="center" label="操作">
          <template #default="tail">
            <el-button-group>
              <el-button
                v-if="avatarFileInfo[tail.$index].download! == 1"
                type="success"
                size="small"
                :icon="Download"
                :loading="downloadLoadingList[tail.$index]"
                @click="downloadZipFile(tail.$index)"
                >下载</el-button
              >
              <el-tag v-else hit type="danger"> 资源准备中.. </el-tag>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </el-config-provider>
  </div>
</template>

<style scoped lang="scss">
/* code... */
.el-header {
  display: flex;
  margin-bottom: 0.5rem;
  height: min-content;
  padding: 0;
  text-align: left;
  justify-content: space-between;
  .el-input {
    width: 220px;
  }
}
.el-message-box__message {
  white-space: pre-wrap;
}
.button-groups {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-evenly;
  .el-button + .el-button {
    margin: 0;
  }
}
.progress-group {
  display: flex;
  width: 100%;
  margin: 0;
  padding: 0;
  & > :first-child {
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
  }
  & > :last-child {
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
  }
}
</style>
