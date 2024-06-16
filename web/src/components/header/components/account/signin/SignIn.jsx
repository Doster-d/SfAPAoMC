import { useForm } from "react-hook-form";
import { signInSchema } from "./models";
import { yupResolver } from "@hookform/resolvers/yup";
import { useSignInMutation } from "../hooks/useSignInMutation";

function SignIn({ setIsRegistration, addNotification }) {
  const {
    register,
    setError,
    handleSubmit,
    formState: { errors },
  } = useForm({ resolver: yupResolver(signInSchema) });
  const signInMutation = useSignInMutation()
  const onSubmit = async (data) => {
    addNotification(JSON.stringify(data), 'good', 3000)
    await signInMutation.mutateAsync(data)
  };
  return (
    <form
      className="account__form"
      onSubmit={handleSubmit(onSubmit)}
      noValidate
    >
      <label htmlFor="email" className="account__label">
        Электронная почта
        <input
          type="email"
          name="email"
          id="email"
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
          id="password"
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
        Вход
      </button>
      <p className="account__text">
        Нет аккаунта?{" "}
        <button
          onClick={(e) => {
            e.preventDefault();
            setIsRegistration(true);
          }}
          className="account__link"
        >
          Регистрация
        </button>
      </p>
    </form>
  );
}

export default SignIn;
