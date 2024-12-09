import React, { useState } from "react";
import PropTypes from "prop-types";
import { Marker, useMapEvents } from "react-leaflet";

const LocationMarker = ({ onLocationSelect }) => {
  const [position, setPosition] = useState(null);

  useMapEvents({
    click(e) {
      const { lat, lng } = e.latlng;
      setPosition([lat, lng]);
      onLocationSelect([lat, lng]);
    },
  });

  return position ? <Marker position={position} /> : null;
};
LocationMarker.propTypes = {
  onLocationSelect: PropTypes.func.isRequired,
};

export default LocationMarker;
