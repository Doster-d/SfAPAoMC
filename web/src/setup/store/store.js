import { configureStore } from "@reduxjs/toolkit";

import userReducer from './reducers/userSlice';
import notificationReducer from "./reducers/notificationSlice";

export const store = configureStore({
    reducer: {
        notification: notificationReducer,
        user: userReducer
    }
})