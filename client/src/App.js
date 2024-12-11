import React, { useState, useEffect, useRef } from "react";
import { MapContainer, TileLayer, Marker, useMapEvents, Popup, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { Bar, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

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

// Add this after the greenIcon configuration
const busIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-yellow.png',
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

function Analytics() {
  const [data, setData] = useState({
    attractions: null,
    demographics: null,
    busRoutes: null,
    popularStops: null,
    geoDistribution: null
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeSubTab, setActiveSubTab] = useState('attractions');
  const chartRef = useRef(null);

  useEffect(() => {
    // Cleanup chart instance when component unmounts or tab changes
    return () => {
      if (chartRef.current) {
        chartRef.current.destroy();
      }
    };
  }, [activeSubTab]);

  useEffect(() => {
    const fetchData = async () => {
      if (data[activeSubTab] !== null) return;

      setIsLoading(true);
      setError(null);
      try {
        // Build the URL with query parameters based on the tab
        let url = `http://localhost:8000/api/analytics/${activeSubTab}`;
        const queryParams = new URLSearchParams();

        // Add specific query parameters based on the tab
        switch (activeSubTab) {
          case 'attractions':
            queryParams.append('limit', '10');
            break;
          case 'bus-routes':
            queryParams.append('limit', '10');
            break;
          case 'popular-stops':
            queryParams.append('limit', '10');
            break;
          // demographics and geographic-distribution don't need query params
          default:
            break;
        }

        // Append query parameters if any exist
        const queryString = queryParams.toString();
        if (queryString) {
          url += `?${queryString}`;
        }

        const response = await fetch(url);
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }
        const responseData = await response.json();
        setData(prevData => ({
          ...prevData,
          [activeSubTab]: responseData
        }));
      } catch (error) {
        setError(error.message);
        console.error(`Error fetching ${activeSubTab} data:`, error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [activeSubTab]);

  const getChartData = () => {
    const currentData = data[activeSubTab];
    if (!currentData) return null;

    const defaultOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
          labels: {
            padding: 20,
            font: {
              size: 12
            }
          }
        },
        title: {
          display: true,
          text: getChartTitle(),
          font: {
            size: 16,
            weight: 'bold'
          },
          padding: 20
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            font: {
              size: 12
            }
          }
        },
        x: {
          ticks: {
            font: {
              size: 12
            },
            maxRotation: 45,
            minRotation: 45
          }
        }
      }
    };

    switch (activeSubTab) {
      case 'attractions':
        return {
          data: {
            labels: currentData.map(a => a.name.length > 20 ? a.name.substring(0, 20) + '...' : a.name),
            datasets: [{
              label: 'Average Rating',
              data: currentData.map(a => a.rating),
              backgroundColor: 'rgba(54, 162, 235, 0.5)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 1
            }]
          },
          options: {
            ...defaultOptions,
            scales: {
              ...defaultOptions.scales,
              y: {
                ...defaultOptions.scales.y,
                max: 5,
                title: {
                  display: true,
                  text: 'Rating (out of 5)',
                  font: {
                    size: 14
                  }
                }
              }
            }
          }
        };

      case 'demographics':
        return {
          data: {
            labels: Object.keys(currentData.age_distribution || {}),
            datasets: [{
              data: Object.values(currentData.age_distribution || {}),
              backgroundColor: [
                'rgba(255, 99, 132, 0.7)',
                'rgba(54, 162, 235, 0.7)',
                'rgba(255, 206, 86, 0.7)',
                'rgba(75, 192, 192, 0.7)',
                'rgba(153, 102, 255, 0.7)',
              ],
              borderWidth: 1
            }]
          },
          options: {
            ...defaultOptions,
            plugins: {
              ...defaultOptions.plugins,
              legend: {
                ...defaultOptions.plugins.legend,
                position: 'right'
              }
            }
          }
        };

      case 'bus-routes':
        return {
          data: {
            labels: currentData.map(route => route.route_number),
            datasets: [{
              label: 'Number of Trips',
              data: currentData.map(route => route.trip_count),
              backgroundColor: 'rgba(26, 115, 232, 0.5)',
              borderColor: 'rgba(26, 115, 232, 1)',
              borderWidth: 1
            }]
          },
          options: defaultOptions
        };

      case 'popular-stops':
        return {
          data: {
            labels: currentData.map(stop => stop.stop_name),
            datasets: [{
              label: 'Usage Count',
              data: currentData.map(stop => stop.usage_count),
              backgroundColor: 'rgba(26, 115, 232, 0.5)',
              borderColor: 'rgba(26, 115, 232, 1)',
              borderWidth: 1
            }]
          },
          options: defaultOptions
        };

      case 'geographic-distribution':
        return {
          data: {
            labels: Object.keys(currentData || {}),
            datasets: [{
              data: Object.values(currentData || {}),
              backgroundColor: [
                'rgba(255, 99, 132, 0.5)',
                'rgba(54, 162, 235, 0.5)',
                'rgba(255, 206, 86, 0.5)',
                'rgba(75, 192, 192, 0.5)',
              ],
              borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
              ],
              borderWidth: 1
            }]
          },
          options: defaultOptions
        };

      case 'demographics':
        return {
          data: {
            labels: currentData.map(item => `${item.age_group} (${item.country})`),
            datasets: [
              {
                label: 'Total Reviews',
                data: currentData.map(item => item.total_reviews),
                backgroundColor: 'rgba(75, 192, 192, 0.5)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
              },
              {
                label: 'Average Rating',
                data: currentData.map(item => item.avg_rating),
                backgroundColor: 'rgba(255, 206, 86, 0.5)',
                borderColor: 'rgba(255, 206, 86, 1)',
                borderWidth: 1
              },
              {
                label: 'Unique Places Reviewed',
                data: currentData.map(item => item.unique_places_reviewed),
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
              }
            ]
          },
          options: defaultOptions
        };

      default:
        return null;
    }
  };

  const getChartTitle = () => {
    switch (activeSubTab) {
      case 'attractions':
        return 'Top Attractions by Rating';
      case 'demographics':
        return 'User Age Distribution';
      case 'bus-routes':
        return 'Most Popular Bus Routes';
      case 'popular-stops':
        return 'Most Frequently Used Bus Stops';
      case 'geographic-distribution':
        return 'User Geographic Distribution';
      default:
        return '';
    }
  };

  const renderChart = () => {
    const chartData = getChartData();
    if (!chartData) return null;

    const ChartComponent = activeSubTab === 'demographics' || activeSubTab === 'geographic-distribution'
      ? Pie
      : Bar;

    return (
      <div style={{ height: '400px' }}>
        <ChartComponent
          ref={chartRef}
          data={chartData.data}
          options={chartData.options}
        />
      </div>
    );
  };

  const createNumberedIcon = (number) => {
    return L.divIcon({
      className: 'custom-numbered-icon',
      html: `<div style="
        background-color: #1a73e8;
        color: white;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: bold;
        border: 2px solid white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
      ">${number}</div>`,
      iconSize: [24, 24],
      iconAnchor: [12, 12],
      popupAnchor: [0, -12],
    });
  };

  const renderContent = () => {
    if (isLoading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    switch (activeSubTab) {
      case 'attractions':
        if (!data.attractions || !Array.isArray(data.attractions)) {
          return <div>No attraction data available</div>;
        }

        return (
          <div style={{ height: 'calc(100vh - 200px)', width: '100%' }}>
            <MapContainer
              center={[34.0522, -118.2437]}
              zoom={11}
              style={{ height: '100%', width: '100%' }}
            >
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              />
              {data.attractions.map((place, index) => {
                if (!place || typeof place.latitude !== 'number' || typeof place.longitude !== 'number') {
                  return null;
                }

                return (
                  <Marker
                    key={place.place_id || index}
                    position={[place.latitude, place.longitude]}
                    icon={createNumberedIcon(index + 1)}
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
                        }}>
                          {index + 1}. {place.name || 'Unnamed Location'}
                        </h3>
                        <div style={{
                          fontSize: '13px',
                          color: '#5f6368',
                          display: 'flex',
                          flexDirection: 'column',
                          gap: '4px'
                        }}>
                          <div>⭐ Rating: {place.avg_rating?.toFixed(2) || 'N/A'}/5</div>
                          <div>📊 Reviews: {place.review_count || 0}</div>
                          <div>🏆 High Ratings: {place.high_rating_ratio ?
                            Math.round(place.high_rating_ratio * 100) : 'N/A'}%</div>
                          {place.category && <div>🏷️ Category: {place.category}</div>}
                          <div style={{ fontSize: '12px', color: '#80868b', marginTop: '4px' }}>
                            📍 {place.latitude?.toFixed(6)}, {place.longitude?.toFixed(6)}
                          </div>
                        </div>
                      </div>
                    </Popup>
                  </Marker>
                );
              })}
            </MapContainer>
          </div>
        );

      // ... other cases remain the same ...
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <div style={{
        display: 'flex',
        gap: '10px',
        marginBottom: '20px'
      }}>
        <button
          onClick={() => setActiveSubTab('attractions')}
          style={{
            padding: '8px 16px',
            backgroundColor: activeSubTab === 'attractions' ? '#1a73e8' : '#fff',
            color: activeSubTab === 'attractions' ? '#fff' : '#1a73e8',
            border: '1px solid #1a73e8',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Top Attractions
        </button>
        {/* ... other tab buttons ... */}
      </div>

      {renderContent()}
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
  const [busRoute, setBusRoute] = useState(null);
  const [attractionPlan, setAttractionPlan] = useState(null);
  const [activeTab, setActiveTab] = useState('map');

  const handleLocationSelect = (coords) => {
    setSelectedLocation(coords);
    const [lat, lng] = coords;
    setSearchQuery(`${lat.toFixed(6)}, ${lng.toFixed(6)}`);
    // Clear bus route when new location is selected
    setBusRoute(null);

    // If we're in attraction plan mode, fetch new plan
    if (searchType === "attraction_plan") {
      fetchAttractionPlan(coords);
    } else {
      // Only set default search type if no previous results exist
      if (searchResults.length === 0) {
        setSearchType("nearest_places");
        handleSearch(coords, "nearest_places");
      } else {
        // Otherwise use current search type
        handleSearch(coords, searchType);
      }
    }
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
    // Clear bus route when new search is performed
    setBusRoute(null);

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

  const fetchBusStops = async (targetLat, targetLon) => {
    if (!selectedLocation) return;

    try {
      const url = new URL('http://localhost:8000/api/geo/direct_bus_routes/');
      url.searchParams.append('lat1', selectedLocation[0]);
      url.searchParams.append('long1', selectedLocation[1]);
      url.searchParams.append('lat2', targetLat);
      url.searchParams.append('long2', targetLon);
      url.searchParams.append('buffer_radius', '0.5');

      const response = await fetch(url, {
        headers: {
          ...(localStorage.getItem('access_token') && {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          })
        }
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
      }

      const responseData = await response.json();
      console.log('Raw API response:', responseData);

      // Check if we have a success response with data
      if (responseData.status === "success" && responseData.data) {
        console.log('Setting bus route with data:', responseData.data);
        setBusRoute(responseData.data);
      } else {
        console.log('No valid route data found:', responseData);
        alert("No direct bus routes found between these locations");
        setBusRoute(null);
      }

    } catch (error) {
      console.error('Error fetching bus stops:', error);
      alert(error.message || 'Failed to fetch bus route information');
      setBusRoute(null);
    }
  };

  const fetchAttractionPlan = async (coords) => {
    if (!coords) return;

    setIsLoading(true);
    try {
      const [lat, lng] = coords;
      const url = new URL('http://localhost:8000/api/geo/attraction_plan/');
      url.searchParams.append('lat', lat);
      url.searchParams.append('long', lng);
      url.searchParams.append('max_places', 5);

      const response = await fetch(url, {
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
      setAttractionPlan(data);

      // Update markers for the planned attractions
      const planMarkers = data.itinerary.map(item => ({
        position: [item.place.latitude, item.place.longitude],
        name: item.place.name
      }));
      setResultMarkers(planMarkers);

    } catch (error) {
      console.error('Error fetching attraction plan:', error);
      alert('Failed to fetch attraction plan');
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
          display: 'flex',
          gap: '10px',
          marginLeft: '20px'
        }}>
          <button
            onClick={() => setActiveTab('map')}
            style={{
              backgroundColor: activeTab === 'map' ? '#1a73e8' : 'transparent',
              color: activeTab === 'map' ? 'white' : '#1a73e8',
              border: '1px solid #1a73e8',
              borderRadius: '4px',
              padding: '8px 16px',
              cursor: 'pointer',
              fontSize: '14px',
              fontWeight: '500'
            }}
          >
            Map
          </button>
          <button
            onClick={() => setActiveTab('analytics')}
            style={{
              backgroundColor: activeTab === 'analytics' ? '#1a73e8' : 'transparent',
              color: activeTab === 'analytics' ? 'white' : '#1a73e8',
              border: '1px solid #1a73e8',
              borderRadius: '4px',
              padding: '8px 16px',
              cursor: 'pointer',
              fontSize: '14px',
              fontWeight: '500'
            }}
          >
            Analytics
          </button>
        </div>

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
              setResultMarkers([]);
              setSearchResults([]);
              setAttractionPlan(null); // Reset attraction plan
              if (selectedLocation) {
                if (e.target.value === "attraction_plan") {
                  fetchAttractionPlan(selectedLocation);
                } else {
                  handleSearch(selectedLocation, e.target.value);
                }
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
            <option value="attraction_plan">Attraction Plan</option>
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

      {activeTab === 'map' ? (
        <div style={{ flex: 1, display: "flex", gap: "20px", padding: "20px" }}>
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
                  eventHandlers={{
                    click: () => {
                      fetchBusStops(marker.position[0], marker.position[1]);
                    }
                  }}
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

                      {searchResults[index]?.description && (
                        <p style={{
                          margin: '4px 0',
                          fontSize: '14px',
                          color: '#5f6368'
                        }}>{searchResults[index].description}</p>
                      )}

                      {busRoute && (
                        <div style={{
                          margin: '8px 0',
                          padding: '12px',
                          backgroundColor: '#f8f9fa',
                          borderRadius: '8px',
                          border: '1px solid #e8eaed'
                        }}>
                          <div style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px',
                            marginBottom: '8px',
                            borderBottom: '1px solid #e8eaed',
                            paddingBottom: '8px'
                          }}>
                            <span style={{
                              backgroundColor: '#1a73e8',
                              color: 'white',
                              padding: '4px 8px',
                              borderRadius: '4px',
                              fontSize: '14px',
                              fontWeight: '500'
                            }}>
                              Route {busRoute.route_number}
                            </span>
                            <span style={{
                              color: '#3c4043',
                              fontSize: '14px',
                              fontWeight: '500'
                            }}>
                              {busRoute.route_name}
                            </span>
                          </div>

                          <div style={{
                            fontSize: '13px',
                            color: '#5f6368',
                            display: 'flex',
                            flexDirection: 'column',
                            gap: '8px'
                          }}>
                            <div style={{
                              display: 'flex',
                              alignItems: 'center',
                              gap: '4px'
                            }}>
                              <span style={{ color: '#1a73e8' }}>🚌</span>
                              Type: {busRoute.route_type} ({busRoute.category})
                            </div>

                            <div style={{
                              backgroundColor: 'white',
                              padding: '8px',
                              borderRadius: '4px',
                              border: '1px solid #e8eaed'
                            }}>
                              <div style={{ marginBottom: '8px' }}>
                                <div style={{ fontWeight: '500', color: '#1a73e8', marginBottom: '4px' }}>
                                  Origin Stop
                                </div>
                                <div>Stop #{busRoute.origin.stop_number}</div>
                                <div>{busRoute.origin.name}</div>
                                <div style={{ color: '#80868b', fontSize: '12px' }}>
                                  {busRoute.origin.distance} miles away
                                </div>
                              </div>

                              <div style={{
                                width: '100%',
                                height: '1px',
                                backgroundColor: '#e8eaed',
                                margin: '8px 0'
                              }} />

                              <div>
                                <div style={{ fontWeight: '500', color: '#1a73e8', marginBottom: '4px' }}>
                                  Destination Stop
                                </div>
                                <div>Stop #{busRoute.destination.stop_number}</div>
                                <div>{busRoute.destination.name}</div>
                                <div style={{ color: '#80868b', fontSize: '12px' }}>
                                  {busRoute.destination.distance} miles away
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      )}

                      <div style={{
                        fontSize: '13px',
                        color: '#3c4043',
                        marginTop: '8px'
                      }}>
                        {searchResults[index]?.address && (
                          <p style={{
                            margin: '4px 0',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '4px'
                          }}>
                            📍 {searchResults[index].address}
                            ({searchResults[index]?.distance?.toFixed(2) || 'N/A'} miles)
                          </p>
                        )}

                        {searchResults[index]?.types && (
                          <p style={{
                            margin: '4px 0',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '4px'
                          }}>
                            🏷️ {searchResults[index].types}
                          </p>
                        )}

                        {searchResults[index] && (
                          <p style={{
                            margin: '4px 0',
                            fontSize: '12px',
                            color: '#80868b'
                          }}>
                            📌 {searchResults[index].latitude.toFixed(6)}, {searchResults[index].longitude.toFixed(6)}
                          </p>
                        )}
                      </div>
                    </div>
                  </Popup>
                </Marker>
              ))}

              {busRoute && busRoute.geometry && (
                <>
                  <Marker
                    position={[busRoute.origin.coordinates[1], busRoute.origin.coordinates[0]]}
                    icon={busIcon}
                  >
                    <Popup>
                      <div style={{ padding: '8px', minWidth: '200px' }}>
                        <h3 style={{ margin: '0 0 8px 0', color: '#1a73e8', fontSize: '16px' }}>
                          Starting Bus Stop
                        </h3>
                        <p style={{ margin: '4px 0', fontSize: '14px' }}>
                          🚌 Line: {busRoute.route_number}
                        </p>
                        <p style={{ margin: '4px 0', fontSize: '14px' }}>
                          Name: {busRoute.origin.name}
                        </p>
                        <p style={{ margin: '4px 0', fontSize: '12px', color: '#666' }}>
                          📍 Distance: {busRoute.origin.distance.toFixed(2)} miles
                        </p>
                      </div>
                    </Popup>
                  </Marker>

                  <Marker
                    position={[busRoute.destination.coordinates[1], busRoute.destination.coordinates[0]]}
                    icon={busIcon}
                  >
                    <Popup>
                      <div style={{ padding: '8px', minWidth: '200px' }}>
                        <h3 style={{ margin: '0 0 8px 0', color: '#1a73e8', fontSize: '16px' }}>
                          Destination Bus Stop
                        </h3>
                        <p style={{ margin: '4px 0', fontSize: '14px' }}>
                          🚌 Line: {busRoute.route_number}
                        </p>
                        <p style={{ margin: '4px 0', fontSize: '14px' }}>
                          Name: {busRoute.destination.name}
                        </p>
                        <p style={{ margin: '4px 0', fontSize: '12px', color: '#666' }}>
                          📍 Distance: {busRoute.destination.distance.toFixed(2)} miles
                        </p>
                      </div>
                    </Popup>
                  </Marker>

                  <Polyline
                    pathOptions={{ color: '#000000', weight: 5, opacity: 1 }}
                    positions={busRoute.geometry.map(([lng, lat]) => [lat, lng])}
                  />
                </>
              )}
            </MapContainer>
          </div>

          {(searchResults.length > 0 || (searchType === 'attraction_plan' && attractionPlan)) && (
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
                  }}>
                    {searchType === 'attraction_plan' ? 'Attraction Plan' : 'Search Results'}
                  </h3>
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

              {isPanelVisible && (
                <>
                  {searchType === 'attraction_plan' && attractionPlan ? (
                    <>
                      <div style={{ marginBottom: '12px', color: '#5f6368', fontSize: '14px' }}>
                        Total Duration: {(() => {
                          const hours = parseFloat(attractionPlan.total_duration.split(' ')[0]);
                          const fullHours = Math.floor(hours);
                          const minutes = Math.round((hours - fullHours) * 60);
                          return `${fullHours}h ${minutes}m`;
                        })()}
                      </div>
                      {attractionPlan.itinerary.map((item, index) => (
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
                            {index + 1}. {item.place.name}
                          </div>
                          <div style={{
                            color: '#5f6368',
                            fontSize: '13px',
                            display: 'flex',
                            flexDirection: 'column',
                            gap: '4px'
                          }}>
                            <div>⏰ {item.start_time} - {item.end_time}</div>
                            <div>⌛ Duration: {(() => {
                              const hours = parseFloat(item.suggested_duration.split(' ')[0]);
                              const fullHours = Math.floor(hours);
                              const minutes = Math.round((hours - fullHours) * 60);
                              return fullHours > 0
                                ? minutes > 0
                                  ? `${fullHours}h ${minutes}m`
                                  : `${fullHours}h`
                                : `${minutes}m`;
                            })()}</div>
                            <div>📍 Distance: {item.place.distance_from_start.toFixed(2)} miles</div>
                            {item.place.address && <div>🏠 {item.place.address}</div>}
                            {item.place.description && <div>ℹ️ {item.place.description}</div>}
                          </div>
                        </div>
                      ))}
                    </>
                  ) : (
                    // Existing search results display
                    searchResults.map((result, index) => (
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
                          <div>📍 Distance: {result.distance?.toFixed(2) || 'N/A'} miles</div>
                          {result.address && <div>🏠 Address: {result.address}</div>}
                        </div>
                      </div>
                    ))
                  )}
                </>
              )}
            </div>
          )}
        </div>
      ) : (
        <Analytics />
      )}

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