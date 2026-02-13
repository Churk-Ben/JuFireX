<!-- @author: Churk -->
<!-- @status: 阶段性完工 -->
<!-- @description: 通用表格组件，用于展示数据表格，支持搜索、分页、排序、操作列等功能 -->

<template>
  <div class="common-table-container">
    <!-- 搜索栏 -->
    <NCard
      v-if="$slots.search"
      :title="finalSearchTitle"
      class="search-card"
      content-class="d-flex pb-0"
      bordered
    >
      <!-- 工具栏 -->
      <template #header-extra>
        <div class="extra-actions">
          <NButton type="primary" @click="handleSearch">
            <template #icon>
              <FontAwesomeIcon icon="search" />
            </template>
            {{ $t("common.commonTable.search.action.search") }}
          </NButton>
          <NButton secondary @click="handleReset">
            <template #icon>
              <FontAwesomeIcon icon="arrow-rotate-right" />
            </template>
            {{ $t("common.commonTable.search.action.reset") }}
          </NButton>
        </div>
      </template>

      <!-- 筛选表单 -->
      <div class="search-form">
        <slot name="search" />
      </div>
    </NCard>

    <!-- 表格主体 -->
    <NCard
      :title="finalTableTitle"
      class="table-card"
      content-class="d-flex flex-column h-100 px-4"
      bordered
    >
      <!-- 工具栏 -->
      <template #header-extra>
        <div class="extra-actions">
          <slot name="toolbar" />
          <NButton secondary @click="handleReload">
            <template #icon>
              <FontAwesomeIcon icon="arrow-rotate-right" />
            </template>
            {{ $t("common.commonTable.table.action.reload") }}
          </NButton>
        </div>
      </template>

      <!-- 表格 -->
      <div class="table-wrapper">
        <NDataTable
          flex-height
          style="height: 100%"
          v-bind="$attrs"
          :remote="false"
          :columns="columns"
          :data="finalData"
          :loading="props.loading"
          :pagination="finalPagination"
          :row-key="rowKey"
          :scroll-x="scrollX"
        />
      </div>
    </NCard>
  </div>
</template>

<script setup lang="ts">
import { reactive, computed } from "vue";
import { NCard, NDataTable, NButton } from "naive-ui";

import type { PropType } from "vue";
import type { DataTableColumns, PaginationProps } from "naive-ui";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import { useI18n } from "vue-i18n";

const { t } = useI18n();

defineOptions({
  name: "CommonTable",
});

const props = defineProps({
  searchTitle: {
    type: String,
    default: undefined,
  },
  tableTitle: {
    type: String,
    default: undefined,
  },
  columns: {
    type: Array as PropType<DataTableColumns<any>>,
    required: true,
  },
  data: {
    type: Array as PropType<any[]>,
    default: () => [],
  },
  pagination: {
    type: [Boolean, Object] as PropType<boolean | PaginationProps>,
    default: true,
  },
  rowKey: {
    type: Function as PropType<(row: any) => string | number>,
    default: undefined,
  },
  scrollX: {
    type: Number,
    default: undefined,
  },
  loading: {
    type: Boolean,
    default: false,
  },
});

const finalSearchTitle = computed(
  () => props.searchTitle ?? t("common.commonTable.search.title"),
);
const finalTableTitle = computed(
  () => props.tableTitle ?? t("common.commonTable.table.title"),
);

const allData = computed(() => props.data || []);

// 内置分页配置
const internalPagination = reactive<PaginationProps>({
  page: 1,
  pageSize: 10,
  showSizePicker: true,
  pageSizes: [5, 10, 20, 50, 100],
  itemCount: 0,
  showQuickJumper: true,
  prefix: ({ itemCount }) =>
    t("common.commonTable.table.pagination.prefix", { itemCount }),
  onUpdatePage: (page: number) => {
    internalPagination.page = page;
  },
  onUpdatePageSize: (pageSize: number) => {
    internalPagination.pageSize = pageSize;
    internalPagination.page = 1;
  },
});

// 合并用户传入的分页配置
const finalPagination = computed(() => {
  if (props.pagination === false) return false;

  // 显式构造新对象，避免复杂类型推断
  const result: any = { ...internalPagination };

  if (typeof props.pagination === "object") {
    Object.assign(result, props.pagination);
  }

  return result as PaginationProps;
});

// 计算显示的数据
const finalData = computed(() => {
  return allData.value;
});

const emit = defineEmits<{
  (e: "reset"): void;
  (e: "search"): void;
  (e: "reload"): void;
}>();

const handleSearch = () => {
  internalPagination.page = 1;
  emit("search");
};

const handleReset = () => {
  internalPagination.page = 1;
  emit("reset");
};

const handleReload = () => {
  internalPagination.page = 1;
  emit("reload");
};
</script>

<style scoped>
.common-table-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.extra-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.search-card {
  flex-shrink: 0;
}

.table-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.table-wrapper {
  flex: 1;
  min-height: 0;
  padding: 0;
}
</style>
