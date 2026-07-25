pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REGISTRY = '488179516441.dkr.ecr.us-east-1.amazonaws.com'
        ECR_REPO = 'python-microservice'
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

        // stage('Checkout') {
        //     steps {
        //         // Checkout the code from the repository
        //         git checkout 'https://github.com/pavan193/python-microsevice-k8.git'
        //     }
        // }

        stage('Build Docker Image') {
            steps {
                sh '''
                echo "Current directory:"
                pwd

                echo "Files:"
                ls -la

                echo "Directories:"
                find . -maxdepth 2 -type d
                '''
                // Build the Docker image
                sh 'docker build -t frontendimage ./python-microservice/frontend/'
                sh 'docker build -t employeeserviceimage ./python-microservice/employee-service/'
                sh 'docker build -t projectserviceimage ./python-microservice/project-service/'
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
                    docker tag frontendimage:latest ${ECR_REGISTRY}/${ECR_REPO}:frontendapp-latest
                    docker tag employeeserviceimage:latest ${ECR_REGISTRY}/${ECR_REPO}:employeedb-latest
                    docker tag projectserviceimage:latest ${ECR_REGISTRY}/${ECR_REPO}:projectdb-latest
                '''
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                    docker push ${ECR_REGISTRY}/${ECR_REPO}:frontendapp-latest
                    docker push ${ECR_REGISTRY}/${ECR_REPO}:employeedb-latest
                    docker push ${ECR_REGISTRY}/${ECR_REPO}:projectdb-latest
                '''
            }
        }
    }
}