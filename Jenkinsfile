pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "securelooper/flask-cicd"
        CONTAINER_NAME = "flask-cicd-container"
        VENV_DIR = 'venv'
        PYTHON = "./${VENV_DIR}/bin/python"
        PIP = "./${VENV_DIR}/bin/pip"
        DOCKER_CREDENTIALS_ID = 'docker-hub-creds'
    }

    stages {
        
        stage('Python Dependency Install') {
            agent {
                docker {
                    image 'python:3.13-slim'
                }
            }
            steps {
                sh """
                    python3 -m venv ${VENV_DIR}
                    ${PIP} install --upgrade pip
                    ${PIP} install -r requirements.txt
                """
            }
        }

        stage("Security Scans") {
            parallel {
                stage('Trivy Vulnerability Scan') {
                    steps {
                        sh '''
                            docker run --rm \
                            -v $PWD:/project \
                            aquasec/trivy:latest fs /project \
                            --exit-code 1 --severity HIGH,CRITICAL || true
                        '''
                    }
                }
                stage("Gitleaks Secret Scan") {
                    steps {
                        sh '''
                            docker run --rm \
                            -v $PWD:/repo \
                            zricethezav/gitleaks:latest detect \
                            --source=/repo --verbose --redact --exit-code 1 || true
                        '''
                    }
                }
            }
        }
        
        stage('Unit Test') {
            agent {
                docker {
                    image 'python:3.13-slim'
                }
            }
            steps {
                sh """
                    ${PYTHON} -m pytest tests/
                """
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def IMAGE_NAME_TAG = "${DOCKER_IMAGE}:${BUILD_NUMBER}"
                    docker.build(IMAGE_NAME_TAG)
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('', DOCKER_CREDENTIALS_ID) {
                        def IMAGE_NAME_TAG = "${DOCKER_IMAGE}:${BUILD_NUMBER}"
                        docker.image(IMAGE_NAME_TAG).push()
                    }
                }
            }
        }

        stage('Deploy On Deploying') {
            steps {
                 sshagent (credentials: ['ssh-ec2']) {
                    script {
                        def IMAGE_NAME_TAG = "${DOCKER_IMAGE}:${BUILD_NUMBER}"
                        sh """
                            ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} '
                            echo "Pulling latest Docker image"
                            sudo docker pull ${IMAGE_NAME_TAG}
                            
                            echo "Stopping any existing container..."
                            sudo docker stop ${CONTAINER_NAME} || true
                            sudo docker rm ${CONTAINER_NAME} || true
                            
                            echo "Running the container..."
                            sudo docker run -d --name ${CONTAINER_NAME} -p 80:5000 ${IMAGE_NAME_TAG}
                            
                            echo "Deployment successful!"
                            '
                        """
                    }
                 }
            }
        }
    }

    // post {
    //     success {
    //         emailext (
    //             subject: "✅ SUCCESS: ${JOB_NAME} #${BUILD_NUMBER}",
    //             body: "Build passed!\n\nDetails: ${env.BUILD_URL}",
    //             to: "${RECIPIENTS}"
    //         )
    //     }
        
    //     failure {
    //         emailext (
    //             subject: "❌ FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
    //             body: "Build failed!\n\nCheck console: ${env.BUILD_URL}",
    //             to: "${RECIPIENTS}"
    //         )
    //     }
    // }
}
