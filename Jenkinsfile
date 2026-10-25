pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REGISTRY = '488179516441.dkr.ecr.us-east-1.amazonaws.com'
        ECR_REPO = 'python-microservice'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Build images') {
            when {
                anyOf {
                    changeset 'frontend/**'
                    changeset 'employee-service/**'
                    changeset 'Jenkinsfile'
                }
            }
            steps {
                sh '''
                    docker build -t ${ECR_REGISTRY}/${ECR_REPO}:frontend-${IMAGE_TAG} ./frontend
                    docker build -t ${ECR_REGISTRY}/${ECR_REPO}:employee-service-${IMAGE_TAG} ./employee-service
                '''
            }
        }

        stage('Push images to ECR') {
            when {
                anyOf {
                    changeset 'frontend/**'
                    changeset 'employee-service/**'
                    changeset 'Jenkinsfile'
                }
            }
            steps {
                sh '''
                    aws ecr get-login-password --region ${AWS_REGION} |
                      docker login --username AWS --password-stdin ${ECR_REGISTRY}

                    docker push ${ECR_REGISTRY}/${ECR_REPO}:frontend-${IMAGE_TAG}
                    docker push ${ECR_REGISTRY}/${ECR_REPO}:employee-service-${IMAGE_TAG}
                '''
            }
        }

        stage('Update GitOps manifests') {
            when {
                anyOf {
                    changeset 'frontend/**'
                    changeset 'employee-service/**'
                    changeset 'Jenkinsfile'
                }
            }
            steps {
                sh '''
                    sed -i "s|:frontend-[^[:space:]]*|:frontend-${IMAGE_TAG}|" k8s/frontend/frontend-deployment.yml
                    sed -i "s|:employee-service-[^[:space:]]*|:employee-service-${IMAGE_TAG}|" k8s/employee-service/deployment.yml

                    git config user.name "Jenkins"
                    git config user.email "jenkins-bot@users.noreply.github.com"
                    git add k8s/frontend/frontend-deployment.yml k8s/employee-service/deployment.yml
                    git commit -m "Deploy Jenkins build ${IMAGE_TAG}"
                '''

                withCredentials([gitUsernamePassword(
                    credentialsId: 'github-write',
                    gitToolName: 'Default'
                )]) {
                    sh 'git push origin HEAD:master'
                }
            }
        }
    }
}
