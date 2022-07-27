<template>
  <el-config-provider :locale="locale">
    <el-header>
      <el-button-group>
        <el-button
          type="primary"
          :disabled="buttonEnable"
          :icon="Finished"
          @click="moderateUsers(1)"
          >通过 ({{ buttonEnable ? 0 : selectionRows }})</el-button
        >
        <el-button
          type="danger"
          :disabled="buttonEnable"
          :icon="CircleClose"
          @click="moderateUsers(2)"
          >驳回 ({{ buttonEnable ? 0 : selectionRows }})</el-button
        >
      </el-button-group>
      <el-input
        v-model="search"
        placeholder="请输入查询关键字"
        @input="searchCustomer"
        clearable
        :prefix-icon="Search"
        @clear="clearSearch"
      />
    </el-header>
    <el-table
      :data="tableData"
      ref="tableInstance"
      max-height="800"
      v-loading="tableLoading"
      element-loading-text="加载中"
      border
      stripe
      @selection-change="columnSelect"
    >
      <el-table-column type="selection"></el-table-column>
      <el-table-column
        label="Id"
        width="70"
        height="10"
        prop="id"
        fit
        align="center"
      >
      </el-table-column>
      <el-table-column
        prop="customer_name"
        label="学生姓名"
        align="center"
        width="100"
      ></el-table-column>
      <el-table-column prop="customer_photo" label="学生照片" align="center">
        <template #default="scope">
          <div
            style="display: flex; align-items: center; justify-content: center"
          >
            <el-image
              :src="'/static/avatar/' + scope.row.customer_photo"
              style="height: 100px; width: 80px"
              fit="cover"
              :lazy="true"
              :preview-src-list="pre_src_list"
              :initial-index="pre_init_index"
              :z-index="5000"
              preview-teleported
              @click="changeInitIndex(scope.$index)"
            >
            </el-image>
          </div>
        </template>
      </el-table-column>
      <el-table-column
        prop="customer_id"
        label="学生身份证号"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="parent_phone"
        label="家长手机号"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="class_name"
        label="学生批次"
        align="center"
        :filter-method="classFiltersMethod"
        :filters="classFilters"
      ></el-table-column>
      <el-table-column
        prop="customer_logtime"
        label="学生登记时间"
        align="center"
      ></el-table-column>
      <el-table-column
        label="审核状态"
        align="center"
        prop="is_valided"
        :filters="statusFilters"
        :filter-method="statusFiltersMethod"
      >
        <template #default="tag">
          <el-tag
            :type="tag.row.is_valided == 0 ? 'warning' : 'danger'"
            size="large"
            effect="dark"
            disable-transitions
            >{{ tag.row.is_valided === 0 ? "待审核" : "驳回" }}</el-tag
          >
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :page-sizes="pageSizeList"
      :total="pagnation.count"
      layout="total,prev, pager, next,jumper,sizes"
      background
      @size-change="sizeChange"
      @current-change="jumpPage"
  /></el-config-provider>
</template>

<script lang="ts" setup>
import { ref, reactive, watch, inject } from "vue";
import { ElMessage, ElTable } from "element-plus";
import { AxiosResponse } from "axios";
import type { TableColumnCtx } from "element-plus/es/components/table/src/table-column/defaults";
import zhCn from "element-plus/lib/locale/lang/zh-cn";

import { Search, CircleClose, Finished } from "@element-plus/icons";

import { customer, pagnationData, classType } from "../types/index";
import service from "../util/api";

const locale = zhCn;
const pagnation = reactive<pagnationData>({
  count: 0,
  next: "null",
  previous: "null",
});
const statusFilters = [
  {
    text: "待审核",
    value: "0",
  },
  {
    text: "驳回",
    value: "2",
  },
];
const classFilters = ref<Array<{ text: string; value: string }>>([]);
const tableLoading = ref<boolean>(false);
const changeLoading = (): void => {
  tableLoading.value = !tableLoading.value;
};
const tableData = ref<Array<customer>>();
const tableInstance = ref<InstanceType<typeof ElTable>>();
const buttonEnable = ref(true);
const selectionRows = ref(0);
// 状态过滤方法
const statusFiltersMethod = (
  value: string,
  row: customer,
  column: TableColumnCtx<customer>
) => {
  const property = column["property"] as string;
  console.log(value);
  console.log(row);
  console.log(column);
  return row[property] == value;
};
//班级过滤方法
const classFiltersMethod = (
  value: string,
  row: customer,
  column: TableColumnCtx<customer>
) => {
  const property = column["property"] as string;
  return row[property] == value;
};

//重制班级过滤
const restClassFilter = () => {
  tableInstance.value?.clearFilter(["class_name"]);
};
// 设置通过传递的response设置表格数据tableData
const set_tableData = (res: AxiosResponse) => {
  pagnation.count = res.data.count;
  pagnation.next = res.data.next;
  pagnation.previous = res.data.previous;
  tableData.value = res.data.results;
  tableData.value!.forEach((ele) => {
    pre_src_list.value.push(ele.customer_photo);
  });
};
const columnSelect = () => {
  if (tableInstance.value?.getSelectionRows().length !== 0) {
    buttonEnable.value = false;
    selectionRows.value = tableInstance.value?.getSelectionRows().length;
  } else {
    buttonEnable.value = true;
  }
};
// 获取父级组件的reload方法
const reload = inject("reload", Function, true);

// 为按钮组添加点击事件
// status :1 通过
// status :2 驳回
const moderateUsers = (status: number) => {
  changeLoading();
  service
    .post(
      `/validateCustomers?status=${status}`,
      JSON.stringify({
        idList: tableInstance.value
          ?.getSelectionRows()
          .map((item: customer) => {
            return item.id;
          }),
      })
    )
    .then((res) => {
      ElMessage.success({ message: res.data.message });
      reload();
      changeLoading();
    })
    .catch((err) => {
      ElMessage.error({ message: err });
      changeLoading();
    });
};
//搜索框中的值
const search = ref<string>();

// 搜索框清空时触发事件
const clearSearch = () => {
  changeLoading();
  service
    .get("/customers")
    .then((res) => {
      set_tableData(res);
      changeLoading();
    })
    .catch((err) => {
      changeLoading();
      ElMessage.error(err.code);
    });
};

// 通过模糊查询用户
const searchCustomer = () => {
  if (search.value !== "") {
    changeLoading();
    service
      .get(`/customer/${search.value}`)
      .then((res: AxiosResponse) => {
        switch (res.data.code) {
          // case 404: tableData.value = new Array<customer>
          case undefined:
            set_tableData(res);
        }
        changeLoading();
      })
      .catch((err) => {
        // console.log(err.data);
        changeLoading();
        // ElMessage.error(err.data)
      });
  } else {
    clearSearch();
  }
};

const pre_src_list = ref<Array<string>>([]);
const pre_init_index = ref<number>();

// 更改图片预览的初始下标
const changeInitIndex = (iniInex: number) => {
  pre_init_index.value = iniInex;
};

const pageSize = ref<number>(30);
const pageSizeList = ref<Array<number>>([30, 50, 100]);
const currentPage = ref<number>();

// 监听当前页面页码，发生改变时滚动到表格最上方
watch(currentPage, (newValue, oldValue) => {
  // window.scrollTo(0, 0)
  tableInstance.value?.scrollTo(0, 0);
});

// 当前页数发生改变时触发事件
const sizeChange = () => {
  changeLoading();
  service
    .get(`/customers?pageSize=${pageSize.value}&is_valided=0`)
    .then((res: AxiosResponse) => {
      changeLoading();
      set_tableData(res);
    })
    .catch((err) => {
      changeLoading();
    });
};
// 当前页面页码改变时触发事件
const jumpPage = () => {
  changeLoading();
  service
    .get(
      `/customers?page=${currentPage.value}&pageSize=${pageSize.value}&is_valided=0`
    )
    .then((res) => {
      changeLoading();
      set_tableData(res);
    })
    .catch((err) => {
      changeLoading();
      ElMessage.error(err.code);
    });
};
// 刷新页面时请求一次数据
service
  .get("/customers?ex_is_valided=1")
  .then((res) => {
    set_tableData(res);
  })
  .catch((err) => {
    ElMessage.error(err.code);
  });

service.get("/classGeneralApi").then((res) => {
  classFilters.value = res.data.map((ele: classType) => {
    return {
      text: ele.class_name,
      value: ele.class_name,
    };
  });
});
</script>

<style lang="scss" scoped>
.el-message-box__message {
  white-space: pre-wrap;
}
.el-header {
  display: flex;
  margin-bottom: 0.5rem;
  height: min-content;
  padding: 0;
  text-align: left;
  justify-content: space-between;
  .el-input {
    width: 220px;
  }
}
</style>

<style lang="scss" scoped></style>
