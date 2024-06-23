import axios from "axios";

const getGeneralInfoInstance = axios.create({
  baseURL: import.meta.env.VITE_BASE_URL,
});

export async function getGeneralInfo() {
  return await getGeneralInfoInstance.get("/api/information");
}
