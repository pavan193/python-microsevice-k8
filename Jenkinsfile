pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REGISTRY = '488179516441.dkr.ecr.us-east-1.amazonaws.com'
        ECR_REPO = 'python-microservice'
    }

    stages {
        stage('Build images') {
            steps {
                sh 'docker build -t frontend:practice ./frontend'
                sh 'docker build -t employee-service:practice ./employee-service'
            }
        }

        stage('Log in to ECR') {
            steps {
                sh '''
                    aws ecr get-login-password --region ${AWS_REGION} |
                    docker login --username AWS --password-stdin ${ECR_REGISTRY}
                '''
            }
        }

        stage('Push images') {
            steps {
                sh '''
                    docker tag frontend:practice ${ECR_REGISTRY}/${ECR_REPO}:frontend-practice
                    docker tag employee-service:practice ${ECR_REGISTRY}/${ECR_REPO}:employee-service-practice

                    docker push ${ECR_REGISTRY}/${ECR_REPO}:frontend-practice
                    docker push ${ECR_REGISTRY}/${ECR_REPO}:employee-service-practice
                '''
            }
        }

        stage('Deploy to EC2') {
            steps {
                sh '''
                    docker pull ${ECR_REGISTRY}/${ECR_REPO}:employee-service-practice
                    docker pull ${ECR_REGISTRY}/${ECR_REPO}:frontend-practice

                    docker rm -f practice-employee-service || true
                    docker run -d \
                      --name practice-employee-service \
                      --network devops-practice-net \
                      --restart unless-stopped \
                      --env-file /etc/devops-practice/rds.env \
                      -e DB_HOST=employee-db-practice.csha86ws6flz.us-east-1.rds.amazonaws.com \
                      -e DB_PORT=5432 \
                      -e DB_NAME=employee_db \
                      ${ECR_REGISTRY}/${ECR_REPO}:employee-service-practice

                    docker rm -f practice-frontend || true
                    docker run -d \
                      --name practice-frontend \
                      --network devops-practice-net \
                      --restart unless-stopped \
                      -e EMPLOYEE_SERVICE_URL=http://practice-employee-service:5001 \
                      -p 8080:5000 \
                      ${ECR_REGISTRY}/${ECR_REPO}:frontend-practice
                '''
            }
        }
    }
}

// OLD Jenkins File content:

// pipeline {
//     agent any

//     environment {
//         AWS_REGION = 'us-east-1'
//         ECR_REGISTRY = '488179516441.dkr.ecr.us-east-1.amazonaws.com'
//         ECR_REPO = 'python-microservice'
//     }

//     stages {
//         stage('Clean and Checkout') {
//             steps {
//                 cleanWs()
//                 checkout scm
//             }
//         }

//         // stage('Checkout') {
//         //     steps {
//         //         // Checkout the code from the repository
//         //         git checkout 'https://github.com/pavan193/python-microsevice-k8.git'
//         //     }
//         // }

//         stage('Build Docker Image') {
//             steps {
//                 // sh 'echo Current directory:'
//                 // sh 'pwd'

//                 // sh 'echo Files:'
//                 // sh 'ls -la'

//                 // sh 'echo Directories:'
//                 // sh 'find . -maxdepth 2 -type d'
//                 // Build the Docker image
//                 sh 'docker build -t frontendimage ./frontend/'
//                 sh 'docker build -t employeeserviceimage ./employee-service/'
//                 sh 'docker build -t projectserviceimage ./project-service/'
//             }
//         }
//         stage('Login to ECR') {
//             steps {
//                 sh '''
//                     aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
//                 '''
//             }
//         }

//         stage('Tag Docker Image') {
//             steps {
//                 sh '''
//                     docker tag frontendimage:latest ${ECR_REGISTRY}/${ECR_REPO}:frontendapp-latest
//                     docker tag employeeserviceimage:latest ${ECR_REGISTRY}/${ECR_REPO}:employeedb-latest
//                     docker tag projectserviceimage:latest ${ECR_REGISTRY}/${ECR_REPO}:projectdb-latest
//                 '''
//             }
//         }

//         stage('Push to ECR') {
//             steps {
//                 sh '''
//                     docker push ${ECR_REGISTRY}/${ECR_REPO}:frontendapp-latest
//                     docker push ${ECR_REGISTRY}/${ECR_REPO}:employeedb-latest
//                     docker push ${ECR_REGISTRY}/${ECR_REPO}:projectdb-latest
//                 '''
//             }
//         }
//     }
// }
