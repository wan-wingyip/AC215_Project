# AC215- Rehab Image Detection AI

- [Presentation Video](#Presentation-Video)
- [Project Organization](#Project-Organization)
- [AC215 Final Project - Rehab AI](#Introduction)
- [Project Pipeline](#project-pipeline)
- [Getting Started](#getting-started)
- [License](#license)


### Presentation Video
- [Link to Youtube Demo](https://youtu.be/GhD88KlUKAE)

### Blog Post Link
- [Link to Medium Blog](https://medium.com/@tonyhua1/using-ai-to-discover-fixer-upper-deals-97a74f3a306c)

### Link to Demo our live MVP webapp!
Experience our live app by visiting: [Rehab AI Webapp](http://34.41.217.17/)


## Project Organization
```
.
|--.github
|  |--workflows
|     |--ci-cd.yaml
|--scripts
|     |--....
|--Old Readmes                  <----- Readme files from previous milestones
|  |--....
|--src
|  |--rough notebooks           <----- rough notebooks for fetching data/ preprocessing and training.
|     |--....
|  |--K8S
|     |--deployment.yaml.old
|     |--fixer-upper-deploy.yaml
|     |--fixer-upper-env.yaml
|     |--fixer-upper-lb-svc.yaml
|  |--c1-data-scraping          <----- This container scrapes images and stores them in Google storage buckets
|     |--....
|  |--c2-data-labeling          <----- This container is not used in our project (meant for labeling)
|     |--....
|  |--c2-preprocessing          <----- This creates tf records, dvc and gets data ready for modeling
|     |--....
|  |--c3-model-training         <----- This trains the model and stores weights in WandB
|     |--....
|  |--c4-model-inference        <----- This is the production back end, it received images predicts.
|     |--....
|  |--c5-frontend-ui            <----- This has the code for front end.
|     |--....
|  |--vertex-ai-deployment      <----- Code for deploying model on vertex-ai
|     |--....
|--.gitattributes
|--.gitignore
|--LICENSE
|--README.md 


```
# AC215 Final Project - Rehab AI

## Project Team
*Team members:* Evan Wan, Faisal Karim, Yaseen Khan Mohmand, Michael Leung, Tony Hua, Alvaro Ramirez

*Group name:* Rehab AI

*Problem Definition:* The real estate market currently lacks a specialized tool that assists potential buyers in distinguishing between fixer-upper homes and renovated properties. 

## Data Description:

For our training dataset we scrape images from Craigslist, we use the keywords, fixer-upper to identify houses that are fixer upper and we use the keywords renovated to images of houses that are not fixer upper. Please note that the keywords are not a replacement for our solution because the availability of these keywords are dependent on the person who creates the listing.

Our training dataset has images from 1300 properties that are fixer uppers and 2000 properties that are renovated. Each property has around 8.4 images on average, so we have a total of 27 thousand images.

In the production setting our images are feteched directly from the zillow api for the relevant zip codes.

## Proposed Solution: 

To address the gap as defined in the problem definition, we have developed an innovative platform. This user-friendly platform allows users to enter a specific zip code, which then provides them with a curated list properties in the area, with with labels that mention whether the house is a fixer-upper home or not. Our approach utilizes a Convolutional Neural Network (CNN) model. This model intelligently analyzes and interprets images from house listings, enabling it to accurately identify properties that are fixer-uppers. This tool not only simplifies the search process for buyers but also offers a unique solution in the realm of real estate property categorization.

![Rehab AI](/previous_readmes/image.png)

### Technical Architecture

![Rehab AI](/previous_readmes/Technical_Architecture.png)

### Deployment

![Rehab AI](/previous_readmes/deployment.jpg)

### Code Structure
The following are the containers we've built:

### Container1 - Training Data Scraper

**Role**: Scrapes images of renovated and un-renovated homes from Craigslist for model training.
- **Source**: Craigslist, we use keywords to identify fixer uppers and renovated houses.
- **Output**: Saves images to Google Cloud Bucket in the `fixer-upper/` and `renovated/` folders.

[Detailed readme for container 1](https://github.com/tonyhua18/AC215_rehab_image_detection_ai/blob/main/src/c1-data-scraping/readme.md)

### Container2a - Image Labeling (We do not use this in our project)

**Role**: Pulls images for manual labeling and saves them back labeled in the case that we have unlabeled data. Currently, we are using a labeled dataset so this container is on standby.
- **Input**: Pulls the unlabeled images from Google Cloud Bucket.
- **Output**: Saves to a folder of labeled images in Google Cloud Bucket.


### Container2c - Data Preprocessing & Versioning

**Role**: Resizes images to correct dimensions for CNN Model Architecture and manages versioning for labeled data to keep track of changes.
- **Input**: Pulls unprocessed images from `fixer-upper/` and `renovated/` in Google Cloud Bucket.
- **Output**: Saves resized images to `fixer-upper/` and `renovated/` in Google Cloud Bucket. Dataset version is incremented by 1 (e.g. v1, v2, v3, etc) and tracked in a data registry folder `dvc-store/` on Google Cloud bucket, using the open-source DVC software.
- **Output**: Creates TFrecords for faster loading to model training container

[Detailed readme for container 2c](https://github.com/tonyhua18/AC215_rehab_image_detection_ai/blob/main/src/c2-preprocessing/readme.md)

### Container3 - CNN Model Training

**Role**: Trains the CNN model to identify fixer-upper homes using the labeled images.
- **Input**: Pulls images from `fixer-upper/` and `renovated/` in Google Cloud Bucket.
- **Output**: Trained model.

[Detailed readme for container 3](https://github.com/tonyhua18/AC215_rehab_image_detection_ai/blob/main/src/c3-model-training/readme.md)


### Container4 - Model Inference and API service

**Role**: This container is pivotal as it hosts our most accurately trained model. Additionally, it provides an API interface for accessing the model's capabilities.
- **Input**: Receives unseen property images corresponding to user-selected zip codes. These images are sourced and delivered by Container5.
- **Output**: Processes the images for a property and applies labels to each, categorizing them as either 'renovated' or 'fixer-upper'. 

[Detailed readme for container 4](https://github.com/tonyhua18/AC215_rehab_image_detection_ai/blob/main/src/c4-model-inference/README.md)


### Container5 - Front End UI

**Role**: This container functions as the front-end interface, representing the website that our visitors interact with.
- **Input**: End users input a zip code to initiate a search for properties.
- **Output**: The website generates and displays a curated list of homes within the specified area. Each property is distinctly labeled, categorizing it as either a 'fixer-upper' or 'renovated' to facilitate user decision-making.

[Detailed readme for container 5](https://github.com/tonyhua18/AC215_rehab_image_detection_ai/blob/main/src/c5-frontend-ui/readme.md)

### Kubernetes Container
**Role**: This folder explains our kubernetes cluster architecture, and also shows the steps of kubernetes deployment. It also has a short example for ansible.

[Detailed readme for kubernetes cluster]()





# How to use
To test our live web app, please visit this link here!: [Rehab AI Webapp](http://34.41.217.17/)


## Automated model training workflow w/ Vertex AI
Our project is designed with an Vertex AI pipeline to simplify model training workflows as well. To read more on how to deploy our pipeline and use it, please see our detailed readme in the `./src/vertex-ai-deployment/` directory.

On a high level, our Vertex AI workflow allows data scientists and ML OPs teams to quickly instantiate or automate data collection, preprocessing, and model training all from a single python terminal interface. 

The different microservices for the pipeline can be hosted and have endpoints exposed, allowing users to simply call an enpoint to have an action performed. Easy as that!

Some of the supported commands and actions are:
```bash
# to scrape images only
python cli.py -s

# to preprocess images only
python cli.py -p

# to train model only
python cli.py -t

# to run entire pipeline from scraping to model-training
python cli.py -all
```




## Automated deployment to Kubernetes w/ Ansible
Our final application is designed to be deployed to Google's Kubernetes Cluster for automated scaling and hosting. To push a deployment, we've created a pipeline with the steps detailed in our `./src/k8s-ansible` folder!

As a very high level overview, we designed a dual load-balancer solution, exposing our front-end application to the outside world and our back-end inferencing API as well. This enables us to both serve our own website, but also invite possible 3rd path developers to collaborate in the future.


## CI/CD with Github Actions
One extremely versatile component of our app is our CI/CD pipeline built with Github Actions! 

For every push and commit made to our repository by developers, optional commands could be instantiated to kickstart workflows!

The following are some of the commands supported by our CI/CD pipeline. Developers can append these commands to the end of their commit messages when pushing code, to kickstart automated unit testing, or docker container builds!

```bash
/test
/build
    /build-1
    /build-2
    /build-3
    /build-4.. etc
/deploy
```

For more information on what workflows are supported, please take a look at our `./github/workflows/` directory to see all the supported commands and actions, and the yaml file to configure such workflows!

