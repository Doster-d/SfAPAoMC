import { useState } from "react";
import SignIn from "./signin/SignIn";
import "./style.scss";
import SignUp from "./signup/SignUp";
import { useDispatch, useSelector } from "react-redux";
import { clearUserData } from "../../../../setup/store/reducers/userSlice";

function Account({ addNotification }) {
  const [isRegistration, setIsRegistration] = useState(false);
  const { userId } = useSelector((state) => state.user);
  const dispatch = useDispatch();
  const logOutHandle = () => {
    dispatch(clearUserData());
    document.cookie = "";
  };
  return (
    <div className="account">
      {userId ? (
        <button
          onClick={(e) => {
            e.preventDefault();
            logOutHandle()
          }}
          className="account__btn"
        >
          Выйти
        </button>
      ) : isRegistration ? (
        <SignUp
          addNotification={addNotification}
          setIsRegistration={setIsRegistration}
        />
      ) : (
        <SignIn
          addNotification={addNotification}
          setIsRegistration={setIsRegistration}
        />
      )}
    </div>
  );
}

export default Account;
