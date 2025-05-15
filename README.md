# 🐳 Jenkins & Docker Installation Guide

## 🔧 Install Docker Engine

Use the official Docker installation script:

```bash
sudo curl -fsSL https://get.docker.com | sudo sh

# Add Your User to the Docker Group
sudo usermod -aG docker $USER
newgrp docker

# Add Jenkins User to the Docker Group
sudo usermod -aG docker jenkins
newgrp docker

# Restart Jenkins if needed:
sudo systemctl restart jenkins
```

---

## 📦 Prerequisite Plugin Installation

Before proceeding with the pipeline setup or deployment process, ensure the following plugins are installed in your CI/CD environment (e.g., Jenkins).

### ✅ Required Plugins

| Plugin Name        | Purpose |
|--------------------|---------|
| **SSH Agent**      | Allows you to use SSH credentials to connect to remote servers during pipeline execution. |
| **Docker Pipeline**| Provides steps to build, run, and manage Docker containers as part of your pipeline. |

### 🔧 Installation Steps (Jenkins Example)

1. **Open Jenkins Dashboard**
2. Navigate to **Manage Jenkins > Manage Plugins**
3. Go to the **Available** tab
4. Search for the following plugins:
   - `SSH Agent`
   - `Docker Pipeline`
5. Select both plugins and click **Install without restart**
6. (Optional) Restart Jenkins if required

### 🧪 Verify Installation

1. Go to **Manage Jenkins > System Information**
2. Search for the plugin names to confirm they are listed and active.

---

## 🛠️ Shared Library Setup

📘 Learn how to add a global trusted pipeline library in Jenkins:

🔗 [Global Trusted Pipeline Libraries](https://github.com/psagar-dev/cheatsheet/blob/main/Jenkins/global-trusted-pipeline-libraries.md)

---

## 📨 Configure SMTP in Jenkins for Email Notifications

📧 To set up SMTP email notifications in Jenkins:

🔗 [SMTP Notification Setup](https://github.com/psagar-dev/cheatsheet/blob/main/Jenkins/smtp-gmail-configure.md)

---

## 🔐 Credentials Setup (Required)

Please add the following credentials in Jenkins:

| Store  | Domain   | ID                | Name          | Functionality                      |
|--------|----------|-------------------|---------------|------------------------------------|
| System | (global) | Github            | ***** / ****** | Used for accessing GitHub repos in pipelines – [How to add this](https://github.com/psagar-dev/cheatsheet/blob/main/Jenkins/credentials-username-password.md) |
| System | (global) | gmail-smtp        | ***** / ****** | Sends notification emails via Gmail SMTP – [How to add this](https://github.com/psagar-dev/cheatsheet/blob/main/Jenkins/credentials-username-password.md) |
| System | (global) | docker-hub-creds  | ***** / ****** | Authenticates Docker Hub for image push/pull – [How to add this](https://github.com/psagar-dev/cheatsheet/blob/main/Jenkins/credentials-username-password.md) |
| System | (global) | ssh-ec2           | ubuntu         | SSH key to connect to EC2 instance – [How to add this](https://github.com/psagar-dev/cheatsheet/blob/main/Jenkins/credentials-ssh.md) |

---

## 🌍 Jenkins Global Environment Variables

This document outlines the global environment variables configured in Jenkins.

### ✅ Global Properties Configuration

Environment variables are enabled globally.

### 📋 List of Environment Variables

| Name                    | Value               | Description                        |
|-------------------------|---------------------|------------------------------------|
| `FLASK_CICD_EC2_HOST`   | `52.66.137.64`      | Public IP of the EC2 instance      |
| `FLASK_CICD_EC2_USER`   | `ubuntu`            | Default SSH user for EC2 login     |
| `FLASK_EMAIL_RECIPIENTS`| `xxxxxxx@gmail.com` | Email recipient for notifications  |

---

# 🚀 Jenkins Pipeline Configuration for `flask-cicd`

## 📁 Pipeline Definition

- **Definition**: Pipeline script from SCM
- **SCM**: Git
- **Repository URL**: `https://github.com/psagar-dev/flask-cicd.git`
- **Credentials**: `psagar-dev/******`
- **Branch Specifier**: `main`
- **Script Path**: `Jenkinsfile`

## ⚡ Trigger

- [x] GitHub hook trigger for GITScm polling 

## 📝 Notes

- This configuration uses a declarative pipeline stored in the `main` branch under the file `Jenkinsfile`.
- Ensure that the **GitHub webhook** is properly configured in your GitHub repository settings to trigger Jenkins jobs automatically.

![Jenkins Configuration](./images/jenkins/flask-cicd-configration.png)

---

# 📄 Jenkinsfile

📌 The shared library used in this pipeline:  
🔗 [jenkins-shared-libraries](https://github.com/psagar-dev/jenkins-shared-libraries)

```groovy
@Library('Shared') _
def config = securityConfig("securelooper/flask-cicd:${BUILD_NUMBER}",'flask-cicd-container')

pipeline {
    agent any
    
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
                            "${config.CONTAINER_NAME}",
                            "80:5000",
                            "ssh-ec2"
                        )
                    }
                 }
            }
        }
    }

    post {
        success {
            script {
                sendSuccessEmailNotification("${env.FLASK_EMAIL_RECIPIENTS}")
            }
        }
        
        failure {
           script {
                sendFailureEmailNotification("${env.FLASK_EMAIL_RECIPIENTS}")
            }
        }
    }
}
```

Here's a **concise summary** of your Jenkins pipeline in **Markdown format**, ideal for documentation or team sharing:

---

# 🚀 Flask CI/CD Pipeline Summary
## 🔧 Key Components

- **Shared Library**: `@Library('Shared')` — contains reusable functions
- **Docker Image**: `securelooper/flask-cicd:${BUILD_NUMBER}`
- **Container Name**: `flask-cicd-container`
- **Base Image**: `python:3.13-slim`
- **Deployment Target**: Remote EC2 instance via SSH
---

## 📦 Pipeline Stages

| Stage                  | Purpose                                           |
|------------------------|---------------------------------------------------|
| **Python Dependency Install** | Installs dependencies inside Python Docker container |
| **Security Scans**     | Runs security checks on code and dependencies     |
| **Unit Test**          | Executes unit tests                               |
| **Build Docker Image** | Builds Docker image with dynamic tag              |
| **Push Docker Image**  | Pushes image to registry using secure credentials |
| **Deploy On Deploying**| Deploys to EC2 using SSH and Docker               |

---

## 📬 Notifications

- ✅ **Success**: Sends email to `${env.FLASK_EMAIL_RECIPIENTS}`
- ❌ **Failure**: Sends alert email on pipeline failure

---

## 🖥️ Deployment Details

- Uses `sshagent` with credential ID: `ssh-ec2`
- Maps port: `80 (host)` → `5000 (container)`
- Custom function: `remoteDockerDeploy(...)`

---

## 📁 Notes

- All critical steps are abstracted into shared library functions:
  - `installPythonDepsVm()`
  - `securityScan()`
  - `unitTest()`
  - `pushDockerImage(...)`
  - `remoteDockerDeploy(...)`
  - `send*EmailNotification(...)`

## 🚀 Pipeline Overview
📷 ![Pipeline Overview](./images/jenkins/pipline-overview.png)