import axios from "axios";

const uploadFileInstance = axios.create({
  baseURL: import.meta.env.VITE_BASE_URL,
  headers: { "Content-Type": "multipart/form-data" },
  onUploadProgress: function (progressEvent) {
    console.log(progressEvent);
  },
});

export async function uploadFile(file, accessToken, userId) {
  const formData = new FormData();
  formData.append("file", file);
  console.log(file, formData);
  return await uploadFileInstance.post(`/api/upload_tin/${userId}`, formData, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
}
