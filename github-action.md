# Environment Variables

These environment variables are required for the deployment process. Replace the sample values with your actual secrets in your CI/CD configuration.

##### ✅ How to Add Environment Variables in GitHub Actions

1. **Go to your GitHub repository**
   Navigate to the repository where you want to add secrets.

2. **Click on "Settings"**
   Located at the top right of the repo page.

3. **Select "Secrets and variables" > "Actions"**
   This is under the "Security" or "Code and automation" section.

4. **Click "New repository secret"**

5. **Add the secret**:

   * **Name**: `AWS_ACCESS_KEY_ID`
   * **Value**: `AKXXXXXXX7EXAMPLE`
   * Click **"Add secret"**

You can add these variable

##### 🔐 AWS Configuration

| Variable Name            | Sample Value                  |
|--------------------------|-------------------------------|
| `AWS_ACCESS_KEY_ID`      | AKIAIOSFODNN7EXAMPLE          |
| `AWS_SECRET_ACCESS_KEY`  | wJalrXXXXXXXX/K7MDENG/bPxRfiCYXXXXXXX |
| `AWS_REGION`             | us-east-1                     |

##### 🚀 ECS Deployment

| Variable Name            | Sample Value                  |
|--------------------------|-------------------------------|
| `ECR_REPOSITORY`         | my-ecr-repo                   |
| `ECS_CLUSTER`            | my-ecs-cluster                |
| `ECS_SERVICE`            | my-ecs-service                |
| `ECS_TASK_DEFINITION`    | my-task-definition:1          |

##### 📣 Slack Notification

| Variable Name            | Sample Value                  |
|--------------------------|-------------------------------|
| `SLACK_WEBHOOK_URL`      | https://hooks.slack.com/services/T000/B000/XXXX |

##### 🔐 SSH Configuration

| Variable Name            | Sample Value                  |
|--------------------------|-------------------------------|
| `SSH_HOST`               | ec2-12-34-56-78.compute.amazonaws.com |
| `SSH_PRIVATE_KEY`        | -----BEGIN RSA PRIVATE KEY-----\n... |