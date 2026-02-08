<!-- @author: Churk -->
<!-- @description: 通用表格组件，用于展示数据表格，支持搜索、分页、排序、操作列等功能 -->
<!-- @status: 待审查 -->

<template>
  <div class="common-table-container">
    <!-- 搜索栏 -->
    <NCard
      v-if="$slots.search"
      :title="searchTitle"
      class="search-card"
      content-class="d-flex"
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
      :title="tableTitle"
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
          :loading="loading"
          :pagination="finalPagination"
          :row-key="rowKey"
          :scroll-x="scrollX"
        />
      </div>
    </NCard>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, type PropType } from "vue";
import { NCard, NDataTable, NButton } from "naive-ui";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import type { DataTableColumns, PaginationProps } from "naive-ui";

defineOptions({
  name: "CommonTable",
});

const props = defineProps({
  searchTitle: {
    type: String,
    default: "筛选表单",
  },
  tableTitle: {
    type: String,
    default: "数据表格",
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
});

// 内置分页配置
const internalPagination = reactive<PaginationProps>({
  page: 1,
  pageSize: 10,
  showSizePicker: true,
  pageSizes: [5, 10, 20, 50],
  itemCount: 0,
  showQuickJumper: true,
  prefix: ({ itemCount }) => `共 ${itemCount} 条`,
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

const loading = ref(false);
const allData = computed(() => props.data || []);

// 计算显示的数据
const finalData = computed(() => {
  const data = allData.value;
  if (props.pagination === false) return data;

  const page = internalPagination.page || 1;
  const pageSize = internalPagination.pageSize || 10;

  // 确保页码不越界
  const maxPage = Math.ceil(data.length / pageSize) || 1;
  if (page > maxPage) {
    internalPagination.page = maxPage;
    return data.slice((maxPage - 1) * pageSize, maxPage * pageSize);
  }

  const start = (page - 1) * pageSize;
  const end = start + pageSize;
  return data.slice(start, end);
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
