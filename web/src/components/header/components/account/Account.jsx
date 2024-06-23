import { useState } from "react";
import SignIn from "./signin/SignIn";
import "./style.scss";
import SignUp from "./signup/SignUp";
import { useDispatch, useSelector } from "react-redux";
import { clearUserData } from "../../../../setup/store/reducers/userSlice";

function Account() {
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
          setIsRegistration={setIsRegistration}
        />
      ) : (
        <SignIn
          setIsRegistration={setIsRegistration}
        />
      )}
    </div>
  );
}

export default Account;
