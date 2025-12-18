pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub-credentials'     // Jenkins credentials ID
        DOCKERHUB_USERNAME    = 'hasaan007'   // CHANGE THIS
        IMAGE_NAME            = "${DOCKERHUB_USERNAME}/cloud-final-app"
    }

    stages {
        stage('Code Fetch Stage') {
            steps {
                // This will pull from GitHub (SCM config in Jenkins job)
                checkout scm
            }
        }

        stage('Docker Image Creation Stage') {
            steps {
                script {
                    def imageTag = "${IMAGE_NAME}:${env.BUILD_NUMBER}"
                    sh "echo Building Docker image ${imageTag}"
                    sh "docker build -t ${imageTag} ."
                }
            }
        }

        stage('Push Image to DockerHub') {
            steps {
                script {
                    def imageTag = "${IMAGE_NAME}:${env.BUILD_NUMBER}"
                    withCredentials([usernamePassword(
                        credentialsId: DOCKERHUB_CREDENTIALS,
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh '''
                            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        '''
                    }
                    sh "docker push ${imageTag}"
                }
            }
        }

        stage('Kubernetes Deployment Stage') {
            steps {
                script {
                    def imageTag = "${IMAGE_NAME}:${env.BUILD_NUMBER}"

                    // Apply PVC, Deployment, Service
                    sh """
                        kubectl apply -f k8s/pvc.yaml
                        kubectl apply -f k8s/deployment.yaml
                        kubectl apply -f k8s/service.yaml
                    """

                    // Update deployment image to this build
                    sh """
                        kubectl set image deployment/notes-app notes-app=${imageTag} --record
                        kubectl rollout status deployment/notes-app
                    """
                }
            }
        }

        stage('Prometheus / Grafana Stage') {
            steps {
                script {
                    // Simple checks you can screenshot for the report
                    sh "kubectl get pods -n monitoring"
                    sh "kubectl get svc -n monitoring"
                }
            }
        }
    }
}
