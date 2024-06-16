import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import { HelmetProvider } from "react-helmet-async";
import { Provider } from "react-redux";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { store } from "./setup/store/store.js";
import { setUserData } from "./setup/store/reducers/userSlice.js";
import { getCookieByName } from "./utils.js";

const queryClient = new QueryClient();
store.dispatch(setUserData(JSON.parse(getCookieByName('user'))))
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <Provider store={store}>
      <HelmetProvider>
        <QueryClientProvider client={queryClient}>
          <App />
        </QueryClientProvider>
      </HelmetProvider>
    </Provider>
  </React.StrictMode>
);
