#!/bin/bash

# download docker sh to VM
curl -fsSL https://get.docker.com -o get-docker.sh

# run sh get-docker.sh download script
sudo sh get-docker.sh

# Add name to group
# Change to your username!
sudo usermod -a -G docker evw754

# check user has been added
grep docker /etc/group

# change user's group ID to docker (to avoid having to log out and log in again)
newgrp docker

# check docker access
docker run hello-world



