<!-- @author: Lithe-Admin -->
<!-- @description: 滚动容器组件，用于包裹内容并添加滚动条 -->
<!-- @status: 完工 -->

<template>
  <div class="scroll-container-root">
    <NScrollbar v-if="scrollable" :ref="forwardRef" v-bind="$attrs">
      <div class="scroll-content" :class="wrapperClass" :style="wrapperStyle">
        <slot />
      </div>
    </NScrollbar>
    <div
      v-else
      class="scroll-container-root scroll-content"
      :class="wrapperClass"
      :style="wrapperStyle"
    >
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import { NScrollbar } from "naive-ui";
import { getCurrentInstance } from "vue";

import type { ScrollbarProps } from "naive-ui";
import type { CSSProperties, ComponentPublicInstance } from "vue";

export interface ContentWrapperProps extends /* @vue-ignore */ ScrollbarProps {
  scrollable?: boolean;
  wrapperClass?: string;
  wrapperStyle?: CSSProperties;
}

defineOptions({
  inheritAttrs: false,
});

const {
  scrollable = true,
  wrapperClass,
  wrapperStyle,
} = defineProps<ContentWrapperProps>();

const instance = getCurrentInstance();

function forwardRef(ref: Element | ComponentPublicInstance | null) {
  if (instance) {
    instance.exposed = ref || {};
    instance.exposeProxy = ref || {};
  }
}
</script>

<style scoped>
.scroll-container-root {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.scroll-content {
  padding: 16px;
  min-height: 100%;
}

/* Mobile padding adjustment */
@media (max-width: 640px) {
  .scroll-content {
    padding: 8px;
  }
}
</style>
