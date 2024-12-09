// src/slices/rootReducer.js
import { combineReducers } from "redux";
import authReducer from "./authSlice";
import locationReducer from "./locationSlice";

const rootReducer = combineReducers({
  auth: authReducer,
  location: locationReducer,
});

export default rootReducer;
