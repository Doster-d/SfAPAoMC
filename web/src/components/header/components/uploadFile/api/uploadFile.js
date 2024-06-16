import axios from "axios";
import { BASE_URL } from "../../../../../const";

const uploadFileInstance = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "multipart/form-data" },
});

export async function uploadFile(file, accessToken, userId) {
  const formData = new FormData();
  formData.append("file", file);
  console.log(file, formData);
  return await uploadFileInstance.post(`/api/upload/${userId}`, formData, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
}
