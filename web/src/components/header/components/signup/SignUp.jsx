function SignUp({ setIsRegistration }) {
  return (
    <form className="account__form">
      <label htmlFor="username" className="account__label">
        Имя пользователя
        <input
          type="text"
          name="username"
          id="username"
          className="account__input"
          placeholder="Имя пользователя"
        />
      </label>
      <label htmlFor="" className="account__label">
        Электронная почта
        <input
          type="email"
          name="email"
          className="account__input"
          placeholder="Email"
        />
      </label>
      <label htmlFor="" className="account__label">
        Пароль
        <input
          type="password"
          name="password"
          className="account__input"
          placeholder="Пароль"
        />
      </label>
      <button className="account__btn" type="submit">
        Зарегистрироваться
      </button>
      <p className="account__text">
        Уже есть аккаунт? 
        <button
          onClick={(e) => {
            e.preventDefault();
            setIsRegistration(false)
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
