import * as yup from "yup";


export const signInSchema = yup.object().shape({
    email: yup.string().email("Неправильный формат").required("Укажите почту"),
    password: yup.string().required("Password is required"),
})