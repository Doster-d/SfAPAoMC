function SignIn({setIsRegistration}) {
  return (
    <form className="account__form">
      <label htmlFor="email" className="account__label">
        Электронная почта
        <input type="email" name="email" id="email" className="account__input" placeholder="Email" />
      </label>
      <label htmlFor="password" className="account__label">
        Пароль
        <input type="password" id="password" name="password" className="account__input" placeholder="Пароль" />
      </label>
      <button className="account__btn" type="submit">Вход</button>
      <p className="account__text">Нет аккаунта? <button           onClick={(e) => {
            e.preventDefault();
            setIsRegistration(true)
          }} className="account__link">Регистрация</button></p>
    </form>
  );
}

export default SignIn;
