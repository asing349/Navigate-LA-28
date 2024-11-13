// src/components/TestProfile.js
import React from "react";
import { useSelector, useDispatch } from "react-redux";
import { logIn, logOut } from "../slices/userSlice";

const TestProfile = () => {
  const user = useSelector((state) => state.user);
  const dispatch = useDispatch();

  return (
    <div>
      <h1>User Profile</h1>
      <p>Name: {user.name}</p>
      <p>Logged In: {user.loggedIn ? "Yes" : "No"}</p>
      <button onClick={() => dispatch(logIn("John Doe"))}>Log In</button>
      <button onClick={() => dispatch(logOut())}>Log Out</button>
    </div>
  );
};

export default TestProfile;
