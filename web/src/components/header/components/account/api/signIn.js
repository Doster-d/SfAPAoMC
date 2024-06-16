import axios, { Axios } from "axios";
import { BASE_URL } from "../../../../../const";


const signInInstance = axios.create({baseURL: BASE_URL})


export async function signIn(data) {
    return (await signInInstance.post('/api/signin', data))
}


