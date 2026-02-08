<!-- @author: Churk -->
<!-- @description: 通用表格组件，用于展示数据表格，支持搜索、分页、排序、操作列等功能 -->
<!-- @status: 待审查 -->

<template>
  <div class="common-table-container">
    <!-- 搜索栏 -->
    <NCard
      v-if="$slots.search"
      :title="$t('page.demo.table.search.title')"
      bordered
      class="search-card"
    >
      <template #header-extra>
        <div class="table-actions">
          <NButton type="primary" @click="handleSearch">
            <template #icon>
              <FontAwesomeIcon icon="search" />
            </template>
            查询
          </NButton>
          <NButton @click="handleReset">
            <template #icon>
              <FontAwesomeIcon icon="rotate" />
            </template>
            重置
          </NButton>
        </div>
      </template>
      <div class="search-layout">
        <div class="search-content">
          <slot name="search" />
        </div>
      </div>
    </NCard>

    <!-- 表格主体 -->
    <NCard
      :title="title"
      bordered
      class="table-card"
      content-class="d-flex flex-column h-100 px-4"
    >
      <!-- 工具栏 -->
      <template #header-extra>
        <div class="table-actions">
          <slot name="toolbar" />
          <NButton secondary @click="reload">
            <template #icon>
              <FontAwesomeIcon icon="arrow-rotate-right" />
            </template>
            刷新
          </NButton>
        </div>
      </template>

      <!-- 表格 -->
      <div class="table-wrapper">
        <NDataTable
          remote
          flex-height
          :columns="columns"
          :data="dataList"
          :loading="loading"
          :pagination="pagination"
          :row-key="rowKey"
          :scroll-x="scrollX"
          style="height: 100%"
          v-bind="$attrs"
        />
      </div>
    </NCard>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { NCard, NDataTable, NButton } from "naive-ui";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import type { DataTableColumns, PaginationProps } from "naive-ui";

defineOptions({
  name: "CommonTable",
});

const props = defineProps<{
  title?: string;
  columns: DataTableColumns<any>;
  scrollX?: number;
  rowKey?: (row: any) => string | number;
  request: (params: {
    page: number;
    pageSize: number;
  }) => Promise<{ list: any[]; total: number }>;
}>();

const emit = defineEmits<{
  (e: "reset"): void;
  (e: "search"): void;
}>();

const loading = ref(false);
const dataList = ref<any[]>([]);

const pagination = reactive<PaginationProps>({
  page: 1,
  pageSize: 10,
  showSizePicker: true,
  pageSizes: [10, 20, 50, 100],
  itemCount: 0,
  showQuickJumper: true,
  prefix: ({ itemCount }) => `共 ${itemCount} 条`,
  onUpdatePage: (page: number) => {
    pagination.page = page;
    fetchData();
  },
  onUpdatePageSize: (pageSize: number) => {
    pagination.pageSize = pageSize;
    pagination.page = 1;
    fetchData();
  },
});

const fetchData = async () => {
  loading.value = true;
  try {
    const { list, total } = await props.request({
      page: pagination.page || 1,
      pageSize: pagination.pageSize || 10,
    });
    dataList.value = list;
    pagination.itemCount = total;
  } catch (error) {
    console.error("Failed to fetch data:", error);
  } finally {
    loading.value = false;
  }
};

const handleSearch = () => {
  pagination.page = 1;
  fetchData();
  emit("search");
};

const handleReset = () => {
  emit("reset");
  pagination.page = 1;
  fetchData();
};

const reload = () => {
  // 刷新时保持当前页码，除非你需要重置到第一页
  fetchData();
};

const reset = () => {
  pagination.page = 1;
  fetchData();
};

onMounted(() => {
  fetchData();
});

defineExpose({
  reload,
  reset,
});
</script>

<style scoped>
.common-table-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
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

.table-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.table-wrapper {
  flex: 1;
  min-height: 0;
  padding: 0;
}
</style>
