FROM node:current-slim


# Create app directory
WORKDIR /app

# Copy app source code & install production dependencies
COPY . . 
RUN npm install --production

# Export necessary port
EXPOSE 3000

# Give Permisions to execute entrypoint script in the future
RUN ["chmod", "+x", "./docker-entrypoint.sh"]

# Build the production app
RUN npm run build

######################

# Entrypoint to script that runs INSIDE the container if started
ENTRYPOINT ["/bin/bash", "./docker-entrypoint.sh"]



# Dockerfile creates a Docker image. Run command must be used to create a container from the image.
# The docker-run.sh script will be used to run the container from the image.

