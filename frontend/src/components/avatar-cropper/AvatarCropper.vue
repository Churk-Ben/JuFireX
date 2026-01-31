<template>
  <div class="avatar-cropper-trigger" @click="triggerSelect">
    <slot>
      <!-- Default trigger if no slot provided -->
      <n-button>Select Image</n-button>
    </slot>
    <input
      ref="fileInput"
      type="file"
      accept="image/*"
      class="hidden-input"
      @change="handleFileChange"
    />
  </div>

  <n-modal
    v-model:show="showModal"
    preset="card"
    title="Crop Avatar"
    style="width: 600px; max-width: 90vw"
    :mask-closable="false"
  >
    <div class="cropper-container" v-if="imageUrl">
      <img ref="imageRef" :src="imageUrl" alt="Source Image" />
    </div>

    <template #footer>
      <n-space justify="end">
        <n-button @click="showModal = false">Cancel</n-button>
        <n-button type="primary" :loading="processing" @click="confirmCrop">
          Confirm
        </n-button>
      </n-space>
    </template>
  </n-modal>
</template>

<script setup lang="ts">
import { ref, nextTick, onBeforeUnmount, watch } from "vue";
import { NModal, NButton, NSpace, useMessage } from "naive-ui";
import Cropper from "cropperjs";
import "cropperjs/dist/cropper.css";

const emit = defineEmits(["cropped", "error"]);

const fileInput = ref<HTMLInputElement | null>(null);
const imageRef = ref<HTMLImageElement | null>(null);
const showModal = ref(false);
const imageUrl = ref("");
const processing = ref(false);
let cropper: Cropper | null = null;
const message = useMessage();

function triggerSelect() {
  fileInput.value?.click();
}

function handleFileChange(e: Event) {
  const input = e.target as HTMLInputElement;
  if (input.files && input.files.length > 0) {
    const file = input.files[0];

    // Basic validation
    if (!file.type.startsWith("image/")) {
      message.error("Please select an image file");
      return;
    }

    // Create URL
    if (imageUrl.value) {
      URL.revokeObjectURL(imageUrl.value);
    }
    imageUrl.value = URL.createObjectURL(file);
    showModal.value = true;

    // Reset input
    input.value = "";
  }
}

watch(showModal, async (val) => {
  if (val) {
    await nextTick();
    if (imageRef.value) {
      initCropper();
    }
  } else {
    destroyCropper();
  }
});

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

  // Get cropped canvas at 256x256 as requested
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
      message.error("Failed to crop image");
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
.hidden-input {
  display: none;
}

.cropper-container {
  height: 400px;
  background-color: #f0f0f0;
  overflow: hidden;
}

.cropper-container img {
  display: block;
  max-width: 100%;
}
</style>
