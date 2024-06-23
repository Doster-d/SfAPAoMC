import axios from "axios";

const getFileInfoInstance = axios.create({ baseURL: import.meta.env.VITE_BASE_URL });

export async function getFileInfoById(fileId) {
  return await getFileInfoInstance.get(`/api/information/${fileId}`);
}

