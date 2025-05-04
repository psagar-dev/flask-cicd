pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        PYTHON = "./venv/bin/python"
        PIP = "./venv/bin/pip"
    }

    stages {
        // stage('Set up Virtualenv') {
        //     steps {
        //         sh """
        //             python -m venv $VENV_DIR
        //         """
        //     }
        // }

        stage('Install Dependencies') {
            {
                docker {
                    image 'python:3.12-slim'
                }
            }
            steps {
                sh """
                    python install -r requirements.txt
                """
            }
        }

        // stage('Run Tests') {
        //     steps {
        //         sh """
        //             $PYTHON -m pytest tests/
        //         """
        //     }
        // }
    }
}
