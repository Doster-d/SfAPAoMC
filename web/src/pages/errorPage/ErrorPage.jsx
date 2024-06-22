import { useEffect } from "react";
import errorImg from "./../../assets/images/error/404.svg";
import "./style.scss";
function ErrorPage() {
  useEffect(() => {
    document.body.style =
      "  background: linear-gradient(90.00deg, rgb(240, 147, 251),rgb(245, 87, 108) 100%);";
    return () => {
      document.body.style = "";
    };
  }, []);
  return (
    <main className="error-page">
      <p className="error-page__text">Упс</p>
      <p className="error-page__central-text">
        4 <img src={errorImg} alt="Error" className="error-page__image" /> 4
      </p>
      <p className="error-page__text">Что-то пошло не по плану</p>
    </main>
  );
}

export default ErrorPage;
