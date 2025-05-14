@Library('Shared') _
def config = securityConfig("securelooper/flask-cicd:${BUILD_NUMBER}",'flask-cicd-container')

pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "securelooper/flask-cicd"
        CONTAINER_NAME = "flask-cicd-container"
        VENV_DIR = 'venv'
        PYTHON = "./${VENV_DIR}/bin/python"
        PIP = "./${VENV_DIR}/bin/pip"
        DOCKER_CREDENTIALS_ID = 'docker-hub-creds'
    }

    stages {
        
        stage('Python Dependency Install') {
            agent {
                docker {
                    image 'python:3.13-slim'
                }
            }
            steps {
                installPythonDepsVm()
            }
        }

        stage("Security Scans") {
            steps {
                script {
                    securityScan()
                }
            }
        }
        
        stage('Unit Test') {
            agent {
                docker {
                    image 'python:3.13-slim'
                }
            }
            steps {
                unitTest()
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${config.DOCKER_IMAGE}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    pushDockerImage("${config.DOCKER_IMAGE}", "${config.DOCKER_CREDENTIALS_ID}")
                }
            }
        }

        stage('Deploy On Deploying') {
            steps {
                 sshagent (credentials: ['ssh-ec2']) {
                    script {
                        remoteDockerDeploy(
                            "${config.DOCKER_IMAGE}",
                            "${config.CONTAINER_NAME}"
                            "80:5000",
                            "ssh-ec2"
                        )
                    }
                 }
            }
        }
    }

    // post {
    //     success {
    //         emailext (
    //             subject: "✅ SUCCESS: ${JOB_NAME} #${BUILD_NUMBER}",
    //             body: "Build passed!\n\nDetails: ${env.BUILD_URL}",
    //             to: "${RECIPIENTS}"
    //         )
    //     }
        
    //     failure {
    //         emailext (
    //             subject: "❌ FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
    //             body: "Build failed!\n\nCheck console: ${env.BUILD_URL}",
    //             to: "${RECIPIENTS}"
    //         )
    //     }
    // }
}
