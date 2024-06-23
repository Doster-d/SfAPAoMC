import { useForm } from "react-hook-form";
import { signInSchema } from "./models";
import { yupResolver } from "@hookform/resolvers/yup";
import { useSignInMutation } from "./hooks/useSignInMutation";
import { Link, redirect, useNavigate } from "react-router-dom";
import { Helmet } from "react-helmet-async";
import { getCookieByName } from "../../utils";

export function loader() {
  if (getCookieByName("user") !== "{}") {
    return redirect("/");
  }
  return null;
}

function SignIn() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({ resolver: yupResolver(signInSchema) });
  const signInMutation = useSignInMutation();
  const navigate = useNavigate();
  const onSubmit = async (data) => {
    await signInMutation.mutateAsync(data);
    navigate("/");
  };
  return (
    <>
      {" "}
      <Helmet>
        <title>K1 - Авторизация</title>
        <meta
          name="description"
          content="Войдите в аккаунт в сервисе анализа патентной активности компаний москвы"
        />
        <meta rel="canonical" href="/signin" />
      </Helmet>
      <main className="auth">
        <div className="container auth__container">
          <div className="title-h1 auth__title">
            {" "}
            Решение кейса “Сервис анализа патентной активности компаний Москвы”
          </div>
          <form
            className="form auth__form"
            onSubmit={handleSubmit(onSubmit)}
            noValidate
          >
            <h2 className="title-h3 form__title">ВХОД</h2>

            <label htmlFor="email" className="form__label form__input-email">
              <input
                type="email"
                name="email"
                id="email"
                className={
                  errors.email
                    ? "form__input form__input--error"
                    : "form__input"
                }
                placeholder="Email"
                {...register("email")}
              />
              {errors.email && (
                <p className="form__error">{errors.email.message}</p>
              )}
            </label>
            <label
              htmlFor="password"
              className="form__label form__input-password"
            >
              <input
                type="password"
                id="password"
                name="password"
                className={
                  errors.password
                    ? "form__input account__input--error"
                    : "form__input"
                }
                placeholder="Пароль"
                {...register("password")}
              />
              {errors.password && (
                <p className="form__error">{errors.password.message}</p>
              )}
            </label>
            <button
              className="form__btn"
              type="submit"
              disabled={signInMutation.isPending}
            >
              {signInMutation.isPending ? "Входим" : "Вход"}
            </button>
            <p className="form__text">
              Нет аккаунта?{" "}
              <Link to={"/signup"} className="form__link">
                Регистрация
              </Link>
            </p>
          </form>
        </div>
      </main>
    </>
  );
}

export default SignIn;
