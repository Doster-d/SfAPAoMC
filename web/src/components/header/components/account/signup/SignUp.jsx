import { useForm } from "react-hook-form";
import { signInSchema } from "./models";
import { yupResolver } from "@hookform/resolvers/yup";

function SignUp({ setIsRegistration, addNotification }) {
  const {
    register,
    setError,
    handleSubmit,
    formState: { errors },
  } = useForm({ resolver: yupResolver(signInSchema) });
  const onSubmit = async (data) => {
    addNotification(JSON.stringify(data), "good", 3000);
  };
  return (
    <form
      className="account__form"
      onSubmit={handleSubmit(onSubmit)}
      noValidate
    >
      <label htmlFor="username" className="account__label">
        Имя пользователя
        <input
          type="text"
          name="username"
          id="username"
          className={
            errors.username
              ? "account__input account__input--error"
              : "account__input"
          }
          placeholder="Имя пользователя"
          {...register("username")}
        />
        {errors.username && (
          <p className="account__error">{errors.username.message}</p>
        )}
      </label>
      <label htmlFor="email" className="account__label">
        Электронная почта
        <input
          type="email"
          name="email"
          className={
            errors.email
              ? "account__input account__input--error"
              : "account__input"
          }
          placeholder="Email"
          {...register("email")}
        />
        {errors.email && (
          <p className="account__error">{errors.email.message}</p>
        )}
      </label>
      <label htmlFor="password" className="account__label">
        Пароль
        <input
          type="password"
          name="password"
          className={
            errors.password
              ? "account__input account__input--error"
              : "account__input"
          }
          placeholder="Пароль"
          {...register("password")}
        />
        {errors.password && (
          <p className="account__error">{errors.password.message}</p>
        )}
      </label>
      <button className="account__btn" type="submit">
        Зарегистрироваться
      </button>
      <p className="account__text">
        Уже есть аккаунт?
        <button
          onClick={(e) => {
            e.preventDefault();
            setIsRegistration(false);
          }}
          className="account__link"
        >
          Войти
        </button>
      </p>
    </form>
  );
}

export default SignUp;
