import axios from "axios";
import { BASE_URL } from "../../../const";

const getFileInfoInstance = axios.create({ baseURL: BASE_URL });

export async function getFileInfoById(fileId) {
  return await getFileInfoInstance.get(`/api/information/${fileId}`);
}

