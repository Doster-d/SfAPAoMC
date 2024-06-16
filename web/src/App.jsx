import { RouterProvider } from "react-router-dom";
import "./App.scss";
import { router } from "./setup/react-router-dom";

function App() {


  return <RouterProvider router={router}/>;
}

export default App;
