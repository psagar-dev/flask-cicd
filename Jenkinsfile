pipeline {
    agent any

    environment {
        IMAGE_NAME = "securelooper/jenkins-flask-app"
        CONTAINER_NAME = "jenkins-flask-app-container"
    }

    stages {
        // stage('Checkout') {
        //     steps {
        //         echo 'Cloning code...'
        //         checkout([$class: 'GitSCM',
        //                   branches: [[name: '*/main']],
        //                   userRemoteConfigs: [[
        //                       url: 'https://github.com/psagar-dev/flask-cicd.git',
        //                       credentialsId: 'github-access'
        //                   ]]
        //         ])
        //     }
        // }

        stage('Test') {
            steps {
                echo 'Cloning code...'
                sh 'python -m pytest tests/'
            }
        }
    }
}
