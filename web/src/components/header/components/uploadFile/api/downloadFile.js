
import axios from "axios";
import { BASE_URL } from "../../../../../const";

const uploadFileInstance = axios.create({
  baseURL: BASE_URL,
  responseType: 'blob',

});

export async function downloadFile(fileId) {
  return await uploadFileInstance.get(`/api/download/${fileId}`);
}
