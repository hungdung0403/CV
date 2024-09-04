@echo off
set MONGO_USERNAME=mongodb
set MONGO_PASSWORD=mongodb123
:: Start MongoDB Docker container
docker run -d --name mongodb -p 27017:27017 ^
  -e MONGO_INITDB_ROOT_USERNAME=%MONGO_USERNAME% ^
  -e MONGO_INITDB_ROOT_PASSWORD=%MONGO_PASSWORD% ^
  mongo:latest

:: Start Selenium Docker container
docker run -d --name selenium -p 4444:4444 selenium/standalone-chrome:127.0-chromedriver-127.0

:: Start Docker Registry Docker container
docker run -d -p 5001:5000 --name registry registry:latest

docker network create jenkins
docker build -t jenkins-blueocean:latest -f Dockerfile.jenkins .
docker run --name jenkins-blueocean --restart=on-failure --detach --network jenkins --env JENKINS_OPTS=" --httpPort=8080 --httpListenAddress=0.0.0.0" --publish 8080:8080 --publish 50000:50000 --volume jenkins-data:/var/jenkins_home --volume /var/run/docker.sock:/var/run/docker.sock --user root jenkins-blueocean:latest

echo "Jenkins Blue Ocean has been started on port 8080"
echo "Services have been started:"
echo "- MongoDB: mongodb://localhost:27017"
echo "- Selenium: http://localhost:4444"
echo "- Docker Registry: http://localhost:5000"