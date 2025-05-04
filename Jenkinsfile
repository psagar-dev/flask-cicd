pipeline {
    agent any

    tools {
        python 'python3'        // name in Global Tool Config
    }

    stages {
        stage('Test') {
            steps {
                echo 'Testing python...'
                sh 'python -m pytest tests/'
            }
        }
    }
}
