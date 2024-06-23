import axios from "axios";


const getFilesInstance = axios.create({baseURL: import.meta.env.VITE_BASE_URL})

export const getFiles = async ({pageParam}) => {
    return (await getFilesInstance.get(`/files/?page=${pageParam + 1}`)).data
}