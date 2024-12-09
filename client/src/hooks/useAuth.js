// src/hooks/useAuth.js
import { useDispatch, useSelector } from "react-redux";
import { login, logout } from "../slices/authSlice";

export const useAuth = () => {
  const dispatch = useDispatch();
  const { user, isAuthenticated } = useSelector((state) => state.auth);

  const loginUser = (userData) => dispatch(login(userData));
  const logoutUser = () => dispatch(logout());

  return { user, isAuthenticated, loginUser, logoutUser };
};
