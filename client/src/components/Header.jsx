import React from "react";
import PropTypes from "prop-types";
import "../styles/Header.css";

const Header = ({ username, onLoginToggle }) => (
  <div className="header">
    <h1 className="header-title">Navigate LA</h1>
    <div className="header-actions">
      {username && <span className="username">{username}</span>}
      <button onClick={onLoginToggle} className="auth-button">
        {username ? "👤" : "🔑"}
      </button>
    </div>
  </div>
);

Header.propTypes = {
  username: PropTypes.string,
  onLoginToggle: PropTypes.func.isRequired,
};

export default Header;
