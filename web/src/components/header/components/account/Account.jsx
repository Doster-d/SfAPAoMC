import { useState } from "react";
import SignIn from "../signin/SignIn";
import "./style.scss";
import SignUp from "../signup/SignUp";

function Account() {
  const [isRegistration, setIsRegistration] = useState(false);
  return (
    <div className="account">{isRegistration ? <SignUp setIsRegistration={setIsRegistration} /> : <SignIn setIsRegistration={setIsRegistration}/>}</div>
  );
}

export default Account;
