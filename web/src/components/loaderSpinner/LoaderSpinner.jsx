import spinnerRight from "./../../assets/images/spinner/spinner_right.svg";
import spinnerLeft from "./../../assets/images/spinner/spinner_left.svg";
import logo from "./../../assets/images/mainpage/header_logo.svg";
function LoaderSpinner() {
  return (
    <picture className="spinner">
      <img className="spinner__image" src={logo} alt="" />
    </picture>
  );
}

export default LoaderSpinner;
