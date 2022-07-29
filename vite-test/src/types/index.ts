// 用户结构
export interface customer {
  id: number;
  customer_id: string;
  customer_name: string;
  customer_photo: string;
  parent_phone: string;
  class_name: string;
  class_id: number;
  customer_logtime: string;
  is_valided: string;
}
// 分页数据结构
export interface pagnationData {
  count: number;
  next: string;
  previous: string;
}
// 班级组结构
export interface classGroup {
  group_id: number;
  group_name: string;
  groups: Array<classType>;
}
// 班级数据结构
export interface classType {
  id: number;
  class_group: number;
  class_name: string;
}
// 列表数据结构
export interface tabType {
  title: string;
}
// 网络请求方法枚举
export enum METHOD {
  GET = "GET",
  POST = "POST",
  UPDATE = "UPDATE",
  DELETE = "DELETE",
}
// 网络响应信息
interface messageInfo {
  [props: string]: any;
}
// 网路响应格式
export interface resMessage {
  code?: number;
  message?: string;
  status?: string;
  info?: string | Array<any> | number;
}
