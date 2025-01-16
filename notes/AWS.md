# <u>IAM user</u>

* When you sign up for an account, you will sign up as a root user. For security reasons, it's best not to use your root user credentials, so once you sign up, set up an IAM user account for yourself. Select the region for your IAM user.
* Create an access key for your IAM user. This will come with an access key and a secret access key. These are required for your IAM user to programmatically access AWS via the AWS CLI. 
* In IAM, you can directly attach policies (basically, permissions) to users, but it's recommended to create groups and attach policies to groups instead. That way, you can simply add new users to the appropriate group. Some examples of AWS-managed policies include access to SageMaker, Lambda, ECR, etc.
* Install AWS CLI on your machine. Use the command `aws configure`. You will be prompted for your access key, your secret access key, and your region. These will be stored (in cleartext, which is not recommended) under `~/.aws/config` and `~/.aws/credentials`. Now you can access AWS resources with your IAM user credentials.

AWS CLI reference: https://awscli.amazonaws.com/v2/documentation/api/latest/reference/index.html

Useful commands:
* `aws sts get-caller-identity`: verify that you correctly set up your user credentials
* `aws iam list-groups-for-user --user-name <user-name>`: list the groups that user belongs to
* `aws iam list-attached-group-policies --group-name <group-name>`: list the policies attached to the group. Note that `list-group-policies` lists the inline policies - explicitly defined within the group - that are not shared across other entities. If you've only attached policies, then `list-group-policies` will return an empty list.
* `aws iam simulate-principal-policy --policy-source-arn arn:aws:iam::<account-id>:user/<user-name> --action-names <action-names>`: check if user has access to specific actions, e.g. `action-names` could be `s3api:list-buckets` (this would tell you if you can access the command `aws s3api list-buckets`). `simulate-principal-policy` will return a JSON object (in this case, the user has access):
```json
{
    "EvaluationResults": [
        {
            "EvalActionName": "s3api:list-buckets",
            "EvalResourceName": "*",
            "EvalDecision": "allowed",
            "MatchedStatements": [
                {
                    "SourcePolicyId": "AdministratorAccess",
                    "SourcePolicyType": "IAM Policy",
                    "StartPosition": {
                        "Line": 3,
                        "Column": 17
                    },
                    "EndPosition": {
                        "Line": 8,
                        "Column": 6
                    }
                }
            ],
            "MissingContextValues": []
        }
    ]
}
```

# <u>IAM roles</u>

You can attach roles to AWS services, like when you start an EC2 instance or create a Lambda function. These are like profiles or permissions for these services (like an IAM user) that allow them to access other AWS services. For example, if you create an EC2 instance, and you need to pull an image from ECR, you can give your EC2 instance a role that allows access to ECR. This is useful because then you don't need to sign in and use your own IAM user credentials - you use the credentials of the role attached to the EC2 instance. This is more secure and compartmentalized.

# <u>Simple Storage Service (S3)</u>

Make a bucket named `bucket-name`: `aws s3 mb s3://bucket-name`

Note: S3 bucket names must be globally unique, among ALL users, not just within your account.

```bash
aws s3api create-bucket \
    --bucket amzn-s3-demo-bucket1$(uuidgen | tr -d - | tr '[:upper:]' '[:lower:]' ) \
    --region us-west-1 \
    --create-bucket-configuration LocationConstraint=us-west-1
```

`aws s3 cp <file-to-upload> s3://bucket-name`

boto3 is installed on AWS lambda by default.

# <u>Elastic Compute Cloud (EC2)</u>



# <u>Elastic Container Repository (ECR)</u>

Reference: https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html

You can push and pull Docker images to and from ECR.

Using the command line,
* `aws ecr get-login-password --region <region>`: this gets an authentication token (basically a long random password)
* `docker login`: when prompted, use AWS for the username and the authentication token from the previous step for the password
* `aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com`: this combines the two previous steps into one easy command. Your authentication token will be saved under `~/.docker/config.json`. This is also known as the ECR registry entry.
* `docker tag <local-image-name:tag> <account-id>.dkr.ecr.<region>.amazonaws.com/<repo-name>:<tag>`: to push, you need to re-tag your image with the ECR repo name. For example, `docker tag my-app:latest <account-id>.dkr.ecr.<region>.amazonaws.com/all-apps/my-app:v1`.
* `docker push <account-id>.dkr.ecr.<region>.amazonaws.com/<repo-name>:<tag>`: push to repo
* `docker pull <account-id>.dkr.ecr.<region>.amazonaws.com/<repo-name>:<tag>`: pull from repo

When you push and pull, Docker looks for your configuration file (`config.json`), but it may not find the right one. When you run the Docker daemon using `sudo`, this gives you root user permissions, which means Docker is running as `root`. If you're not actually the root user, Docker may look in the wrong place and incorrectly determine that you do not have credentials to push and pull.

Recipe:
* Always use `sudo` for `docker` commands: `aws ecr get-login-password --region <region> | sudo docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com`. There will be an output message that tells you where the token is saved (it should be `/root/.docker/config.json`).
* Set the environmental variable `export DOCKER_CONFIG=/root/.docker`
* Push or pull

`aws ecr create-repository --repository-name <repo-name> --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE`

image tag mutable means that whenever we push a new image, it'll be tagged as latest