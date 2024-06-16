import * as yup from "yup";


export const signInSchema = yup.object().shape({
    username: yup.string().required("Укажите имя"),
    email: yup.string().email("Неправильный формат").required("Укажите почту"),
    password: yup.string().required("Требуется пароль"),
})