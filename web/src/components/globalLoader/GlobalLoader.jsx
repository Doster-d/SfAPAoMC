import LoaderSpinner from "../loaderSpinner/LoaderSpinner";
import './style.scss'
function GlobalLoader() {
    return ( <div className="global-loader">
        <LoaderSpinner />
    </div> );
}

export default GlobalLoader;