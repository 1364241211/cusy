<template>
  <div>
    <v-md-editor v-model="text" height="80vh"></v-md-editor>
  </div>
</template>

<script lang="ts" setup>
import { ref, watch } from "vue";
const text = ref("");

watch(text, (newValue, oldValue) => {
  console.log(oldValue);
  console.log(newValue);
});
</script>

<style lang="scss" scoped></style>
