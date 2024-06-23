import { useForm } from "react-hook-form";
import { signUpSchema } from "./models";
import { yupResolver } from "@hookform/resolvers/yup";
import { useSignUpMutation } from "../hooks/useSignUpMutation";

function SignUp({ setIsRegistration }) {
  const {
    register,
    setError,
    handleSubmit,
    formState: { errors },
  } = useForm({ resolver: yupResolver(signUpSchema) });
  const signUpMutation = useSignUpMutation();
  const onSubmit = async (data) => {
    await signUpMutation.mutateAsync(data);
    if (signUpMutation.isSuccess) {
      setIsRegistration(false);
    }
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
      <button
        className="account__btn"
        type="submit"
        disabled={signUpMutation.isPending}
      >
        {signUpMutation.isPending ? "Регистрируемся" : "Зарегистрироваться"}
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
