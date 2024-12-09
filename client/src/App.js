// src/App.js
import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { setLocation } from "./slices/locationSlice";
import Header from "./components/Header";
import MapContainerComponent from "./components/MapContainerComponent";
import SearchBar from "./components/SearchBar";
import LoginModal from "./components/LoginModal";
import "./App.css";

<<<<<<< HEAD
// Fix for default marker icon
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

function LocationMarker({ onLocationSelect }) {
  const [position, setPosition] = useState(null);

  useMapEvents({
    click(e) {
      const { lat, lng } = e.latlng;
      setPosition([lat, lng]);
      onLocationSelect([lat, lng]);
    },
  });

  return position ? <Marker position={position} /> : null;
}

function LoginModal({ isOpen, onClose, onSuccess }) {
  const [isLoginMode, setIsLoginMode] = useState(true);
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    dob: '',
    country: ''
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const formBody = new URLSearchParams();
      formBody.append('username', formData.username);
      formBody.append('password', formData.password);

      const response = await fetch('http://localhost:8000/api/auth/token/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formBody
      });

      if (!response.ok) {
        throw new Error('Invalid credentials');
      }

      const data = await response.json();
      localStorage.setItem('access_token', data.access_token);
      setSuccessMessage('Login successful!');
      setTimeout(() => onSuccess(formData.username), 1500);
    } catch (error) {
      setError('Login failed. Please check your credentials.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateAccount = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMessage('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/users/users/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: formData.username,
          password: formData.password,
          dob: formData.dob || null,
          country: formData.country || null
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to create account');
      }

      setSuccessMessage('Account created successfully! You can now log in.');
      setFormData({
        username: '',
        password: '',
        dob: '',
        country: ''
      });

      // Switch to login mode after successful account creation
      setTimeout(() => {
        setIsLoginMode(true);
        setSuccessMessage('');
      }, 1500);

    } catch (error) {
      setError('Failed to create account: ' + error.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  if (!isOpen) return null;

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000
    }}>
      <div style={{
        backgroundColor: 'white',
        padding: '24px',
        borderRadius: '8px',
        width: '100%',
        maxWidth: '400px',
        position: 'relative'
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '24px'
        }}>
          <h2 style={{ margin: 0, color: '#202124', fontSize: '24px' }}>
            {isLoginMode ? 'Sign In' : 'Create Account'}
          </h2>
          <button onClick={onClose} style={{
            border: 'none',
            background: 'none',
            fontSize: '24px',
            cursor: 'pointer'
          }}>×</button>
        </div>

        <form onSubmit={isLoginMode ? handleLogin : handleCreateAccount}>
          {error && (
            <div style={{
              color: '#d93025',
              fontSize: '14px',
              marginBottom: '12px',
              padding: '8px',
              backgroundColor: '#fce8e6',
              borderRadius: '4px'
            }}>{error}</div>
          )}

          {successMessage && (
            <div style={{
              color: '#34a853',
              fontSize: '14px',
              marginBottom: '12px',
              padding: '8px',
              backgroundColor: '#e6f4ea',
              borderRadius: '4px'
            }}>{successMessage}</div>
          )}

          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              placeholder="Username"
              required
              style={{
                padding: '8px 12px',
                borderRadius: '4px',
                border: '1px solid #dadce0',
                fontSize: '14px'
              }}
            />

            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Password"
              required
              style={{
                padding: '8px 12px',
                borderRadius: '4px',
                border: '1px solid #dadce0',
                fontSize: '14px'
              }}
            />

            {!isLoginMode && (
              <>
                <input
                  type="date"
                  name="dob"
                  value={formData.dob}
                  onChange={handleChange}
                  placeholder="Date of Birth"
                  style={{
                    padding: '8px 12px',
                    borderRadius: '4px',
                    border: '1px solid #dadce0',
                    fontSize: '14px'
                  }}
                />

                <input
                  type="text"
                  name="country"
                  value={formData.country}
                  onChange={handleChange}
                  placeholder="Country"
                  style={{
                    padding: '8px 12px',
                    borderRadius: '4px',
                    border: '1px solid #dadce0',
                    fontSize: '14px'
                  }}
                />
              </>
            )}
          </div>

          <div style={{
            marginTop: '24px',
            display: 'flex',
            flexDirection: 'column',
            gap: '12px'
          }}>
            <button
              type="submit"
              disabled={isLoading}
              style={{
                backgroundColor: '#1a73e8',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                padding: '8px 24px',
                fontSize: '14px',
                fontWeight: '500',
                cursor: isLoading ? 'not-allowed' : 'pointer',
                transition: 'background-color 0.2s ease',
                opacity: isLoading ? 0.7 : 1
              }}
            >
              {isLoading ? 'Please wait...' : (isLoginMode ? 'Sign In' : 'Create Account')}
            </button>

            <button
              type="button"
              onClick={() => {
                setIsLoginMode(!isLoginMode);
                setError('');
                setSuccessMessage('');
              }}
              style={{
                backgroundColor: 'transparent',
                color: '#1a73e8',
                border: 'none',
                padding: '8px',
                fontSize: '14px',
                cursor: 'pointer',
                textDecoration: 'underline'
              }}
            >
              {isLoginMode ? 'Need an account? Create one' : 'Already have an account? Sign in'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function App() {
  const [searchQuery, setSearchQuery] = useState("");
  const [searchType, setSearchType] = useState("nearest_places");
  const [selectedLocation, setSelectedLocation] = useState(null);
=======
const App = () => {
>>>>>>> 5ac6c53c86b5d3bc0cbc9153afe0c09c45438412
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

  const handleSearch = async () => {
    if (!selectedLocation) {
      alert("Please select a location on the map first");
      return;
    }

    if (searchType === "nearest_places") {
      try {
        const [lat, lng] = selectedLocation;
        console.log('Sending request with coordinates:', { lat, lng });

        const response = await fetch('http://localhost:8000/api/nearest_places/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            ...(localStorage.getItem('access_token') && {
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            })
          },
          body: JSON.stringify({ lat, long: lng })
        });

        console.log('Raw response:', response);
        const data = await response.json();
        console.log('Response data:', data);

      } catch (error) {
        console.error('Error details:', error);
        alert('Failed to fetch nearest places');
      }
    }
  };

  return (
    <div style={{
      fontFamily: "Roboto, Arial, sans-serif",
      height: "100vh",
      display: "flex",
      flexDirection: "column",
      backgroundColor: "#f8f9fa"
    }}>
      <div style={{
        padding: "12px 24px",
        backgroundColor: "white",
        boxShadow: "0 1px 3px rgba(0,0,0,0.12)",
        display: "flex",
        alignItems: "center",
        gap: "20px"
      }}>
        <h1 style={{
          color: "#1a73e8",
          margin: 0,
          fontSize: "22px",
          fontWeight: "400"
        }}>Navigate LA</h1>
        <div style={{
          display: "flex",
          gap: "10px",
          flex: 1,
          maxWidth: "700px",
          backgroundColor: "white",
          padding: "8px 16px",
          borderRadius: "8px",
          boxShadow: "0 2px 4px rgba(0,0,0,0.1), 0 4px 8px rgba(0,0,0,0.1)",
          transition: "box-shadow 0.3s ease"
        }}>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Click on map or search in LA..."
            style={{
              padding: "8px 12px",
              border: "none",
              outline: "none",
              fontSize: "15px",
              flex: 1,
              backgroundColor: "transparent"
            }}
          />
          <select
            value={searchType}
            onChange={(e) => setSearchType(e.target.value)}
            style={{
              padding: "8px 12px",
              border: "none",
              outline: "none",
              fontSize: "15px",
              color: "#5f6368",
              backgroundColor: "transparent",
              cursor: "pointer"
            }}
          >
            <option value="nearest_places">Nearest Places</option>
            <option value="nearest_restrooms">Nearest Restrooms</option>
          </select>
          <button
            onClick={handleSearch}
            style={{
              backgroundColor: "#1a73e8",
              color: "white",
              border: "none",
              borderRadius: "4px",
              padding: "8px 16px",
              cursor: "pointer",
              fontSize: "14px",
              fontWeight: "500",
              transition: "background-color 0.2s ease",
            }}
          >
            Search
          </button>
        </div>
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
