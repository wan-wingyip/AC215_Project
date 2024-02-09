#!/bin/bash

# docker-entrypoint.sh to execute INSIDE the container AFTER the container is started

echo "Container is running!!!"
echo "Starting the frontend server..."

# once inside the container, start the frontend server
npm run dev

echo "Frontend server started successfully!"