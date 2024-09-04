pipeline {
    agent any // This can be replaced with a specific label if needed

    environment {
        REGISTRY = 'host.docker.internal:5001' // Replace with your registry address
        IMAGE_NAME = 'python-etl-cv'
        TAG = 'latest'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    try {
                        docker.withRegistry('http://host.docker.internal:5001/') {
                            sh 'docker compose build --no-cache'
                            sh "docker tag ${IMAGE_NAME}:${TAG} ${REGISTRY}/${IMAGE_NAME}:${TAG}"
                            sh "docker push ${REGISTRY}/${IMAGE_NAME}:${TAG}"
                        }
                    } catch (Exception e) {
                        error "Build failed: ${e.message}"
                    }
                }
            }
        }
        stage('Cleanup') {
            steps {
                sh 'docker image prune -f'
                sh 'docker container prune -f'
            }
        }
    }
}