import axios, { Axios } from "axios";


const signInInstance = axios.create({baseURL: import.meta.env.VITE_BASE_URL})


export async function signIn(data) {
    return (await signInInstance.post('/api/signin', data))
}


