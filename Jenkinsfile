pipeline {

    agent any

    environment {
        AWS_REGION = 'ap-south-1'
        ECR_REPOSITORY = 'ai-devops-k8s'
        AWS_ACCOUNT_ID = '470451076070'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build \
                -t $ECR_REPOSITORY:$IMAGE_TAG \
                ./app
                '''
            }
        }

        stage('Login to ECR') {
            steps {
                sh '''
                aws ecr get-login-password \
                --region $AWS_REGION | \
                docker login \
                --username AWS \
                --password-stdin \
                $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
                '''
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                docker tag \
                $ECR_REPOSITORY:$IMAGE_TAG \
                $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:$IMAGE_TAG

                docker push \
                $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:$IMAGE_TAG
                '''
            }
        }

        stage('Deploy to EKS') {
            steps {
                sh '''
                kubectl set image deployment/ai-devops-k8s \
                ai-devops-k8s=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:$IMAGE_TAG

                kubectl rollout status deployment/ai-devops-k8s
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                kubectl get pods -o wide
                kubectl get svc
                kubectl get deployment ai-devops-k8s
                '''
            }
        }
    }

    post {
        success {
            echo 'Deployment completed successfully'
        }

        failure {
            echo 'Deployment failed - investigate Jenkins and Kubernetes logs'
        }
    }
}

