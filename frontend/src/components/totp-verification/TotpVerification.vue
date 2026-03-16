<template>
  <div class="totp-verification">
    <n-input v-model:value="code" type="number" placeholder="请输入验证码" :maxlength="6" :autocomplete="false" />
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const code = ref("");
</script>
