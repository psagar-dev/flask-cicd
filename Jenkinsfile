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
    }
}