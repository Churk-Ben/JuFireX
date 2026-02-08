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
          <NButton secondary @click="handleReset">
            <template #icon>
              <FontAwesomeIcon icon="arrow-rotate-right" />
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
          :remote="!!request"
          flex-height
          :columns="columns"
          :data="finalData"
          :loading="loading"
          :pagination="finalPagination"
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
import { ref, reactive, onMounted, computed } from "vue";
import { NCard, NDataTable, NButton } from "naive-ui";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import type { DataTableColumns, PaginationProps } from "naive-ui";

defineOptions({
  name: "CommonTable",
});

export interface CommonTableProps {
  /** 表格标题 */
  title?: string;
  /** 列定义 */
  columns: DataTableColumns<any>;
  /** 静态数据源 (优先级高于 request) */
  data?: any[];
  /**
   * 数据加载函数
   * @param params 分页参数
   * @returns Promise<{ list: any[]; total?: number }> | Promise<any[]>
   */
  request?: (params: {
    page: number;
    pageSize: number;
  }) => Promise<{ list: any[]; total?: number } | any[]>;
  /**
   * 分页配置
   * - false: 关闭分页
   * - undefined: 使用默认分页
   * - PaginationProps: 自定义分页配置
   */
  pagination?: boolean | PaginationProps;
  /** 行主键 */
  rowKey?: (row: any) => string | number;
  /** 横向滚动宽度 */
  scrollX?: number;
}

const props = withDefaults(defineProps<CommonTableProps>(), {
  pagination: true,
  request: async () => [],
});

const emit = defineEmits<{
  (e: "reset"): void;
  (e: "search"): void;
  (e: "update:page", page: number): void;
  (e: "update:pageSize", pageSize: number): void;
}>();

const loading = ref(false);
const internalData = ref<any[]>([]);

// 计算最终使用的数据
const finalData = computed(() => props.data || internalData.value);

// 分页状态管理
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
    emit("update:page", page);
    fetchData();
  },
  onUpdatePageSize: (pageSize: number) => {
    internalPagination.pageSize = pageSize;
    internalPagination.page = 1;
    emit("update:pageSize", pageSize);
    fetchData();
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

const fetchData = async () => {
  // 如果提供了静态数据，则不进行请求
  if (props.data) return;

  loading.value = true;
  try {
    const params = {
      page: internalPagination.page || 1,
      pageSize: internalPagination.pageSize || 10,
    };

    const response = await props.request(params);

    if (Array.isArray(response)) {
      internalData.value = response;
      // 如果返回纯数组，且启用了分页，尝试自动推断 total (前端分页场景暂不处理，仅赋值)
      if (props.pagination !== false) {
        internalPagination.itemCount = response.length;
      }
    } else {
      internalData.value = response.list;
      if (response.total !== undefined) {
        internalPagination.itemCount = response.total;
      }
    }
  } catch (error) {
    console.error("Failed to fetch data:", error);
    internalData.value = [];
  } finally {
    loading.value = false;
  }
};

const handleSearch = () => {
  internalPagination.page = 1;
  fetchData();
  emit("search");
};

const handleReset = () => {
  emit("reset");
  internalPagination.page = 1;
  fetchData();
};

const reload = () => {
  // 刷新时保持当前页码
  fetchData();
};

const reset = () => {
  internalPagination.page = 1;
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
