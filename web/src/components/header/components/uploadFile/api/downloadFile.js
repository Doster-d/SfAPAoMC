
import axios from "axios";


const uploadFileInstance = axios.create({
  baseURL: import.meta.env.VITE_BASE_URL,
  responseType: 'blob',

});

export async function downloadFile(fileId) {
  return await uploadFileInstance.get(`/api/download/${fileId}`);
}
