import React, { useState } from 'react';
import './SearchBar.css';

const SearchBar = ({ onSearch }) => {
    const [zipcode, setZipcode] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        onSearch(zipcode);
    };

    return (
        <div className="searchBar">
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Enter a zip code to get started"
                    value={zipcode}
                    onChange={(e) => setZipcode(e.target.value)}
                />
                <button type="submit">Search</button>
            </form>
        </div>
    );
};

export default SearchBar;
