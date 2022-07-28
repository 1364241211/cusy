<template>
  <el-config-provider :locale="locale">
    <div>
      <el-header>
        <el-button-group>
          <el-button
            type="danger"
            :disabled="buttonEnable"
            :icon="CircleClose"
            @click="deleteClasses"
            >删除 ({{ buttonEnable ? 0 : selectionRows }})</el-button
          >
          <el-button type="primary" @click="addClass"> 添加班级 </el-button>
        </el-button-group>
        <!---<el-input
        v-model="search"
        placeholder="请输入查询关键字"
        @input="searchCustomer"
        clearable
        :prefix-icon="Search"
        @clear="clearSearch"
      />--->
      </el-header>
      <el-table
        ref="tableInstance"
        :data="tableData"
        @selection-change="columnSelect"
      >
        <el-table-column type="selection"></el-table-column>
        <el-table-column
          label="id"
          prop="id"
          align="center"
          width="70px"
        ></el-table-column>
        <el-table-column
          label="班级批次"
          prop="class_name"
          align="center"
        ></el-table-column>
        <el-table-column
          label="班级组"
          prop="class_group"
          align="center"
        ></el-table-column>
      </el-table>
      <el-dialog
        v-model="addDialog"
        destroy-on-close
        append-to-body
        close-on-press-escape
        center
        @close="reload()"
      >
        <template #header>
          <h4>添加班级</h4>
        </template>
        <template #default>
          <component :is="AddClass"></component>
        </template>
      </el-dialog>
    </div>
  </el-config-provider>
</template>

<script lang="ts" setup>
import { ref, reactive, inject } from "vue";
import { ElTable, ElMessage } from "element-plus";
import type { TableColumnCtx } from "element-plus/es/components/table/src/table-column/defaults";
import { CircleClose } from "@element-plus/icons";
import type { AxiosResponse } from "axios";
import zhCn from "element-plus/lib/locale/lang/zh-cn";

import type { classType } from "../types/index";
import service from "../util/api";
import AddClass from "./AddClass.vue";

const locale = ref(zhCn);
const tableData = ref<Array<classType>>([]);
const tableInstance = ref<InstanceType<typeof ElTable>>();
const classFilters = ref<Array<{ text: string; value: string }>>([]);
const buttonEnable = ref(true);
const selectionRows = ref(0);
const addDialog = ref(false);

// 关闭时 刷新组件
const reload = inject("reload", Function, true);

// 获取选择的表格数据
const columnSelect = () => {
  if (tableInstance.value?.getSelectionRows().length !== 0) {
    buttonEnable.value = false;
    selectionRows.value = tableInstance.value?.getSelectionRows().length;
  } else {
    buttonEnable.value = true;
  }
};
// 班级过滤方法
//const calssFiltersMethod = (
//  value: string,
//  row: classType,
//  column: TableColumnCtx<classType>
//) => {
//  const property = column["property"] as string;
//  return row[property as keyof classType] === value;
//};
// 重制班级过滤
//const restClassFilter = () => {
// tableInstance.value?.clearFilter(["class_name"]);
//};

// 点击删除按钮删除班级
const deleteClasses = () => {
  console.log(tableInstance.value?.getSelectionRows());
  service
    .delete("/classes", {
      data: JSON.stringify({
        idList: tableInstance.value
          ?.getSelectionRows()
          .map((ele: classType) => {
            return ele.id;
          }),
      }),
    })
    .then((res) => {
      switch (res.data.code) {
        case 200:
          {
            ElMessage.success("删除成功");
            reload();
          }
          break;
        case 404:
          ElMessage.error(res.data.message);
          break;
      }
    })
    .catch((err) => {
      ElMessage.error("出现未知错误，删除失败");
    });
};

// 点击增加按钮添加班级
const addClass = () => {
  addDialog.value = true;
};

// 获取数据并渲染到表格
service.get("/classGeneralApi").then((res: AxiosResponse) => {
  tableData.value = res.data.map(
    (ele: { id: number; class_name: string; class_group: number }) => {
      return {
        id: ele.id,
        class_name: ele.class_name,
        class_group: ele.class_group,
      };
    }
  );
  classFilters.value = res.data.map(
    (ele: { id: number; class_name: string; class_group: number }) => {
      return {
        text: ele.class_name,
        value: ele.id,
      };
    }
  );
});
</script>

<style lang="scss" scoped>
.el-header {
  display: flex;
  margin-bottom: 0.5rem;
  height: min-content;
  padding: 0;
  text-align: left;
  justify-content: space-between;
}
</style>
