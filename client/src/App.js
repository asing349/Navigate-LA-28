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
  const [searchQuery, setSearchQuery] = useState("");
  const [searchType, setSearchType] = useState("query1");
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
      {/* Header Component */}
      <Header
        username={user?.username}
        onLoginToggle={() => setIsLoginOpen(!isLoginOpen)}
      />

      {/* Main Content */}
      <div className="main">
        <SearchBar
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
          searchType={searchType}
          setSearchType={setSearchType}
        />
        <MapContainerComponent onLocationSelect={handleLocationSelect} />
        {selectedLocation && (
          <div className="location-info">
            Selected: {selectedLocation[0].toFixed(6)},{" "}
            {selectedLocation[1].toFixed(6)}
          </div>
        )}
      </div>

      {/* Login Modal */}
      <LoginModal
        isOpen={isLoginOpen}
        onClose={() => setIsLoginOpen(false)}
        onSuccess={handleLoginSuccess}
      />
    </div>
  );
};

export default App;

