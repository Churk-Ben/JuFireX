<template>
  <div class="container">
    <div class="row g-3">
      <div class="col-12">
        <h1>{{ $t("app.title") }}</h1>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { NCard, NButton, NResult, NSpace } from "naive-ui";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { faGamepad } from "@fortawesome/free-solid-svg-icons";
</script>
