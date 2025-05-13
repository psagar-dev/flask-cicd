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

        stage("Trivy Vulnerability Scan") {
            agent {
                docker {
                    image 'aquasec/trivy:latest'
                }
            }
            steps {
                sh 'trivy fs . --exit-code 1 --severity HIGH,CRITICAL . || true'
            }
        }

        stage("Gitleaks Secret Scan") {
            agent {
                docker {
                    image 'zricethezav/gitleaks:latest'
                }
            }

            steps {
                sh """
                    gitleaks detect --source=. --verbose --redact --exit-code 1 || true
                """
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
