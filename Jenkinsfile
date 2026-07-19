pipeline {
    agent any

    stages {
        // stage('Checkout') {
        //     steps {
        //         // Checkout the code from the repository
        //         git checkout 'https://github.com/pavan193/python-microsevice-k8.git'
        //     }
        // }
        stage('Build Docker Image') {
            steps {
                // Build the Docker image
                sh 'docker build -t frontendimage ./frontend/'
                sh 'docker build -t employeeserviceimage ./employeeservice/'
                sh 'docker build -t projectserviceimage ./projectservice/'
            }
        }
        stage('push Docker Image') {
            steps {
                // Push the Docker image to a registry (e.g., ECR, Docker Hub)
                echo 'Pushing Docker images to registry...'
            }
        }
    }
}