import axios from "axios";
import { BASE_URL } from "../../../const";

const getGeneralInfoInstance = axios.create({baseURL:BASE_URL})

export async function getGeneralInfo() {
    return (await getGeneralInfoInstance.get('/api/information'))
}