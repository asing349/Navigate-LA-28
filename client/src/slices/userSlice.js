// src/slices/userSlice.js
import { createSlice } from "@reduxjs/toolkit";

const userSlice = createSlice({
  name: "user",
  initialState: {
    name: "",
    loggedIn: false,
  },
  reducers: {
    logIn: (state, action) => {
      state.name = action.payload;
      state.loggedIn = true;
    },
    logOut: (state) => {
      state.name = "";
      state.loggedIn = false;
    },
  },
});

export const { logIn, logOut } = userSlice.actions;
export default userSlice.reducer;
