<script setup lang="ts">
import { provide, ref } from "vue";
const fatherShow = ref(true);
const updateFaShow = () => {
  fatherShow.value = !fatherShow.value;
};
provide("updateFaShow", updateFaShow);
</script>

<template>
  <div class="mainContent" v-if="fatherShow">
    <router-view></router-view>
  </div>
  <router-view name="adminVue"></router-view>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  position: relative;
  /* height: calc(81vw + 10px); */
  height: max-content;
  width: calc(100%);
}

.mainContent {
  background: #71b6a2;
  height: calc(100vh);
  width: calc(100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
