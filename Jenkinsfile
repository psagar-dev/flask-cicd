pipeline {
    agent {
        docker {
            image 'python:3.12-slim'
        }
    }

    stages {
        stage('Build') {
            steps {
                sh """
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        stage('Test') {
            steps {
                echo 'Testing python...'
                sh 'python -m pytest tests/'
            }
        }
    }
}
