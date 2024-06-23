import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  username: "",
  accessToken: "",
  userId: null,
};

export const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    setUserData(state, action) {
      state.username = action.payload.username ? action.payload?.username : "";
      state.accessToken = action.payload.accessToken
        ? action.payload?.accessToken
        : "";
      state.userId = action.payload.userId ? action.payload?.userId : null;
    },
    clearUserData(state) {
      state.username = "";
      state.accessToken = "";
      state.userId = null;
    },
  },
});

export const { setUserData, clearUserData } = userSlice.actions;

export default userSlice.reducer;
