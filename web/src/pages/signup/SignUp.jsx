import { useSignUpMutation } from "./hooks/useSignUpMutation";
import { useForm } from "react-hook-form";
import { signUpSchema } from "./models";
import { yupResolver } from "@hookform/resolvers/yup";
import { Link, redirect, useNavigate } from "react-router-dom";
import { Helmet } from "react-helmet-async";
import { useSelector } from "react-redux";
import { getCookieByName } from "./../../utils";
import GlobalLoader from "../../components/globalLoader/GlobalLoader";

export function loader() {
  if (getCookieByName("user") !== "{}") {
    return redirect("/");
  }
  return null;
}
function SignUp() {
  const { userId } = useSelector((state) => state.user);
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({ resolver: yupResolver(signUpSchema) });
  const signUpMutation = useSignUpMutation();
  const onSubmit = async (data) => {
    await signUpMutation.mutateAsync(data);
    navigate("/signin");
  };
  return (
    <>
      {signUpMutation.isPending && <GlobalLoader />}
      <Helmet>
        <title>K1 - Регистрация</title>
        <meta
          name="description"
          content="Создайте аккаунт в сервисе анализа патентной активности компаний москвы"
        />
        <meta rel="canonical" href="/signup" />
      </Helmet>
      <main className="auth">
        <div className="container auth__container">
          <div className="title-h1 auth__title">
            Решение кейса “Сервис анализа патентной активности компаний Москвы”
          </div>
          <form
            className="form auth__form"
            onSubmit={handleSubmit(onSubmit)}
            noValidate
          >
            <h2 className="title-h3 form__title">РЕГИСТРАЦИЯ</h2>
            <label htmlFor="email" className="form__label form__input-email">
              <input
                type="email"
                name="email"
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
              htmlFor="username"
              className="form__label form__input-username"
            >
              <input
                type="text"
                name="username"
                id="username"
                className={
                  errors.username
                    ? "form__input form__input--error"
                    : "form__input"
                }
                placeholder="Имя пользователя"
                {...register("username")}
              />
              {errors.username && (
                <p className="form__error">{errors.username.message}</p>
              )}
            </label>

            <label
              htmlFor="password"
              className="form__label form__input-password"
            >
              <input
                type="password"
                name="password"
                className={
                  errors.password
                    ? "form__input form__input--error"
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
              disabled={signUpMutation.isPending}
            >
              {signUpMutation.isPending
                ? "Регистрируемся"
                : "Зарегистрироваться"}
            </button>
            <p className="form__text">
              Уже есть аккаунт?
              <Link to={"/signin"} className="form__link">
                Войти
              </Link>
            </p>
          </form>
        </div>
      </main>
    </>
  );
}

export default SignUp;
