
import axios from "axios";
import { BASE_URL } from "../../../../../const";

const uploadFileInstance = axios.create({
  baseURL: BASE_URL,
  responseType: 'blob'
});

export async function downloadFile(accessToken, userId, fileId) {
  return await uploadFileInstance.get(`/api/download/${userId}/${fileId}`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
}
