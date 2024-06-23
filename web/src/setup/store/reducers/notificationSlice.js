import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  newNotification: {
    message: "",
    type: "",
    duration: null,
  },
};

export const notificationSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    addNewNotification(state, action) {
      state.newNotification.message = action.payload.message;
      state.newNotification.type = action.payload.type;
      state.newNotification.duration = action.payload.duration;
    },
  },
});

export const { addNewNotification } = notificationSlice.actions;

export default notificationSlice.reducer;
