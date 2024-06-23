import axios from "axios";


const signInInstance = axios.create({baseURL: import.meta.env.VITE_BASE_URL})


export async function signUp(data) {
    return (await signInInstance.post('/api/signup', data))
}


