import { ref } from "vue";
import service from "../util/api";
import { customer, ListMessage, METHOD, resMessage } from "../types";
import { AxiosError, AxiosRequestHeaders, AxiosResponse } from "axios";

export async function useRequest(
  url: string,
  method: METHOD = METHOD.GET,
  data?: string,
  BlobFile?: boolean,
  headers?: AxiosRequestHeaders
) {
  const res = ref<
    resMessage | ListMessage<customer> | Blob | undefined | null
  >();
  const error = ref<string | undefined | null>(null);
  const resType = BlobFile ? "blob" : "json";
  switch (method) {
    case METHOD.GET:
      await service
        .get(url, { responseType: resType, headers: headers })
        .then((resp: AxiosResponse) => {
          res.value = resp.data;
        })
        .catch((err: AxiosError) => {
          error.value = err.message;
        });
      break;
    case METHOD.POST:
      await service
        .post(url, data, { responseType: resType, headers: headers })
        .then((resp: AxiosResponse) => {
          res.value = resp.data;
        })
        .catch((err: AxiosError) => {
          error.value = err.message;
        });
      break;
    case METHOD.DELETE:
      await service
        .post(url, data, { responseType: resType, headers: headers })
        .then((resp: AxiosResponse) => {
          res.value = resp.data;
        })
        .catch((err: AxiosError) => {
          error.value = err.message;
        });
      break;
    case METHOD.UPDATE:
      await service
        .post(url, data, { responseType: resType, headers: headers })
        .then((resp: AxiosResponse) => {
          res.value = resp.data;
        })
        .catch((err: AxiosError) => {
          error.value = err.message;
        });
      break;
  }
  return { res, error };
}
