import axios from "axios";
import { BASE_URL } from "../../../../../const";


const signInInstance = axios.create({baseURL: BASE_URL})


export async function signUp(data) {
    return (await signInInstance.post('/api/signin', data))
}


