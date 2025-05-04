pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        PYTHON = "./${VENV_DIR}/bin/python"
        PIP = "./${VENV_DIR}/bin/pip"
    }

    stages {
        stage('Build') {
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

        stage('Test') {
            agent {
                docker {
                    image 'python:3.12-slim'
                }
            }
            steps {
                sh """
                    $PYTHON -m pytest tests/
                """
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh "docker image build -t ${DOCKER_IMAGE_NAME} ."
            }
        }

        stage("Stop & Remove Old Container") {
            steps {
                sh """
                    if docker ps -a --format '{{.Names}}' | grep -Eq "^${DOCKER_CONTAINER_NAME}\$"; then
                        docker container rm -f ${DOCKER_CONTAINER_NAME} || true
                    fi
                """
            }
        }

        stage('deploying on stage envirement') {
            steps {
                sh "docker run -d -p 5000:5000 --name ${DOCKER_CONTAINER_NAME} ${DOCKER_IMAGE_NAME}"
            }
        }
    }
}