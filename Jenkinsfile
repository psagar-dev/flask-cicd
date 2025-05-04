pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning code...'
                git 'https://github.com/psagar-dev/flask-cicd.git'
            }
        }
    }
}
