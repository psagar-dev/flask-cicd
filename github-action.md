
## 🚀 Flask CI/CD Pipeline: GitHub Actions → AWS ECS Fargate

Automate the build, test, security scan, and deployment of your Flask app using **GitHub Actions**, **AWS ECR/ECS (Fargate)**, **Cloudflare DNS**, and **Slack** notifications.

---

#### 📝 Brief Description

This CI/CD setup enables:

* **Automated build, test, and deployment** for every code change (staging) and release (production).
* **Security checks** using `Trivy` and `Gitleaks` before every deployment.
* **Seamless Docker image storage** in AWS ECR.
* **Serverless deployment** with AWS ECS Fargate.
* **Custom domains** managed by `Cloudflare`.
* **Slack notifications** for pipeline status **(success/failure)**.

**Result:**
Every code change is built, tested, security-checked, and deployed automatically—making your app secure, up-to-date, and reliably available on your custom domain.

---

#### 🖼️ Architecture Overview

```mermaid
flowchart LR
    Developer[Developer Push/Release] -->|Triggers| GitHubActions[GitHub Actions]
    GitHubActions -->|Build & Push| ECR[AWS ECR]
    GitHubActions -->|Deploy| ECS[AWS ECS Fargate]
    ECR --> ECS
    ECS -->|DNS| Cloudflare[Cloudflare]
    GitHubActions -->|Notify| Slack[Slack]
    Cloudflare -->|Route| Browser[prod/stage.yourdomain.com]

```

---

#### 📸 Visual Guide

##### 1. 🐳 AWS ECR (Elastic Container Registry)

* **🔒 Create ECR Private Repo:**
  Create a private repository in AWS ECR to store your Docker images securely.
![ECR Private Repo](./images/github/ecr-private-repo.png)
  

* **📂 ECR Repo List:**
View all existing repositories in ECR, including your new Flask app repo.
![ECR Private Repo List](./images/github/ecr-repository-list.png)
  
  

* **🏷️ ECR Image Tags:**
  Shows the list of images and tags that have been pushed to your private ECR repository.
![Private register images](./images/github/private-register-images.png)
  
---

#### 2.🚢 AWS ECS Fargate

* **🛠️ Create ECS Cluster:**
  Start by creating a new ECS cluster to run your containers in Fargate mode.
  ![Create Cluster](./images/github/create-cluster.png)
  

* **📝 Create Task Definition:**
  Shows the interface for creating a new ECS task definition for your Flask app.
  ![ECS Task Create](./images/github/ecs-task-create.png)
  

* **📜 Task Definition List:**
  Displays all ECS task definitions which describe how containers are run.
  ![ECS Task List](./images/github/ecs-task-list.png)
  
* **📝 Create Service:**
This screen is used to set up a new service in Amazon ECS. Here, you choose your task definition, configure deployment settings, and connect your containers to an Application Load Balancer. This process makes sure your application runs smoothly, scales easily, and is accessible through a reliable load balancer.
![ECS Create Service](./images/github/ecr-create-service.png)

![ECS Service List](./images/github/service.png)

### 🚦 Application Load Balancer
![Load Balancer](./images/github/load-balncer.png)

---

#### 3.🌐 Cloudflare DNS

* **🏷️ Production Domain Setup:**
  Example of a CNAME(Load Balancer) record in Cloudflare for routing traffic to your production environment.
![cloudflare Production Setup](./images/github/cloudflare-production.png)
  
* **🧪 Staging Domain Setup:**
  Example of an A record in Cloudflare to route staging traffic for QA/testing.
  ![cloudflare Stage Setup](./images/github/cloudflare-stage.png)



Here's a concise and professional deployment **module document** for setting up an **EC2 instance for GitHub Actions self-hosted runner** and deploying to a **staging environment**.

---

### 🛠️ EC2 Setup for GitHub Actions Runner & Staging Deployment

## 📍 Overview

This guide covers:

1. Provisioning an EC2 instance for a GitHub Actions runner
2. Installing the runner & dependencies
3. Connecting it to GitHub
4. Deploying to a staging environment

---

### 1️⃣ Launch EC2 for GitHub Actions Runner
![Ec2](./images/ec2.png)

### 2️⃣ Install Docker & Add Permissions

```bash
sudo curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
newgrp docker
```

### 🚀 Step-by-Step: Set Up GitHub Actions Runner (Ubuntu/Linux)

#### ✅ 1. **Go to GitHub Repository Settings**

* Open your repository on GitHub.
* Click on **Settings > Actions > Runners**.
* Click **"New self-hosted runner"**.
* Select:

  * OS: **Linux**
  * Architecture: **x64**

GitHub will generate a **setup script** like this:

```bash
# Create a folder
mkdir actions-runner && cd actions-runner

# Download latest runner package
curl -o actions-runner-linux-x64-2.314.1.tar.gz -L https://github.com/actions/runner/releases/download/v2.314.1/actions-runner-linux-x64-2.314.1.tar.gz

# Extract installer
tar xzf ./actions-runner-linux-x64-2.314.1.tar.gz

# Configure the runner
./config.sh --url https://github.com/<your-username>/<your-repo> --token <your-token>

# Start the runner
./run.sh
```

> ⚠️ Replace `<your-username>/<your-repo>` and `<your-token>` with your actual repository info.

#### 🧪 3. **Verify Runner**

* Go back to **Settings > Actions > Runners**.
* You should see the runner status as **Idle**.

![Self Host](./images/github/ci-cd.png)

---

### 🧩 Notes:

* Ensure the machine has access to Docker (if your workflows need it).
* Add your runner to specific **labels** for easier workflow filtering.
* Use `runs-on: self-hosted` or `runs-on: [self-hosted, linux]` in your workflow.


#### ⚙️ Environment Variables

Set these as **GitHub Secrets** for security:

| Variable Name            | Example                                                                   | Usage               |
| ------------------------ | ------------------------------------------------------------------------- | ------------------- |
| AWS\_ACCESS\_KEY\_ID     | AKIAIOSXXXXXXXXXXXX                                                       | AWS authentication  |
| AWS\_SECRET\_ACCESS\_KEY | wJalrXXXXXXXX/K7MDENG/bPxRfiCXXXXXXXX                                     | AWS authentication  |
| AWS\_REGION              | ap-south-1                                                                | AWS region          |
| ECR\_REPOSITORY          | flask-app                                                                 | ECR repository name |
| ECS\_CLUSTER             | flask-app-cluster                                                         | ECS cluster name    |
| ECS\_SERVICE             | flask-app-service                                                         | ECS service name    |
| ECS\_TASK\_DEFINITION    | flask-task-def:1                                                          | ECS task definition |
| SLACK\_WEBHOOK\_URL      | [https://hooks.slack.com/services/](https://hooks.slack.com/services/)... | Slack notifications |
| SSH\_HOST                | ec2-12-34-56-78.compute.amazonaws.com                                     | SSH (if used)       |
| SSH\_PRIVATE\_KEY        | -----BEGIN RSA PRIVATE KEY-----...                                        | SSH key (if used)   |

---

##### ✅ How to Add Environment Variables in GitHub Actions

1. Go to your GitHub repository.
2. Click on **Settings**.
3. Select **Secrets and variables > Actions**.
4. Click **New repository secret**.
5. Add the secret with the **Name** and **Value**.

---

#### 🚦 Pipeline Overview

##### 🏁 Main Branch: `production.yml`

```yaml
on:
  release:
    types: [published]
  workflow_dispatch:
```

* **🚀 Deploys to Production** when a release is published.

---

#### 🧪 Staging Branch: `staging.yml`

```yaml
on:
  push:
    branches: [staging]
  workflow_dispatch:
```

* **🧪 Deploys to Staging** on every push to `staging` branch.

---

#### 🧩 Key Pipeline Jobs

##### 📦 Install Dependencies
Common to both `staging.`yml` and `production.yml` — checks out code, sets up Python, and installs requirements.

```yaml
install-dependencies:
  runs-on: self-hosted
  steps:
    - name: Checkout code
      uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'
    - name: Install dependencies
      run: |
        pip install --upgrade pip
        pip install -r requirements.txt
```
##### 📝 Explanation:

| Step                 | Description                                                          |
| -------------------- | -------------------------------------------------------------------- |
| `actions/checkout`   | Checks out the code from the GitHub repository into the runner.      |
| `setup-python@v5`    | Sets up Python 3.12 environment on the GitHub self-hosted runner.    |
| Install dependencies | Upgrades `pip` and installs Python packages from `requirements.txt`. |

#### 🔐 Security Check
✅ Used in both `staging.yml` and `production.yml`
Scans for vulnerabilities (`Trivy`) and secrets (`Gitleaks`).

```yaml
security-check:
  runs-on: self-hosted
  needs: install-dependencies
  steps:
    - name: Checkout code
      uses: actions/checkout@v4
    - name: Trivy Installation
      run: |
        sudo apt-get update -y
        sudo apt-get install -y wget apt-transport-https gnupg lsb-release
        wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
        echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | sudo tee -a /etc/apt/sources.list.d/trivy.list
        sudo apt-get update -y
        sudo apt-get install -y trivy
    - name: Trivy FS Scan
      run: trivy fs --format table -o fs-report.json .
    - name: Gitleaks Installation
      run: sudo apt install gitleaks -y
    - name: Gitleaks Code Scan
      run: gitleaks detect --source . -r gitleaks-report.json -f json
```
##### 📝 Explanation

| Step                          | Description                                                                                                  |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `needs: install-dependencies` | Ensures this job runs **after** `install-dependencies` is complete.                                          |
| `actions/checkout@v4`         | Checks out the repo code again in this job (required for scanning tools).                                    |
| **Trivy Installation**        | Installs [Trivy](https://github.com/aquasecurity/trivy), a tool to scan for OS/package/code vulnerabilities. |
| **Trivy FS Scan**             | Scans the full file system (`.`) and writes the output to `fs-report.json`.                                  |
| **Gitleaks Installation**     | Installs [Gitleaks](https://github.com/gitleaks/gitleaks), a secrets detection tool.                         |
| **Gitleaks Code Scan**        | Scans the codebase for hardcoded secrets and writes a report in `gitleaks-report.json`.   

##### 🛡️ Purpose

This job helps catch:

* Vulnerabilities in dependencies or file system content (**Trivy**).
* Secrets accidentally committed to the codebase (**Gitleaks**).

✅ Ideal for CI/CD pipelines in production-grade environments where **security checks are mandatory** before deployment.

---

#### 🧪 Run Tests

Executes Python tests to verify code before deployment.
✅ Used in both `staging.yml` and `production.yml`

```yaml
run-tests:
  runs-on: self-hosted
  needs: security-check
  steps:
    - name: Checkout code
      uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'
    - name: Install dependencies
      run: |
        pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: python -m pytest tests/
```
##### 📝 Explanation

| Step                      | Description                                                             |
| ------------------------- | ----------------------------------------------------------------------- |
| `needs: security-check`   | Ensures this job runs **after** `security-check` completes.             |
| `actions/checkout@v4`     | Retrieves the repository code to the runner.                            |
| `setup-python@v5`         | Sets up Python 3.12 for running the tests.                              |
| Install dependencies      | Installs all required Python packages listed in `requirements.txt`.     |
| `python -m pytest tests/` | Executes all test cases inside the `tests/` directory using **pytest**. |


##### 🧠 Purpose

This job:

* Ensures your application code is **functionally correct** before deployment.
* Catches errors early by **automatically running your unit or integration tests**.

✅ Best practice to run this before any deployment to **staging or production**.

### 🚀 `deploy-staging`

This job **automatically deploys the latest code to the staging server** whenever changes are pushed to the `staging` branch.

It performs the following:

1. **Builds and tags** a Docker image using the latest code.
2. **Pushes** the image to **Amazon ECR**.
3. **Connects via SSH** to a remote staging server.
4. **Pulls the new image**, removes the old container, and **runs the updated container** using the new image.

This ensures your staging environment is always up to date with the latest code changes for testing and review.

```
deploy-staging:
        runs-on: self-hosted
        needs: run-tests
        if: github.ref == 'refs/heads/staging'
        env:
            ECR_REPOSITORY: ${{ secrets.ECR_REPOSITORY }}
            IMAGE_TAG: staging-${{ github.run_number }}
        steps:
          - name: Checkout code
            uses: actions/checkout@v4
          
          - name: Configure AWS credentials
            uses: aws-actions/configure-aws-credentials@v4
            with:
                aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
                aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
                aws-region: ${{ secrets.AWS_REGION }}
          
          - name: Log in to Amazon ECR
            id: login-ecr
            uses: aws-actions/amazon-ecr-login@v2

          - name: Build, tag, and push Docker image to ECR
            env:
                ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
            run: |
                  docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
                  docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG

          - name: Set up SSH key
            run: |
              mkdir -p ~/.ssh
              echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/id_ed25519
              chmod 600 ~/.ssh/id_ed25519
              ssh-keyscan -H ${{ secrets.SSH_HOST }} >> ~/.ssh/known_hosts
          
          - name: Deploy to remote server via SSH
            uses: appleboy/ssh-action@v1
            with:
              host: ${{ secrets.SSH_HOST }}
              username: ubuntu
              key: ${{ secrets.SSH_PRIVATE_KEY }}
              port: 22
              script: |
                export AWS_ACCESS_KEY_ID=${{ secrets.AWS_ACCESS_KEY_ID }}
                export AWS_SECRET_ACCESS_KEY=${{ secrets.AWS_SECRET_ACCESS_KEY }}
                export AWS_REGION=${{ secrets.AWS_REGION }}

                if ! command -v aws &> /dev/null; then
                  echo "Installing AWS CLI..."
                  sudo apt update
                  sudo apt install unzip curl -y
                  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
                  unzip -o awscliv2.zip
                  sudo ./aws/install
                  export PATH=$PATH:/usr/local/bin
                fi

                echo "🔐 Logging into ECR..."
                aws ecr get-login-password --region ${{ secrets.AWS_REGION }} | docker login --username AWS --password-stdin ${{ steps.login-ecr.outputs.registry }}

                IMAGE_URI=${{ steps.login-ecr.outputs.registry }}/${{ secrets.ECR_REPOSITORY }}:staging-${{ github.run_number }}

                echo "📦 Pulling Image: $IMAGE_URI"
                docker pull $IMAGE_URI

                echo "🧹 Removing old container"
                docker rm -f python-cicd-container || true

                echo "🚀 Running new container"
                docker run -d --name python-cicd-container -p 80:5000 $IMAGE_URI
```


Here’s a **brief description** of the two Slack notification jobs in your `staging` workflow:

### 🔔 `notify-on-success-staging`

Sends a **Slack message when the staging pipeline completes successfully**.
It notifies the team with repo name, branch, and commit SHA to confirm that the deployment succeeded.
```
notify-on-success-staging:
      runs-on: self-hosted
      needs: [install-dependencies,security-check, run-tests, deploy-staging]
      if: success()
      steps:
        - name: Send Slack Notification on Success
          uses: slackapi/slack-github-action@v2.0.0
          with:
            payload: |
              {
                "text": "✅ *CI/CD Pipeline Succeeded!*",
                "attachments": [
                  {
                    "color": "#2eb886",
                    "fields": [
                      {
                        "title": "Repo",
                        "value": "${{ github.repository }}",
                        "short": true
                      },
                      {
                        "title": "Branch",
                        "value": "${{ github.ref_name }}",
                        "short": true
                      },
                      {
                        "title": "Commit",
                        "value": "${{ github.sha }}",
                        "short": false
                      }
                    ]
                  }
                ]
              }
            webhook-type: incoming-webhook
          env:
            SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### 🔥 `notify-on-failure-staging`

Sends a **Slack alert if any stage of the staging pipeline fails** (including build, test, or deploy).
This helps the team quickly react to pipeline issues with details like repo, branch, and commit.

```
    notify-on-failure-staging:
        runs-on: self-hosted
        needs: [install-dependencies,security-check, run-tests, deploy-staging]
        if: failure()
        steps:
          - name: Send Slack Notification on Failure
            uses: slackapi/slack-github-action@v2.0.0
            with:
              payload: |
                {
                  "text": "❌ *CI/CD Pipeline Failed!*",
                  "attachments": [
                    {
                      "color": "#ff0000",
                      "fields": [
                        {
                          "title": "Repo",
                          "value": "${{ github.repository }}",
                          "short": true
                        },
                        {
                          "title": "Branch",
                          "value": "${{ github.ref_name }}",
                          "short": true
                        },
                        {
                          "title": "Commit",
                          "value": "${{ github.sha }}",
                          "short": false
                        }
                      ]
                    }
                  ]
                }
              webhook-type: incoming-webhook
            env:
              SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

Here’s a **brief description** of the `deploy-production` job in your GitHub Actions workflow:

### 🚀 `deploy-production`

This job **automatically deploys the app to AWS ECS** when a new **GitHub release is published**.

It performs the following:

1. **Builds and tags** a Docker image from the latest release code.
2. **Pushes** the image to **Amazon ECR**.
3. **Fetches the ECS task definition**, updates it with the new image.
4. **Registers a new task definition revision**.
5. **Deploys** the new version to the **ECS service** by updating it.

✅ This ensures production always runs the latest release, with a safe and controlled deployment to ECS.

```
deploy-production:
        runs-on: self-hosted
        needs: run-tests
        env:
          ECR_REPOSITORY: ${{ secrets.ECR_REPOSITORY }}
          IMAGE_TAG: ${{ github.run_number }}
        if: github.event_name == 'release' && github.event.action == 'published'
        steps:
            - name: Checkout code
              uses: actions/checkout@v4

            - name: Configure AWS credentials
              uses: aws-actions/configure-aws-credentials@v4
              with:
                aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
                aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
                aws-region: ${{ secrets.AWS_REGION }}

            - name: Log in to Amazon ECR
              id: login-ecr
              uses: aws-actions/amazon-ecr-login@v2

            - name: Build, tag, and push Docker image to ECR
              env:
                ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
              run: |
                  docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
                  docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG

            - name: Deploy to remote server via SSH
              uses: appleboy/ssh-action@v1
              with:
                host: ${{ secrets.SSH_HOST }}
                username: ubuntu
                key: ${{ secrets.SSH_PRIVATE_KEY }}
                port: 22
                script: |
                  export AWS_ACCESS_KEY_ID=${{ secrets.AWS_ACCESS_KEY_ID }}
                  export AWS_SECRET_ACCESS_KEY=${{ secrets.AWS_SECRET_ACCESS_KEY }}
                  export AWS_REGION=${{ secrets.AWS_REGION }}

                  if ! command -v aws &> /dev/null; then
                    echo "Installing AWS CLI..."
                    sudo apt update
                    sudo apt install unzip curl -y
                    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
                    unzip -o awscliv2.zip
                    sudo ./aws/install
                    export PATH=$PATH:/usr/local/bin
                  fi

                  echo "🔐 Logging into ECR..."
                  aws ecr get-login-password --region ${{ secrets.AWS_REGION }} | docker login --username AWS --password-stdin ${{ steps.login-ecr.outputs.registry }}

            - name: Fetch Current Task Definition
              run: |
                aws ecs describe-task-definition \
                  --task-definition ${{ secrets.ECS_TASK_DEFINITION }} \
                  --query "taskDefinition" > task-def.json

            - name: Update Image in Task Definition
              id: update-task
              run: |
                IMAGE_URI=${{ steps.login-ecr.outputs.registry }}/$ECR_REPOSITORY:$IMAGE_TAG
                jq --arg IMAGE "$IMAGE_URI" '
                  del(
                    .taskDefinitionArn,
                    .revision,
                    .status,
                    .requiresAttributes,
                    .compatibilities,
                    .registeredAt,
                    .registeredBy
                  )
                  | .containerDefinitions[0].image = $IMAGE
                ' task-def.json > new-task-def.json

            - name: Register New Task Definition Revision
              id: register-task
              run: |
                TASK_DEF_ARN=$(aws ecs register-task-definition \
                  --cli-input-json file://new-task-def.json \
                  --query "taskDefinition.taskDefinitionArn" \
                  --output text)
                echo "TASK_DEF_ARN=$TASK_DEF_ARN" >> $GITHUB_ENV

            - name: Deploy to ECS
              run: |
                aws ecs update-service \
                  --cluster ${{ secrets.ECS_CLUSTER }} \
                  --service ${{ secrets.ECS_SERVICE }} \
                  --task-definition $TASK_DEF_ARN \
                  --force-new-deployment
```


Here’s a **brief description** of the two Slack notification jobs in your **main production pipeline**:

### ✅ `notify-on-success-main`

Sends a **Slack message** when the entire **production CI/CD pipeline** succeeds — including build, security checks, tests, and deployment.

Includes:

* Repository name
* Branch
* Commit SHA

✅ Confirms successful deployment after a published release.
```
notify-on-success-main:
      runs-on: self-hosted
      needs: [install-dependencies,security-check, run-tests, deploy-production]
      if: success()
      steps:
        - name: Send Slack Notification on Success
          uses: slackapi/slack-github-action@v2.0.0
          with:
            payload: |
              {
                "text": "✅ *CI/CD Pipeline Succeeded!*",
                "attachments": [
                  {
                    "color": "#2eb886",
                    "fields": [
                      {
                        "title": "Repo",
                        "value": "${{ github.repository }}",
                        "short": true
                      },
                      {
                        "title": "Branch",
                        "value": "${{ github.ref_name }}",
                        "short": true
                      },
                      {
                        "title": "Commit",
                        "value": "${{ github.sha }}",
                        "short": false
                      }
                    ]
                  }
                ]
              }
            webhook-type: incoming-webhook
          env:
            SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### ❌ `notify-on-failure-main`

Sends a **Slack alert** if **any stage fails** in the production pipeline.

Includes:

* Repository name
* Branch
* Commit SHA

🚨 Helps the team stay informed of broken builds or deployment issues immediately.
```
notify-on-failure-main:
        runs-on: self-hosted
        needs: [install-dependencies,security-check, run-tests, deploy-production]
        if: failure()
        steps:
          - name: Send Slack Notification on Failure
            uses: slackapi/slack-github-action@v2.0.0
            with:
              payload: |
                {
                  "text": "❌ *CI/CD Pipeline Failed!*",
                  "attachments": [
                    {
                      "color": "#ff0000",
                      "fields": [
                        {
                          "title": "Repo",
                          "value": "${{ github.repository }}",
                          "short": true
                        },
                        {
                          "title": "Branch",
                          "value": "${{ github.ref_name }}",
                          "short": true
                        },
                        {
                          "title": "Commit",
                          "value": "${{ github.sha }}",
                          "short": false
                        }
                      ]
                    }
                  ]
                }
              webhook-type: incoming-webhook
            env:
              SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

#### 4.⚙️ CI/CD Pipeline Status (GitHub Actions & Slack)

* **🚀 Production Pipeline Success:**
  Shows a successful production pipeline run on GitHub Actions, triggered by a release.
![Production Pipline Success](./images/github/production-pipline-success.png)
  

* **🧪 Staging Pipeline Success:**
  Shows a successful staging pipeline run for new code pushes to the staging branch.
  ![Stgaing Pipline Success](./images/github/staging-pipline-suucess.png)
  

* **📣 Production Slack Notification:**
  Slack notification for production pipeline status (success or failure).
  ![Prduction Fail Success](./images/github/prduction-fail-success.png)
  

* **❌ Staging Pipeline Failed Notification:**
  Example Slack alert when the staging pipeline fails.
  ![Staging Faild](./images/github/staging-faild.png)
  

* **✅ Staging Pipeline Success Notification:**
  Example Slack alert when the staging pipeline succeeds.
  ![Stgaing Success](./images/github/stgaing-success.png)
  
#### 5.🌟 Application Result

* **🌍 Production App Live:**
  The deployed Flask app running on the production domain.
  ![Production View Success](./images/github/production-success-view.png)
  

* **🧪 Staging App Live:**
  The deployed Flask app available on the staging domain for testing.
  ![Stage View Success](./images/github/stage-suucess-view.png)

### Slack Notifications

Sends a message to Slack on every pipeline success or failure, including repo, branch, and commit information.