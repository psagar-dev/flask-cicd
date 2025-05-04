pipeline {
    agent {
        docker {
            image 'python:3.12-slim'
        }
    }

    environment {
        VENV_PATH = "./venv"
        PYTHON_BIN = "./venv/bin/python"
        PIP_BIN = "./venv/bin/pip"
    }

    stages {
        stage('Build') {
            steps {
                sh """
                    python -m venv $VENV_PATH
                    $PIP_BIN install --upgrade pip
                    $PIP_BIN install -r requirements.txt
                """
            }
        }

        stage('Test') {
            steps {
                echo 'Testing python...'
                sh '$PYTHON_BIN -m pytest tests/'
            }
        }
    }
}
