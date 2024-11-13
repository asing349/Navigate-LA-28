// src/slices/index.js
import { combineReducers } from "redux";
import userReducer from "./userSlice";
import testReducer from "./testSlice";

const rootReducer = combineReducers({
  user: userReducer,
  test: testReducer,
});

export default rootReducer;
