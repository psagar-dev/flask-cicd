pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh """
                    python -m pip install --upgrade pip'
                    pip install -r requirements.txt
                """
            }
        }
        
        stage('Test') {
            steps {
                echo 'Testing python...'
                sh 'python3 -m pytest tests/'
            }
        }
    }
}
