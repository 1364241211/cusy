import axios, { AxiosRequestConfig } from "axios";
import cookies from "../cookies/index";

let csrf_token: string = cookies.cookies.get("csrftoken");
const service = axios.create({
  baseURL: "http://192.168.2.103:8000/api",
  timeout: 60000,
  withCredentials: true,
  headers: {
    "content-type": "application/json",
    "x-request-with": "XMLHttpRequest",
    csrf_token: csrf_token,
  },
});

service.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    if (!config?.headers) {
      throw new Error(
        `Expected 'config' and 'config.headers' not to be undefined`
      );
    }
    if (cookies.cookies.isKey("token")) {
      config.headers.Authorization = `Bearer ${cookies.cookies.get("token")}`;
    } else {
      // router.push("/admin/login")
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default service;
