<template>
  <div>
    <md-editor
      v-model="text"
      :toolbars="toolbars"
      class="md-editor"
      @on-upload-img="handUploadImg"
      @on-save="saveMd"
    >
      <template #defToolbars>
        <normal-toolbar title="上传视频" @on-click="handleVideo">
          <template #trigger>
            <svg
              viewBox="0 0 1024 1024"
              xmlns="http://www.w3.org/2000/svg"
              data-v-78e17ca8=""
              class="md-icon"
            >
              <path
                fill="currentColor"
                d="M512 64a448 448 0 1 1 0 896 448 448 0 0 1 0-896zm0 832a384 384 0 0 0 0-768 384 384 0 0 0 0 768zm-48-247.616L668.608 512 464 375.616v272.768zm10.624-342.656 249.472 166.336a48 48 0 0 1 0 79.872L474.624 718.272A48 48 0 0 1 400 678.336V345.6a48 48 0 0 1 74.624-39.936z"
              ></path>
            </svg>
          </template>
        </normal-toolbar>
      </template>
    </md-editor>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref, watch } from "vue";
import MdEditor, { ToolbarNames } from "md-editor-v3";
import "md-editor-v3/lib/style.css";
import { useRequest } from "../hooks/useReqest";
import { useImageCompress } from "../hooks/useImageCompress";
import { METHOD } from "../types";
import { ElMessage } from "element-plus";
const NormalToolbar = MdEditor.NormalToolbar;
const toolbars = [
  "bold",
  "underline",
  "italic",
  "-",
  "title",
  "strikeThrough",
  "sub",
  "sup",
  "quote",
  "unorderedList",
  "orderedList",
  "-",
  "codeRow",
  "code",
  "link",
  "image",
  0,
  "table",
  "-",
  "revoke",
  "next",
  "save",
  "=",
  "pageFullscreen",
  "fullscreen",
  "preview",
  "htmlPreview",
  "catalog",
] as ToolbarNames[];

const video = ref<File | undefined | null>();
const text = ref("");
// 创建防抖 避免多次请求
const state = ref(false);


// 当点击保存按钮时保存文档
const saveMd = async (value: string) => {
  if (!state.value) {
    state.value = true;
    const { res, error } = await useRequest(
      "/uploadMd",
      METHOD.POST,
      JSON.stringify({
        file: {
          body: value,
          fileType: "md",
          fileSize: text.value.length,
        },
      })
    );
    if (res.value) {
      ElMessage.success(res.value.message);
    } else if (error.value) {
      ElMessage.error(error.value);
    }
    setTimeout(() => {
      state.value = false;
    }, 2000);
  } else {
    ElMessage.error("保存过于频繁,请2秒后在尝试!");
  }
};
// 上传图片到服务器
const handUploadImg = async (
  files: Array<File>,
  callback: (urls: Array<string>) => void
) => {
  const { dataUrl, size } = await useImageCompress(files.at(0)!);
  const { res, error } = await useRequest(
    "/uploadMdRes",
    METHOD.POST,
    JSON.stringify({
      file: {
        body: dataUrl.value,
        fileType: files.at(0)?.type.replace("image/", ""),
        fileSize: size.value,
      },
    })
  );
  if (error.value) {
    ElMessage.error("图片上传失败");
  }
  if (res.value) {
    console.log(res.value);
    callback([`http://192.168.2.103/static${res.value.info as string}`]);
  }
};

// 上传视频到服务器
const handleVideo = async () => {
  let fileInpt = document.createElement("input");
  fileInpt.setAttribute("id", "file");
  fileInpt.setAttribute("type", "file");
  fileInpt.setAttribute("name", "file");
  fileInpt.setAttribute("accept", "video/mp4");
  fileInpt.setAttribute("style", "visibility:hidden");
  fileInpt.addEventListener("change", async () => {
    video.value = fileInpt.files?.item(0);
    if (video.value) {
      const { dataUrl, size } = await useImageCompress(video.value);
      const { res, error } = await useRequest(
        "/uploadMdRes",
        METHOD.POST,
        JSON.stringify({
          file: {
            body: dataUrl.value,
            fileType: video.value.type.replace("video/", ""),
            fileSize: size.value,
          },
        })
      );
      if (res.value) {
        text.value =
          text.value +
          `<video controls preload='autoplay' name="media" width="100%" height="300">\r\n\t<source src='${
            "http://192.168.2.103/static" + res.value?.info
          }' type="video/mp4">\r\n</video>\r\n`;
      } else if (error.value) {
        ElMessage.error(error.value);
      }
    }
  });
  document.body.appendChild(fileInpt);
  fileInpt.value;
  fileInpt.click();
};

onMounted(async () => {
  const { res, error } = await useRequest("/uploadMd", METHOD.GET);
  if (res.value) {
    text.value = res.value.info as string;
  } else if (error.value) {
    ElMessage.error(error.value);
  }
  console.log(res.value);
  console.log(error.value);
});
</script>

<style lang="scss" scoped>
.md-editor {
  height: 90vh;
}
</style>
