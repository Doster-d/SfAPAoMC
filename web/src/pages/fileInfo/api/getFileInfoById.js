import axios from "axios";
import { BASE_URL } from "../../../const";

const getFileInfoInstance = axios.create({ baseURL: BASE_URL });

export async function getFileInfoById(accessToken, userId, fileId) {
    console.log(fileId, userId, accessToken);
  return await getFileInfoInstance.get(`/api/information/${userId}/${fileId}`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
}

