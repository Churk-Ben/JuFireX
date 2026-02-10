<!-- @author: Churk -->
<!-- @description: 头像裁剪组件，用于裁剪用户上传的头像 -->
<!-- @status: 完工 -->

<template>
  <div class="avatar-cropper-trigger" @click="triggerSelect">
    <slot>
      <n-button>{{ $t("common.avatarCropper.select") }}</n-button>
    </slot>
    <input
      ref="fileInput"
      type="file"
      accept="image/*"
      class="d-none"
      @change="handleFileChange"
    />
  </div>

  <n-modal
    v-model:show="showModal"
    preset="card"
    :title="$t('common.avatarCropper.title')"
    style="width: 600px; max-width: 90vw"
    :mask-closable="false"
    @after-leave="handleAfterLeave"
  >
    <div class="cropper-container" v-if="imageUrl">
      <img ref="imageRef" :src="imageUrl" alt="Source Image" />
    </div>

    <template #footer>
      <n-space justify="end">
        <n-button @click="showModal = false">
          {{ $t("common.avatarCropper.cancel") }}
        </n-button>
        <n-button type="primary" :loading="processing" @click="confirmCrop">
          {{ $t("common.avatarCropper.confirm") }}
        </n-button>
      </n-space>
    </template>
  </n-modal>
</template>

<script setup lang="ts">
import { ref, nextTick, onBeforeUnmount, watch } from "vue";
import { NModal, NButton, NSpace } from "naive-ui";

import Cropper from "cropperjs";
import "cropperjs/dist/cropper.css";

defineOptions({
  name: "AvatarCropper",
});

const emit = defineEmits(["cropped", "error"]);

const fileInput = ref<HTMLInputElement | null>(null);
const imageRef = ref<HTMLImageElement | null>(null);
const showModal = ref(false);
const imageUrl = ref("");
const processing = ref(false);
let cropper: Cropper | null = null;

function triggerSelect() {
  fileInput.value?.click();
}

function handleFileChange(e: Event) {
  const input = e.target as HTMLInputElement;
  if (input.files && input.files.length > 0) {
    const file = input.files[0];

    // 简单校验
    if (!file.type.startsWith("image/")) {
      return;
    }

    // 创建 URL
    if (imageUrl.value) {
      URL.revokeObjectURL(imageUrl.value);
    }
    imageUrl.value = URL.createObjectURL(file);
    showModal.value = true;

    // 重置输入
    input.value = "";
  }
}

watch(showModal, async (val) => {
  if (val) {
    await nextTick();
    if (imageRef.value) {
      initCropper();
    }
  }
});

function handleAfterLeave() {
  destroyCropper();
}

function initCropper() {
  if (cropper) {
    cropper.destroy();
  }
  if (!imageRef.value) return;

  cropper = new Cropper(imageRef.value, {
    aspectRatio: 1,
    viewMode: 1,
    dragMode: "move",
    autoCropArea: 1,
    background: false,
    zoomable: true,
    movable: true,
    scalable: false,
    rotatable: false,
    cropBoxMovable: false,
    cropBoxResizable: false,
  });
}

function destroyCropper() {
  if (cropper) {
    cropper.destroy();
    cropper = null;
  }
}

function confirmCrop() {
  if (!cropper) return;

  processing.value = true;

  // 裁剪图片
  const canvas = cropper.getCroppedCanvas({
    width: 256,
    height: 256,
    imageSmoothingEnabled: true,
    imageSmoothingQuality: "high",
  });

  canvas.toBlob((blob: Blob | null) => {
    processing.value = false;
    if (blob) {
      emit("cropped", blob);
      showModal.value = false;
    } else {
      emit("error", new Error("Failed to create blob"));
    }
  }, "image/png");
}

onBeforeUnmount(() => {
  destroyCropper();
  if (imageUrl.value) {
    URL.revokeObjectURL(imageUrl.value);
  }
});
</script>

<style scoped>
.cropper-container {
  height: 400px;
  background-color: #f0f0f020;
  border-radius: var(--n-border-radius);
  overflow: hidden;
}

.cropper-container img {
  display: block;
  max-width: 100%;
}
</style>
