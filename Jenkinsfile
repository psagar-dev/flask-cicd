pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        PYTHON = "./venv/bin/python"
        PIP = "./venv/bin/pip"
    }

    stages {
        stage('Install Dependencies') {
            agent {
                docker {
                    image 'python:3.12-slim'
                }
            }
            steps {
                sh """
                    python install -r requirements.txt
                """
            }
        }
    }
}
