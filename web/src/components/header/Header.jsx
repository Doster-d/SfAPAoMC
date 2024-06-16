import { Link } from "react-router-dom";
import logo from "./../../assets/images/mainpage/header_logo.svg";
import "./style.scss";
import { useToggle } from "../../hooks/useToggle";
import UploadFile from "./components/uploadFile/UploadFile";
import NotificationContainer from "../notification/Notification";
import useNotifications from "../../hooks/useNotification";
import Account from "./components/account/Account";
import openNav from "./../../assets/images/openMenu.svg";
import closeNav from "./../../assets/images/closeMenu.svg";
import { useRef } from "react";
function Header() {
  const [isDownloadOpen, toggleDownloadOpen] = useToggle();
  const { notifications, addNotification, removeNotification } =
    useNotifications();
  const [isAccountOpen, toggleAccountOpen] = useToggle();
  const [isMenuOpened, toggleMenuOpened] = useToggle();
  const navigationRef = useRef();
  return (
    <>
      <NotificationContainer
        onClose={removeNotification}
        notifications={notifications}
      />
      <header className="header">
        <div className="container header__container">
          <picture className="image-wrapper">
            <img src={logo} alt="K1 Logo" className="image-wrapper__image" />
          </picture>
          <button
            onClick={toggleMenuOpened}
            className="header__open-navigation-btn"
          >
            <img src={openNav} alt="" />
          </button>
          <div
            onClick={(e) => {
              if(!e.target.closest('.header__navigation')) {
                toggleMenuOpened();
              }
            }}
            className={
              isMenuOpened
                ? "header__navigation-wrapper header__navigation-wrapper--opened"
                : "header__navigation-wrapper"
            }
          >
            <ul
              ref={navigationRef}
              className={
                isMenuOpened
                  ? "header__navigation header__navigation--opened"
                  : "header__navigation"
              }
            >
              <button
                onClick={toggleMenuOpened}
                className="header__close-navigation-btn"
              >
                <img src={closeNav} alt="" />
              </button>
              <li className="header__navigation-item">
                <Link className="header__navigation-text" to={"/"}>
                  Главная
                </Link>
              </li>
              <li className="header__navigation-item">
                <button
                  onClick={toggleDownloadOpen}
                  className="header__navigation-text"
                >
                  Использовать сейчас
                </button>
                {isDownloadOpen && (
                  <UploadFile addNotification={addNotification} />
                )}
              </li>
              <li className="header__navigation-item">
                <button
                  onClick={toggleAccountOpen}
                  className="header__navigation-text"
                >
                  Личный кабинет
                </button>
                {isAccountOpen && <Account addNotification={addNotification} />}
              </li>
            </ul>
          </div>
        </div>
      </header>
    </>
  );
}

export default Header;
