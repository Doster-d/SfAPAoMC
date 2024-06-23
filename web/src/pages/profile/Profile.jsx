import pfp from "./.././../assets/images/profile/profile_pfp.svg";
import logout from "./.././../assets/images/profile/profile_logout.svg";
import { useDispatch, useSelector } from "react-redux";
import "./style.scss";
import { redirect, useNavigate } from "react-router-dom";
import { addNewNotification } from "../../setup/store/reducers/notificationSlice";
import { NOTIFICATION_GOOD } from "../../const";
import { eraseCookie, getCookieByName } from "../../utils";
import { clearUserData } from "../../setup/store/reducers/userSlice";
import { Helmet } from "react-helmet-async";

export function loader() {
  if (getCookieByName("user") === "{}") {
    return redirect("/");
  }
  return null;
}
function Profile() {
  const { username } = useSelector((state) => state.user);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const logOutHandle = () => {
    dispatch(clearUserData());
    eraseCookie('user')
  };
  return (
    <>
      <Helmet>
        <title>K1 - Личный кабинет</title>
        <meta
          name="description"
          content="Ваш личный кабинет в сервисе анализа патентной активности компаний москвы"
        />
        <meta rel="canonical" href="/profile" />
      </Helmet>
      <main className="profile">
        <div className="container profile__container">
          <section className="profile__upper">
            <h1 className="title-h1 profile__title">
              Решение кейса “Сервис анализа патентной активности компаний
              Москвы”
            </h1>
            <div className="profile__general-info">
              <picture className="image-wrapper profile__pfp">
                <img className="image-wrapper__image" src={pfp} alt="" />
              </picture>
              <button
                onClick={(e) => {
                  e.preventDefault();
                  logOutHandle();
                  dispatch(
                    addNewNotification({
                      message: "Вы вышли из аккаунта",
                      type: NOTIFICATION_GOOD,
                      duration: 5000,
                    })
                  );
                  navigate("/signin");
                }}
                className="profile__logout-wrapper"
              >
                <p className="profile__logout">ВЫЙТИ</p>
                <img src={logout} alt="" className="profile__logout" />
              </button>
            </div>
          </section>
          <section className="profile__additional-info">
            <div className="profile__addition-info-item">
              <p className="profile__item-name">Имя пользователя</p>
              <p className="profile__item-info">{username}</p>
            </div>
            <div className="profile__addition-info-item">
              <p className="profile__item-name">Электронная почта</p>
              <p className="profile__item-info">example@example.com</p>
            </div>
          </section>
        </div>
      </main>
    </>
  );
}

export default Profile;
