<template>
  <div>
    <el-config-provider :locale="locale">
      <el-header>
        <el-button-group>
          <el-button
            type="warning"
            :disabled="buttonEnable"
            :icon="CircleClose"
            @click="moderateUsers(2)"
            >驳回 ({{ buttonEnable ? 0 : selectionRows }})</el-button
          >
          <el-tooltip
            content="点击后<strong style='color:red'><i>使用新生导入模版<i></strong>导出<strong style='color:red'><i>当前页面<i></strong>的数据"
            raw-content
          >
            <el-button
              type="primary"
              :icon="Document"
              @click="exportPage"
              class="button-transion"
              >单页导出(新生导入模版)
            </el-button></el-tooltip
          >
          <el-tooltip
            content="点击后<strong style='color:red'><i>使用新生导入模版<i></strong>导出<strong style='color:red'><i>所有页面<i></strong>的数据"
            raw-content
          >
            <el-button
              type="primary"
              :icon="Files"
              @click="exportAll"
              class="button-transion"
              >全部导出(新生导入模版)
            </el-button></el-tooltip
          >
          <el-tooltip
            content="点击后<strong style='color:red'><i>使用人脸识别模版<i></strong>导出<strong style='color:red'><i>当前页面<i></strong>的数据"
            raw-content
          >
            <el-button
              type="success"
              color="#626aef"
              :icon="Document"
              @click="exportMTPage"
              class="button-transion"
              >单页导出(人脸识别模版)
            </el-button></el-tooltip
          >
          <el-tooltip
            content="点击后<strong style='color:red'><i>使用人脸识别模版<i></strong>导出<strong style='color:red'><i>所有页面<i></strong>的数据"
            raw-content
          >
            <el-button
              type="success"
              color="#626aef"
              :icon="Files"
              @click="exportMTAll"
              class="button-transion"
              >全部导出(人脸识别模版)
            </el-button></el-tooltip
          >
          <el-tooltip
            content="点击后导出所有图片<strong style='color:red'><i>文件内容过大，请耐心等待，请勿刷新页面!<i></strong>的数据"
            raw-content
          >
            <el-button
              type="danger"
              :icon="Picture"
              @click="exportAvatar"
              :loading="exportAvatarLoding"
              >导出所有图片
            </el-button></el-tooltip
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
        @selection-change="columnSelect"
        border
        stripe
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
          width="100"
          align="center"
        ></el-table-column>
        <el-table-column prop="customer_photo" label="学生照片" align="center">
          <template #default="scope">
            <div
              style="
                display: flex;
                align-items: center;
                justify-content: center;
              "
            >
              <el-image
                :src="'/static/avatar/' + scope.row.customer_photo"
                style="height: 100px; width: 80px"
                fit="cover"
                :lazy="true"
                :preview-src-list="pre_src_list"
                :preview-teleported="true"
                :initial-index="pre_init_index"
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
          :filters="classFilters"
          :filter-method="calssFiltersMethod"
        ></el-table-column>
        <el-table-column
          prop="customer_logtime"
          label="学生登记时间"
          align="center"
        ></el-table-column>
        <el-table-column align="center" label="操作">
          <template #default="tail">
            <el-button-group>
              <!----<div class="button-groups">--->
              <el-button
                type="primary"
                size="small"
                :icon="Edit"
                @click="updateCustomer(tail.$index)"
                >修改</el-button
              >
              <el-button
                type="danger"
                size="small"
                :icon="Delete"
                @click="deleteCustomer(tail.$index)"
                >删除</el-button
              >
              <!----<el-button
              type="warning"
              @click="rejectCustomer(tail.$index)"
              size="small"
            >
              驳回
            </el-button>--->
              <!---</div>--->
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        v-model:page-sizes="pageSizeList"
        v-model:total="pagnation.count"
        layout="total,prev, pager, next,jumper,sizes"
        background
        @size-change="sizeChange"
        @current-change="jumpPage"
      />
      <el-drawer
        title="修改"
        v-model="drawer"
        direction="ltr"
        size="45%"
        @close="destroyCom"
      >
        <component
          v-if="isAlive"
          :is="asynComp"
          :itemProps="item_Props.data"
        ></component>
      </el-drawer>
    </el-config-provider>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, defineAsyncComponent, inject, onMounted } from "vue";
import { ElMessage, ElMessageBox, ElTable } from "element-plus";
import type { TableColumnCtx } from "element-plus/es/components/table/src/table-column/defaults";
import zhCn from "element-plus/lib/locale/lang/zh-cn";

import {
  Delete,
  Edit,
  Search,
  CircleClose,
  Files,
  Document,
  Picture,
} from "@element-plus/icons";

import {
  classType,
  customer,
  ListMessage,
  resMessage,
  METHOD,
  pagnationData,
} from "../types/index";
import service from "../util/api";
import { useRequest } from "../hooks/useReqest";

const exportAvatarLoding = ref(false);
const locale = zhCn;
const buttonEnable = ref(true);
const selectionRows = ref(0);
const isAlive = ref(false);
const destroyCom = () => {
  isAlive.value = false;
};
const reload = inject("reload", Function, true);
const classFilters = ref<Array<{ text: string; value: string }>>([]);

const pagnation = reactive<pagnationData>({
  count: 0,
  next: "null",
  previous: "null",
});
const tableLoading = ref<boolean>(false);
const changeLoading = (): void => {
  tableLoading.value = !tableLoading.value;
};
const tableData = ref<Array<customer>>();
const tableInstance = ref<InstanceType<typeof ElTable>>();

// 班级过滤方法
const calssFiltersMethod = (
  value: string,
  row: customer,
  column: TableColumnCtx<customer>
) => {
  const property = column["property"] as string;
  console.log(value);
  console.log(row);
  console.log(column);
  return row[property as keyof customer] === value;
};

// 重制班级过滤
const restClassFilter = () => {
  tableInstance.value?.clearFilter(["class_name"]);
};

// 设置通过传递的response设置表格数据tableData
const set_tableData = (res: ListMessage<customer>) => {
  pagnation.count = res.count as number;
  pagnation.next = res.next as string;
  pagnation.previous = res.previous as string;
  tableData.value = res.results;
  // 清空预览图片列表中的元素
  pre_src_list.value.length = 0;
  tableData.value!.forEach((ele: customer) => {
    pre_src_list.value.push(
      `${import.meta.env.VITE_APP_STATIC_URL}/static/avatar/${
        ele.customer_photo
      }`.trim()
    );
  });
};

// 获取选择的表格数据
const columnSelect = () => {
  if (tableInstance.value?.getSelectionRows().length !== 0) {
    buttonEnable.value = false;
    selectionRows.value = tableInstance.value?.getSelectionRows().length;
  } else {
    buttonEnable.value = true;
  }
};

// 为按钮组添加点击事件
// status :1 通过
// status :2 驳回
const moderateUsers = async (status: number) => {
  changeLoading();
  const { res, error } = await useRequest(
    `/validateCustomers?status=${status}`,
    METHOD.POST,
    JSON.stringify({
      idList: tableInstance.value?.getSelectionRows().map((item: customer) => {
        return item.id;
      }),
    })
  );
  if (res.value) {
    ElMessage.success({ message: (res.value as resMessage).message });
    reload();
    changeLoading();
  } else if (error.value) {
    changeLoading();
  }
};
const search = ref<string>();
const pre_src_list = ref<Array<string>>([]);
const pre_init_index = ref<number>();

// 更改图片预览的初始下标
const changeInitIndex = (iniInex: number) => {
  pre_init_index.value = iniInex;
};

const pageSize = ref<number>(100);
const pageSizeList = ref<Array<number>>([100, 200, 300]);
const currentPage = ref<number>();

// 监听当前页面页码，发生改变时滚动到表格最上方
// watch(currentPage, (newValue, oldValue) => {
// window.scrollTo(0, 0)
// tableInstance.value?.scrollTo(0, 0);
//});

// 搜索框清空时触发事件
const clearSearch = async () => {
  changeLoading();
  const { res, error } = await useRequest("/customers", METHOD.GET);
  if (res.value) {
    set_tableData(res.value as ListMessage<customer>);
    changeLoading();
  } else if (error.value) {
    changeLoading();
    ElMessage.error(error.value);
  }
};

// 当前页数发生改变时触发事件
const sizeChange = async () => {
  changeLoading();
  const { res, error } = await useRequest(
    `/customers?pageSize=${pageSize.value}`
  );
  if (res.value) {
    changeLoading();
    set_tableData(res.value as ListMessage<customer>);
  } else if (error.value) {
    changeLoading();
  }
};

// 当前页面页码改变时触发事件
const jumpPage = async () => {
  changeLoading();
  const { res, error } = await useRequest(
    `/customers?page=${currentPage.value}&pageSize=${pageSize.value}`
  );
  if (res.value) {
    changeLoading();
    set_tableData(res.value as ListMessage<customer>);
  } else if (error.value) {
    changeLoading();
    ElMessage.error(error.value);
  }
};

// 通过模糊查询用户
const searchCustomer = async () => {
  if (search.value !== "") {
    changeLoading();
    const { res, error } = await useRequest(`/customer/${search.value}`);
    if (res.value) {
      set_tableData(res.value as ListMessage<customer>);
      changeLoading();
    } else if (error.value) {
      changeLoading();
    }
  } else {
    await clearSearch();
  }
};

// 删除单个用户
const deleteCustomer = (index: number) => {
  const warningInfo = `确定删除该用户吗？（注意该操作不可逆）\n姓名:${
    tableData.value?.at(index)?.customer_name
  }\n用户身份证: ${tableData.value?.at(index)?.customer_id}`;
  ElMessageBox.confirm(warningInfo, "警告!", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "error",
  })
    .then(() => {
      const id: number | undefined = tableData.value?.at(index)?.id;
      if (id !== undefined) {
        service.delete(`/customers?id=${id}`).then((res) => {
          switch (res.data.code) {
            case 200:
              {
                ElMessage.success(res.data.message);
                reload();
              }
              break;
            case 404:
              ElMessage.error(res.data.message);
              break;
          }
        });
      }
    })
    .catch(() => {});
};
const drawer = ref(false);
let item_Props = reactive({
  data: {
    id: 0,
    customer_name: "",
    customer_id: "",
    customer_photo: "",
    parent_phone: "",
    customer_logtime: "",
    class_id: 0,
    class_name: "",
  } as customer,
});
const asynComp = defineAsyncComponent({
  loader: () => import("./AddToCustomer.vue"),
  delay: 200,
});

// 更新用户
const updateCustomer = (index: number) => {
  const columnData = tableData.value?.at(index);
  item_Props["data"] = columnData as customer;
  drawer.value = !drawer.value;
  isAlive.value = true;
};

// 导出单页数据
const exportPage = async () => {
  let cPage = 1;
  if (currentPage.value) {
    cPage = currentPage.value;
  }
  const { res, error } = await useRequest(
    `/exportAll?page=${cPage}&pageSize=${pageSize.value}`,
    METHOD.GET,
    undefined,
    true
  );
  if (res.value) {
    const bl = new Blob([res.value as Blob], {
      type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    });
    const a = document.createElement("a");
    a.href = window.URL.createObjectURL(bl);
    a.download = `新生导入模版(${cPage}).xlsx`;
    a.click();
    window.URL.revokeObjectURL(a.href);
  } else if (error.value) {
    ElMessage.error("导出失败");
  }
};

// 将数据全部导出为excel
const exportAll = async () => {
  const { res, error } = await useRequest(
    "/exportAll",
    METHOD.POST,
    undefined,
    true
  );
  if (res.value) {
    const bl = new Blob([res.value as Blob], {
      type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    });
    const a = document.createElement("a");
    a.href = window.URL.createObjectURL(bl);
    a.download = "新生导入模版(全).xlsx";
    a.click();
    window.URL.revokeObjectURL(a.href);
  } else if (error.value) {
    ElMessage.error("导出失败");
  }
};

// 导出人脸识别模版单页数据
const exportMTPage = async () => {
  let cPage = 1;
  if (currentPage.value) {
    cPage = currentPage.value;
  }
  const { res, error } = await useRequest(
    `/exportMTAll?page=${cPage}&pageSize=${pageSize.value}`,
    METHOD.GET,
    undefined,
    true
  );
  if (res.value) {
    const bl = new Blob([res.value as Blob], {
      type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    });
    const a = document.createElement("a");
    a.href = window.URL.createObjectURL(bl);
    a.download = `人脸识别模版(${cPage}).xlsx`;
    a.click();
    window.URL.revokeObjectURL(a.href);
  } else if (error.value) {
    ElMessage.error("导出失败");
  }
};

// 将人脸识别模版数据全部导出为excel
const exportMTAll = async () => {
  const { res, error } = await useRequest(
    "/exportMTAll",
    METHOD.POST,
    undefined,
    true
  );
  if (res.value) {
    const bl = new Blob([res.value as Blob], {
      type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    });
    const a = document.createElement("a");
    a.href = window.URL.createObjectURL(bl);
    a.download = "人脸识别模版(全).xlsx";
    a.click();
    window.URL.revokeObjectURL(a.href);
  } else if (error.value) {
    ElMessage.error("导出失败");
  }
};

// 分片下载用户头像
const exportAvatar = async () => {
  exportAvatarLoding.value = true;
  const { res: f1, error: f2 } = await useRequest("/exportAvatar", METHOD.GET);
  let fileDataList: Array<Blob> = [];
  let fileLength: number = 0;
  if (f1.value) {
    fileLength = (f1.value as resMessage).info as number;
  } else if (f2.value) {
    ElMessage.error(f2.value);
    return;
  }
  console.log(f2);
  let taskQueen = [];
  const Q: number = Math.floor(fileLength / 10);
  for (let i = 0; i < 10; i++) {
    if (i == 9) taskQueen.push(serq("/exportAvatar", i * Q, fileLength));
    else taskQueen.push(serq("/exportAvatar", i * Q, (i + 1) * Q - 1));
  }
  await Promise.all(taskQueen)
    .then((results) => {
      results.forEach((res) => {
        console.log(res.data);
        fileDataList.push(res.data);
      });
    })
    .catch((err) => {
      ElMessage.error(err);
      exportAvatarLoding.value = false;
    });
  const file = new Blob(fileDataList);
  const a = document.createElement("a");
  a.href = window.URL.createObjectURL(file);
  a.download = "avatar.zip";
  a.click();
  window.URL.revokeObjectURL(a.href);
  exportAvatarLoding.value = false;
};

const serq = (url: string, start: number, end: number) => {
  const headers = {
    "transfer-encoding": "chunked",
    Range: `bytes=${start}-${end}`,
  };
  console.log(headers);
  const s = service.post(url, undefined, {
    responseType: "blob",
    headers: headers,
  });
  return s;
};

// 刷新页面时请求一次数据
onMounted(async () => {
  const { res, error } = await useRequest("/customers");
  if (res.value) {
    set_tableData(res.value as ListMessage<customer>);
  } else if (error.value) {
    ElMessage.error(error.value);
  }

  service.get("/classGeneralApi").then((res) => {
    classFilters.value = res.data.map((ele: classType) => {
      return {
        text: ele.class_name,
        value: ele.class_name,
      };
    });
  });
});
</script>

<style lang="scss" scoped>
.search-header {
  display: flex;
  width: 100%;
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
.el-message-box__message {
  white-space: pre-wrap;
}
.button-groups {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-evenly;
  .el-button + .el-button {
    margin: 0;
  }
}
.button-transion {
  :deep(span) {
    display: none;
  }
}
.button-transion:hover {
  overflow: hidden;
  :deep(span) {
    display: inline-block;
  }
}
</style>
