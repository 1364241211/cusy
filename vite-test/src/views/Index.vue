<template>
  <van-tabs :active="active" animated>
    <van-tab title="登记">
      <component :is="Enroll"></component>
    </van-tab>
    <van-tab title="查询">
      <component :is="EnrollSearch"></component>
    </van-tab>
  </van-tabs>
</template>

<script lang="ts" setup>
import Enroll from "../components/Enroll.vue";
import EnrollSearch from "../components/EnrollSearch.vue";
import { ref, reactive } from "vue";

import type { tabType } from "../types/index";

const active = ref(0);

const tabList = ref<Array<tabType>>([{ title: "登记" }, { title: "查询" }]);
</script>
<style lang="scss" scoped>
.van-tabs {
  width: 100%;
  height:100%;
}
</style>
