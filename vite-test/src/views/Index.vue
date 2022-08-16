<template>
  <van-tabs :active="active" animated>
    <van-tab title="登记">
      <component :is="Enroll"></component>
    </van-tab>
    <van-tab title="充值说明">
      <div class="md-preview">
        <component :is="PreviewMd" :edId="'recharge'" :type="2"></component>
      </div>
    </van-tab>
    <van-tab title="查询">
      <component :is="EnrollSearch"></component>
    </van-tab>
  </van-tabs>
</template>

<script lang="ts" setup>
import Enroll from "../components/Enroll.vue";
import EnrollSearch from "../components/EnrollSearch.vue";
import PreviewMd from "../components/PreviewMd.vue";
import { ref, reactive } from "vue";

import type { tabType } from "../types/index";

const active = ref(0);

const tabList = ref<Array<tabType>>([
  { title: "登记" },
  { title: "查询" },
  { title: "充值说明" },
]);
</script>
<style lang="scss" scoped>
.van-tabs {
  width: 100%;
  height: 100%;
}
.md-preview {
  height: 100vh;
  width: 100%;
  display: flex;
  justify-content: center;
  align-content: center;
  background: whitesmoke;
}
</style>
