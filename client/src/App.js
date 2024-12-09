// src/App.js
import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { setLocation } from "./slices/locationSlice";
import Header from "./components/Header";
import MapContainerComponent from "./components/MapContainerComponent";
import SearchBar from "./components/SearchBar";
import LoginModal from "./components/LoginModal";
import "./App.css";

const App = () => {
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  const { selectedLocation } = useSelector((state) => state.location);
  const { user } = useSelector((state) => state.auth);
  const dispatch = useDispatch();

  const handleLocationSelect = (coords) => {
    dispatch(setLocation(coords));
  };

  const handleLoginSuccess = (username) => {
    setIsLoginOpen(false);
  };

  return (
    <div className="app">
      <Header
        username={user?.username}
        onLoginToggle={() => setIsLoginOpen(!isLoginOpen)}
      />
      <div className="main">
        <SearchBar />
        <MapContainerComponent onLocationSelect={handleLocationSelect} />
        {selectedLocation && (
          <div className="location-info">
            Selected: {selectedLocation[0].toFixed(6)},{" "}
            {selectedLocation[1].toFixed(6)}
          </div>
        )}
      </div>
      <LoginModal
        isOpen={isLoginOpen}
        onClose={() => setIsLoginOpen(false)}
        onSuccess={handleLoginSuccess}
      />
    </div>
  );
};

export default App;
