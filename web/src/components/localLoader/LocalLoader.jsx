import LoaderSpinner from "../loaderSpinner/LoaderSpinner";
import './style.scss'
function LocalLoader() {
  return (
    <div className="local-loader">
      <LoaderSpinner />
    </div>
  );
}

export default LocalLoader;
