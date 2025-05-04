pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                echo 'Testing python...'
                sh 'python3 -m pytest tests/'
            }
        }
    }
}
