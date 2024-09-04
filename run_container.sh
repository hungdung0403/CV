#!/bin/bash

# Get the localhost IP address
LOCAL_IP=$(ifconfig | grep "inet " | grep -Fv 127.0.0.1 | awk '{print $2}')

# Pull the latest Docker image from the local registry
docker pull host.docker.internal:5001/python-etl-cv:latest

# Run the Docker container with the specified environment variables
docker run -d --name python-etl-cv \
  -e CHROMEDRIVER_PATH=/usr/local/bin/chromedriver \
  -e WEB_URL=https://timviec365.vn/nguoi-tim-viec.html \
  -e MONGO_URI=mongodb://$LOCAL_IP:27017 \
  -e USERNAME_DB=mongodb \
  -e PASSWORD_DB=mongodb123 \
  -e DOMAIN_SELENIUM=http://$LOCAL_IP:4444/wd/hub \
  python-etl-cv:latest

echo "Container 'python-etl-cv-container' has been started."