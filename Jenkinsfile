pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning code...'
                checkout([$class: 'GitSCM',
                          branches: [[name: '*/main']],
                          userRemoteConfigs: [[
                              url: 'https://github.com/psagar-dev/flask-cicd.git',
                              credentialsId: 'github-access'
                          ]]
                ])
            }
        }
    }
}
