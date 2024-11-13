// src/slices/userSlice.js
import { createSlice } from '@reduxjs/toolkit';

const testSlice = createSlice({
  name: 'user',
  initialState: {
    name: '',
    loggedIn: false,
  },
  reducers: {
    logIn: (state, action) => {
      state.name = action.payload;
      state.loggedIn = true;
    },
    logOut: (state) => {
      state.name = '';
      state.loggedIn = false;
    },
  },
});

export const { logIn, logOut } = testSlice.actions;
export default testSlice.reducer;
