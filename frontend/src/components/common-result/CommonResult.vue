<template>
  <div class="result-container">
    <div class="result-content">
      <n-icon :name="icon" />
      <div class="result-message">{{ message }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const props = defineProps({
  icon: {
    type: String,
    default: "info",
  },
  message: {
    type: String,
    default: "Operation completed successfully",
  },
});
</script>

<style scoped>
.result-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.result-content {
  display: flex;
  align-items: center;
}

.result-message {
  margin-left: 10px;
}
</style>
