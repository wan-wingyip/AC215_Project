#!/bin/bash

# update the VM
sudo apt-get update

# download docker sh to the VM
sudo apt install docker.io 

# Add name to group
# Change to your username!
sudo usermod -a -G docker faisalk_karim3

# check if user has been added
grep docker /etc/group

# change user's group ID to docker (to avoid having to log out and log in again)
newgrp docker

# make an empty secrets folder for later
mkdir /secrets

# give read write access to folder
chmod a+rwx /secrets