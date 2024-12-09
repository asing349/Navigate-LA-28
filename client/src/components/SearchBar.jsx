import React from "react";
import PropTypes from "prop-types";
import "../styles/SearchBar.css"; // Importing the CSS file

const SearchBar = ({
  searchQuery,
  setSearchQuery,
  searchType,
  setSearchType,
}) => (
  <div className="search-bar">
    <input
      type="text"
      value={searchQuery}
      onChange={(e) => setSearchQuery(e.target.value)}
      placeholder="Search..."
      className="search-input"
    />
    <select
      value={searchType}
      onChange={(e) => setSearchType(e.target.value)}
      className="search-select"
    >
      <option value="query1">Query 1</option>
      <option value="query2">Query 2</option>
      <option value="query3">Query 3</option>
    </select>
    <button className="search-button">Search</button>
  </div>
);

SearchBar.propTypes = {
  searchQuery: PropTypes.string.isRequired,
  setSearchQuery: PropTypes.func.isRequired,
  searchType: PropTypes.string.isRequired,
  setSearchType: PropTypes.func.isRequired,
};

export default SearchBar;
