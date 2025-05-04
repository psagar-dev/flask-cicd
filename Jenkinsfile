pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "securelooper/flask-app-demo"
        CONTAINER_NAME = "flask-app-demo-container"
        VENV_DIR = 'venv'
        PYTHON = "./${VENV_DIR}/bin/python"
        PIP = "./${VENV_DIR}/bin/pip"
    }

    stages {
        stage('Python Dependency Install') {
            agent {
                docker {
                    image 'python:3.12-slim'
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

        stage('Unit Test') {
            agent {
                docker {
                    image 'python:3.12-slim'
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
                    docker.build(DOCKER_IMAGE)
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('', DOCKER_CREDENTIALS_ID) {
                        docker.image(DOCKER_IMAGE).push()
                    }
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent (credentials: ['ssh-ec2']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} '
                        echo "Pulling latest Docker image"
                        sudo docker pull ${DOCKER_IMAGE}

                        echo "Stopping existing container"
                        sudo docker stop ${CONTAINER_NAME} || true
                        sudo docker rm ${CONTAINER_NAME} || true

                        echo "Starting new container"
                        sudo docker run -d --name ${CONTAINER_NAME} -p 80:5000 ${DOCKER_IMAGE}

                        echo "✅ Deployment successful"
                        '
                    """
                }
            }
        }
    }
}
