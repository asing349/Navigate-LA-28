import React, { useState } from "react";
import { MapContainer, TileLayer, Marker, useMapEvents, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default marker icon
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

// Add a new red icon configuration after the default icon setup
const redIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

// Add this after the redIcon configuration
const greenIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
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
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  const [username, setUsername] = useState(null);
  const [searchResults, setSearchResults] = useState([]);
  const [resultMarkers, setResultMarkers] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isPanelVisible, setIsPanelVisible] = useState(true);

  const handleLocationSelect = (coords) => {
    setSelectedLocation(coords);
    const [lat, lng] = coords;
    setSearchQuery(`${lat.toFixed(6)}, ${lng.toFixed(6)}`);
    handleSearch(coords, searchType);
  };

  const handleLoginSuccess = (loggedInUsername) => {
    setIsLoginOpen(false);
    setUsername(loggedInUsername);
  };

  const handleSearch = async (location = selectedLocation, type = searchType) => {
    if (!location) {
      alert("Please select a location on the map first");
      return;
    }

    setIsLoading(true);
    setResultMarkers([]);
    setSearchResults([]);

    try {
      const [lat, lng] = location;
      const endpoint = type === "nearest_places"
        ? 'nearest_places'
        : 'nearest_restrooms';

      const url = new URL(`http://localhost:8000/api/geo/${endpoint}/`);
      url.searchParams.append('lat', lat);
      url.searchParams.append('long', lng);

      const response = await fetch(url, {
        method: 'GET',
        headers: {
          ...(localStorage.getItem('access_token') && {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          })
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setSearchResults(data);

      // Update markers from the search results
      const markers = data.map(result => ({
        position: [result.latitude, result.longitude],
        name: result.name || 'Unnamed Location'
      }));
      setResultMarkers(markers);
    } catch (error) {
      console.error('Error details:', error);
      alert(`Failed to fetch ${type.replace('_', ' ')}`);
    } finally {
      setIsLoading(false);
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
            onChange={(e) => {
              setSearchType(e.target.value);
              setResultMarkers([]); // Clear markers when switching search type
              setSearchResults([]); // Clear results when switching search type
              if (selectedLocation) { // Only trigger search if location is selected
                handleSearch(selectedLocation, e.target.value);
              }
            }}
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
          <div style={{
            fontSize: "14px",
            color: "#5f6368"
          }}>
            Selected: {selectedLocation[0].toFixed(6)}, {selectedLocation[1].toFixed(6)}
          </div>
        )}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginLeft: 'auto' }}>
          {username && (
            <span style={{
              fontSize: '14px',
              color: '#5f6368'
            }}>
              {username}
            </span>
          )}
          <button
            onClick={() => {
              if (username) {
                // Handle logout
                localStorage.removeItem('access_token');
                setUsername(null);
              } else {
                setIsLoginOpen(true);
              }
            }}
            style={{
              backgroundColor: '#1a73e8',
              color: 'white',
              width: '36px',
              height: '36px',
              borderRadius: '50%',
              border: 'none',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '16px'
            }}
          >
            {username ? '👤' : '🔑'}
          </button>
        </div>
      </div>
      <div style={{
        flex: 1,
        display: "flex",
        gap: "20px",
        padding: "20px"
      }}>
        <div style={{
          flex: searchResults.length && isPanelVisible ? "1 1 70%" : "1 1 100%",
          transition: "flex 0.3s ease"
        }}>
          <MapContainer
            center={[34.0522, -118.2437]}
            zoom={13}
            style={{ height: "100%", width: "100%" }}
            zoomControl={false}
          >
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            <LocationMarker onLocationSelect={handleLocationSelect} />
            {resultMarkers.map((marker, index) => (
              <Marker
                key={index}
                position={marker.position}
                icon={searchType === 'nearest_restrooms' ? greenIcon : redIcon}
              >
                <Popup>
                  <div style={{
                    padding: '8px',
                    minWidth: '200px',
                    maxWidth: '300px'
                  }}>
                    <h3 style={{
                      margin: '0 0 8px 0',
                      color: '#1a73e8',
                      fontSize: '16px',
                      borderBottom: '1px solid #eee',
                      paddingBottom: '8px'
                    }}>{marker.name}</h3>

                    {searchResults[index].description && (
                      <p style={{
                        margin: '4px 0',
                        fontSize: '14px',
                        color: '#5f6368'
                      }}>{searchResults[index].description}</p>
                    )}

                    <div style={{
                      fontSize: '13px',
                      color: '#3c4043',
                      marginTop: '8px'
                    }}>
                      <p style={{
                        margin: '4px 0',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '4px'
                      }}>
                        📍 {searchResults[index].address || 'Address not available'}
                      </p>

                      {searchResults[index].types && (
                        <p style={{
                          margin: '4px 0',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '4px'
                        }}>
                          🏷️ {searchResults[index].types}
                        </p>
                      )}

                      <p style={{
                        margin: '4px 0',
                        fontSize: '12px',
                        color: '#80868b'
                      }}>
                        📌 {searchResults[index].latitude.toFixed(6)}, {searchResults[index].longitude.toFixed(6)}
                      </p>
                    </div>
                  </div>
                </Popup>
              </Marker>
            ))}
          </MapContainer>
        </div>

        {searchResults.length > 0 && (
          <div style={{
            flex: isPanelVisible ? "1 1 30%" : "0 0 auto",
            backgroundColor: 'white',
            padding: isPanelVisible ? '15px' : '8px',
            borderRadius: '8px',
            boxShadow: '0 2px 6px rgba(0,0,0,0.1)',
            maxHeight: 'calc(100vh - 140px)',
            overflowY: 'auto',
            alignSelf: 'flex-start',
            transition: 'all 0.3s ease',
            width: isPanelVisible ? 'auto' : '40px',
            position: 'relative',
            display: 'flex',
            flexDirection: 'column'
          }}>
            <div style={{
              display: 'flex',
              justifyContent: isPanelVisible ? 'space-between' : 'center',
              alignItems: 'center',
              marginBottom: isPanelVisible ? '15px' : '0',
              borderBottom: isPanelVisible ? '1px solid #eee' : 'none',
              paddingBottom: isPanelVisible ? '10px' : '0'
            }}>
              {isPanelVisible && (
                <h3 style={{
                  margin: '0',
                  color: '#1a73e8',
                  fontSize: '18px',
                  fontWeight: '500'
                }}>Search Results</h3>
              )}
              <button
                onClick={() => setIsPanelVisible(!isPanelVisible)}
                style={{
                  backgroundColor: '#1a73e8',
                  color: 'white',
                  border: 'none',
                  borderRadius: '50%',
                  width: '36px',
                  height: '36px',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '18px',
                  transition: 'all 0.2s ease',
                  boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                  outline: 'none',
                  padding: 0,
                  transform: isPanelVisible ? 'rotate(0deg)' : 'rotate(180deg)'
                }}
              >
                ›
              </button>
            </div>

            {isPanelVisible && searchResults.map((result, index) => (
              <div key={index} style={{
                padding: '12px',
                borderBottom: '1px solid #eee',
                fontSize: '14px',
                backgroundColor: index % 2 === 0 ? '#f8f9fa' : 'white',
                borderRadius: '4px',
                marginBottom: '8px'
              }}>
                <div style={{
                  fontWeight: '500',
                  color: '#1a73e8',
                  marginBottom: '4px'
                }}>
                  {result.name || 'Unnamed Location'}
                </div>
                <div style={{
                  color: '#5f6368',
                  fontSize: '13px',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '4px'
                }}>
                  <div>📍 Distance: {result.distance?.toFixed(2) || 'N/A'} meters</div>
                  {result.address && <div>🏠 Address: {result.address}</div>}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      <LoginModal
        isOpen={isLoginOpen}
        onClose={() => setIsLoginOpen(false)}
        onSuccess={handleLoginSuccess}
      />
      {isLoading && (
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          backgroundColor: 'white',
          padding: '20px',
          borderRadius: '8px',
          boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
          zIndex: 1000,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '10px'
        }}>
          <div style={{
            width: '40px',
            height: '40px',
            border: '4px solid #f3f3f3',
            borderTop: '4px solid #1a73e8',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite'
          }} />
          <div style={{ color: '#5f6368', fontSize: '14px' }}>
            Searching nearby locations...
          </div>
        </div>
      )}
      <style>
        {`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}
      </style>
    </div>
  );
}

export default App;