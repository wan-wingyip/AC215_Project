// ./app/page.js

// set processing to client side
'use client'

// get environment variables
require('dotenv').config();

// import dependencies
import styles from './page.module.css'
import React, { useEffect, useState } from 'react';

// import custom components
import Banner from './components/Banner';
import SearchBar from './components/SearchBar';
import Property from './components/Property';
import NavBar from './components/NavBar';

// import util functions
import {fetchPropertyList} from './util/realEstateApi';
import { fetchLabels } from './util/inferenceContainerApi';
import {removeDuplicateIds} from './util/removeDuplicateIds';


// Home page component
function Home() {
  // const to store properties and labels for display
  const [properties, setProperties] = useState([]);
  const [labels, setLabels] = useState({});

  // const to store text for status message
  const [status, setStatus] = useState('Welcome! Please enter a zip code to get started.');


  // when search is clicked, fetch properties and labels
  const handleSearch = async (zipcode) => {
    setStatus('Looking for properties that match your criteria...');

    // Check if data for this zip code is already stored in Local Storage
    const storedData = localStorage.getItem(zipcode);
    if (storedData) {
      const { properties, labels } = JSON.parse(storedData);
      setProperties(properties);
      setLabels(labels);
      console.log('Data loaded from local storage:', properties, labels);
      setStatus('Properties and labels loaded successfully. Please scroll down to view properties and labels.');
      return;
    }

    // fetch properties and labels via API
    try {
      const response = await fetchPropertyList(zipcode);
      const data = response.data.home_search.results;

      if (data.length === 0) {
        // If no properties are found
        setStatus("No properties for sale for requested zip code. It is rough out here...");
        setProperties([]); // Clear any previous properties
        return; // Exit the function early
      }

      // filter out duplicates properties
      const uniqueProperties = removeDuplicateIds(data);

      // display properties first
      setProperties(uniqueProperties);  
      setStatus('Properties found! Now fetching labels from AI model... ~15 seconds');


      // Await the completion of fetchLabels and then set labels
      const labelsData = await fetchLabels(uniqueProperties);
      setLabels(labelsData); // Update the labels state with the data received
      setStatus('Properties and labels loaded successfully. Please scroll down to view properties and labels.');

      // save properties and labels to local storage
      localStorage.setItem(zipcode, JSON.stringify({ properties: uniqueProperties, labels: labelsData }));

    } catch (error) {
      
      // handle error
      console.error('Error fetching data: ', error);
      setStatus('Failed to load data. Please try again.');
    }
  };


  // render home page
  return (
    <main className={styles.main}>
      <div className={styles.bannerContainer}>
        <Banner 
          title="Find your next home"
          buttonText="Explore buying"
          buttonUrl="/search?purpose=for-sale"
          imageUrl="https://www.zillowstatic.com/bedrock/app/uploads/sites/5/2023/07/womanonporch_nationalbrand_1920w.jpg"
        />
        <div className={styles.searchOverlay}>
          <SearchBar onSearch={handleSearch} className={styles.SearchBar} />
        </div>
      </div>

      {properties.length === 0 ? (
        <div className={styles.noResults}>
          <h1>Getting Started</h1>
          <br/>
          <p>{status}</p>
          <br/>
          <p>For demo purposes, the following zip codes have fixer-uppers:</p>
          <p>95122, 48211</p>
        </div>
      ) : (
        <div className={styles.resultsContainer}>
          <h1>Search Results</h1>
          <p> {status} </p>
          <br/>
          <div className={styles.propertyGrid}>
            {properties.map(property => (
              <Property 
                key={property.property_id} 
                property={property} 
                label = {labels[property.property_id]}/>
            ))}
          </div>
        </div>
      )}

    </main>
  );
}

export default Home;
