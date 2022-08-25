<script setup lang="ts">
import { ref, toRefs, watchEffect } from "vue";
const props = defineProps<{ currentProgress: number | any | string }>();
const { currentProgress } = toRefs(props);
const barColor = ref("#4c9f32");
const currentWidth = ref(`${currentProgress.value}%`);
watchEffect(() => {
  currentWidth.value = `${currentProgress.value}%`;
  if (currentProgress.value == undefined) {
    currentWidth.value = "0%";
  }
  if (currentProgress.value == 100) {
    barColor.value = "#8282d2";
  }
});
</script>

<template>
  <div class="progress">
    <div class="progress-bar">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped lang="scss">
/* code... */
.progress {
  height: 1.2rem;
  width: 100%;
  border: 0.1px solid #d7c8c8;
  background: white;
  margin: 0;
  padding: 0;
}
.progress-bar {
  background: v-bind(barColor);
  width: v-bind(currentWidth);
  height: 100%;
  border-radius: inherit;
  margin: 0;
  padding: 0;
}
</style>
