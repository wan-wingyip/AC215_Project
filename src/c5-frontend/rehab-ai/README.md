# Rehab AI Frontend

## Overview

**Rehab AI Frontend** is a cutting-edge ReactJS-based web application designed to revolutionize the real estate search experience. This intuitive platform enables users to discover real estate properties within specific zip codes effortlessly.

### Key Features
- **Zip Code-Based Search:** Users can search for properties by simply entering a zip code.
- **Real Estate Marketplace API Integration:** The frontend connects seamlessly with a comprehensive real estate API, ensuring an extensive listing of properties.
- **Advanced ML Computer Vision:** Our backend incorporates a sophisticated machine learning model that analyzes property images, classifying them as either "fixer-upper" or "renovated". This feature significantly aids buyers in narrowing down their search for the ideal home.




## Usage Instructions

### Live Demonstration
Experience our live app by visiting: [Rehab AI Webapp](http://34.41.217.17/)


### Local Deployment (For Testing)

#### Setting Up the Development Server
1. Clone the repository and navigate to the root directory (this readme's directory).
2. Execute the following command to start the development server in test mode:
   ```bash
   npm run dev
   ```
3. Access your test server at http://localhost:3000.

### Production Deployment

### Pushing to DockerHub and Google Artifact Registry
- To push to dockerhub and google artifact registry, add the command `/build` when pushing a new commit. This CICD command automatically builds a docker container, and pushes the image to DockerHub and Google Artiface Repository

### Launching a VM instance
- To deploy, add the command `/deploy` when pushing a new commit. This CICD command automatically pulls the image from Google's Artifact Registry and deploys a new K8s deployment for the image. If an front end image is not already present, then the `/test` and `/build` steps of the CICD pipeline will automatically run prior to deployment.

## Making Modifications
- Homepage Code: Edit `app/page.js` for changes to the homepage.
- Layout Customization: Modify `app/layout.js` for layout adjustments.
- Reusable Components: `app/components` contains elements like Navbars, banners, buttons, etc.
- Utility Functions: `app/util` houses essential functions, including API calls and validation scripts.
- Styling: Alter `app/css` for design and styling modifications.

## How the app works
- App takes user input in the form of a `5 digit zip code`
- App sends a request with the zip code to the `Realty.in.US API` and retrieves a list of properties
- Each property has the following attributes:
    - `property_id`
    - `image_url`
    - `price`
    - `address`
    - `number of bedrooms / bathrooms`
    - `sqft`
    - and more..
- The property and its details are rendered for the user
- The `property_id` and `image_url` are sent via a POST request to our `C4 Model Inferencing Backend Server` for prediction
- The model uses computer vision to predict if the home is a fixer-upper or not
- The backend API returns a `fixer-upper or not` boolean, where it is displayed as a flag for users
- The search results are updated with the `fixer-upper flag` for properties that return true.