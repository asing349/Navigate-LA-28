import React from "react";
import PropTypes from "prop-types";
import { MapContainer, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import LocationMarker from "./LocationMarker";

const MapContainerComponent = ({ onLocationSelect }) => (
  <MapContainer
    center={[34.0522, -118.2437]}
    zoom={13}
    style={{ height: "100%", width: "100%" }}
  >
    <TileLayer
      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      attribution="&copy; OpenStreetMap contributors"
    />
    <LocationMarker onLocationSelect={onLocationSelect} />
  </MapContainer>
);
MapContainerComponent.propTypes = {
  onLocationSelect: PropTypes.func.isRequired,
};

export default MapContainerComponent;
