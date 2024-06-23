import * as yup from "yup";

export const signUpSchema = yup.object().shape({
  email: yup.string().email("Неправильный формат").required("Укажите почту"),
  username: yup.string().required("Укажите имя"),
  password: yup.string().required("Требуется пароль"),
});
