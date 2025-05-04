pipeline {
    agent any

    environment {
        IMAGE_NAME = "securelooper/jenkins-flask-app"
        CONTAINER_NAME = "jenkins-flask-app-container"
    }

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

        stage('Build Docker Image') {
            steps {
                sh "docker image build -t ${IMAGE_NAME} ."
            }
        }

        stage("Stop & Remove Old Container") {
            steps {
                sh """
                    if docker ps -a --format '{{.Names}}' | grep -Eq "^${CONTAINER_NAME}\$"; then
                        docker container stop ${CONTAINER_NAME} || true
                        docker container rm ${CONTAINER_NAME} || true
                    fi
                """
            }
        }

        stage('Run Docker Container') {
            steps {
                sh "docker run -d -p 5000:5000 --name ${CONTAINER_NAME} ${IMAGE_NAME}"
            }
        }
    }
}
