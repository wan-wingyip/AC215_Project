// Navbar.jsx

import React from 'react';
import './NavBar.css'; // Importing the CSS file for styling

const Navbar = () => {
    return (
        <nav className="navbar">
            <div className="navbar-logo">
                Rehab.ai
            </div>
            <div className="navbar-links">
                <a href="https://medium.com/@tonyhua1/using-ai-to-discover-fixer-upper-deals-97a74f3a306c">About</a>
                <a href="https://github.com/tonyhua18/AC215_rehab_image_detection_ai">GitHub Repo</a>
            </div>
        </nav>
    );
};

export default Navbar;