// Property.jsx

import React from 'react';
import { FaBed, FaBath } from 'react-icons/fa';
import { BsGridFill } from 'react-icons/bs';
import { GoVerified } from 'react-icons/go';
import { useState, useEffect } from 'react';
import './Property.css'; // Import the CSS file

const Property = ({ property, label }) => {

    // Const to store the fixer-upper label overlay state
    const [showOverlay, setShowOverlay] = useState(false);

    // Function to update the fixer-upper label overlay based on the label
    useEffect(() => {
        // If label is 1, show "Fixer-upper" overlay
        if (label === 1) {
        setShowOverlay(true);
        } else {
        setShowOverlay(false);
        }
    }, [label]); // Only re-run if label changes

    // Function to replace the image URL's ending from 's.jpg' to 'od.jpg'
    const getUpdatedImageUrl = (url) => {
        if (!url) return '';
        return url.replace('s.jpg', 'od.jpg');
    };

    // Updated image URL
    const updatedImageUrl = getUpdatedImageUrl(property.primary_photo.href);

    return (

        <a href={`/property/${property.property_id}`} className="property-link">
            <div className="property-container">
            {showOverlay && <div className="overlay-label">Fixer-upper</div>}
                <div>
                    <img src={updatedImageUrl} className="property-image" alt="property" />
                </div>
                <div className="text-container">
                    <div className="property-price-container">
                        <div className="property-price">
                            <div className="property-verified-icon">{property.flags.is_new_listing && <GoVerified />}</div>
                            <span className="property-price-text">$ {property.list_price}</span>
                        </div>
                    </div>
                    <div className="property-details">
                        {property.description.beds && <div className="property-detail-item"><FaBed /> <span className="property-detail-text">{property.description.beds} Beds</span></div>}
                        {property.description.baths && <div className="property-detail-item"><FaBath /> <span className="property-detail-text">{property.description.baths} Baths</span></div>}
                        {property.description.sqft && <div className="property-detail-item"><BsGridFill /> <span className="property-detail-text">{property.description.sqft} Sq Ft</span></div>}
                    </div>
                    <span className="property-address">
                        {property.location.address.line}, {property.location.address.city}, {property.location.address.state_code}
                    </span>
                </div>
            </div>
        </a>
    );
};

export default Property;
