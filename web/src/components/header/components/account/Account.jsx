import { useState } from "react";
import SignIn from "./signin/SignIn";
import "./style.scss";
import SignUp from "./signup/SignUp";

function Account({ addNotification }) {
  const [isRegistration, setIsRegistration] = useState(false);
  return (
    <div className="account">
      {isRegistration ? (
        <SignUp
          addNotification={addNotification}
          setIsRegistration={setIsRegistration}
        />
      ) : (
        <SignIn addNotification={addNotification} setIsRegistration={setIsRegistration} />
      )}
    </div>
  );
}

export default Account;
