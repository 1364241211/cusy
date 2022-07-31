import { compressAccurately, filetoDataURL } from "image-conversion";
import { ref } from "vue";

export async function useImageCompress(data: Blob) {
  const dataUrl = ref<string>();
  const size = ref<number>();
  const error = ref();
  let compressValue = null;
  const isImage = /image/.test(data.type);
  if (isImage && data.size > 1024 * 1024 * 2) {
    try {
      compressValue = await compressAccurately(data, 1024);
    } catch (err) {
      error.value = err;
    }
  }
  try {
    dataUrl.value = await filetoDataURL(
      compressValue === null ? data : compressValue
    );
  } catch (err) {
    error.value = err;
  }
  size.value = dataUrl.value?.length;
  dataUrl.value = dataUrl.value?.replace(/data:\w+\/\w+;base64,/, "");
  return { dataUrl, size, error };
}
