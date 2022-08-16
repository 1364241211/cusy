<script setup lang="ts">
// code...
import { ref, onMounted } from "vue";
import { useRequest } from "../hooks/useReqest";
import { Notify } from "vant";
import MdEditor from "md-editor-v3";
import { resMessage } from "../types";

const text = ref<string>();
const props = defineProps<{ type: number; edId: string }>();

// 组件挂载时渲染md文档
onMounted(async () => {
  const { res, error } = await useRequest(`/mdGeneralApi?type=${props.type}`);
  if (res.value) {
    text.value = ((res.value as resMessage).info as string)
      ? ((res.value as resMessage).info as string)
      : "";
  } else if (error.value) {
    Notify({ type: "danger", message: error.value });
  }
});
</script>

<template>
  <div class="md-preview-div">
    <md-editor
      v-model="text"
      :preview-only="true"
      :editor-id="edId"
    ></md-editor>
  </div>
</template>

<style lang="scss" scoped>
/* code... */
.md-preview-div {
  width: 88vw;
  height: 86vh;
  overflow-y: scroll;
}
:deep(.md-previewOnly) {
  height: 100%;
}
:deep(img) {
  width: 100%;
}
</style>
