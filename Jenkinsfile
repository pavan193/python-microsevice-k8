pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REGISTRY = '488179516441.dkr.ecr.us-east-1.amazonaws.com'
        ECR_REPO = 'python-microservice'
    }

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
                sh 'docker build -t employeeserviceimage ./employee-service/'
                sh 'docker build -t projectserviceimage ./project-service/'
            }
        }
        stage('Login to ECR') {
            steps {
                sh '''
                    aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                '''
            }
        }

        stage('Tag Docker Image') {
            steps {
                sh '''
                    docker tag frontendimage:${BUILD_NUMBER} ${ECR_REGISTRY}/frontendimage:${BUILD_NUMBER}
                    docker tag employeeserviceimage:${BUILD_NUMBER} ${ECR_REGISTRY}/employeeserviceimage:${BUILD_NUMBER}
                    docker tag projectserviceimage:${BUILD_NUMBER} ${ECR_REGISTRY}/projectserviceimage:${BUILD_NUMBER}
                '''
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                    docker push ${ECR_REGISTRY}/frontendimage:${BUILD_NUMBER}
                    docker push ${ECR_REGISTRY}/employeeserviceimage:${BUILD_NUMBER}
                    docker push ${ECR_REGISTRY}/projectserviceimage:${BUILD_NUMBER}
                '''
            }
        }
    }
}