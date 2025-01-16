A **serverless function** is a piece of code that triggers on certain events, events that you define. It is serverless because you do not provision or manage the server that the code will run on; the cloud provider does it for you. AWS Lambda is Amazon's implementation of serverless functions.

The name of the top-level function is `lambda_handler`, and it takes an `event` as argument. `event` is a dictionary-like data structure. Example:
```python
import json

print('Loading function')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    print("value1 = " + event['key1'])
    print("value2 = " + event['key2'])
    print("value3 = " + event['key3'])
    return event['key1']  # Echo back the first key value
    #raise Exception('Something went wrong')
```

Project directory structure:
* Top-level folder has the name of your function
* Within this folder, there is a `lambda_function.py`
* Within `lambda_function.py`, there is a `lambda_handler` function

For a web application, the trigger of your Lambda function is the API Gateway.

The output of your Lambda function can be managed via "Add destination". You can send the output of your Lambda function to another Lambda function; this is useful in time-intensive applications since Lambda functions can only run for maximum 15 minutes. AWS provides something called Step Functions to make this process of chaining Lambda functions easier.

You can create a Lambda function via a SAM (AWS Serverless Application Model) template
* Properties
    * MemorySize: X MBs (RAM)
    * Timeout: X seconds
    * EphemeralStorage: X MBs (disk)
    * Policies: permissions attached to the role associatd with this function

Runtime dependencies:
* You can specify environment variables
* You can upload your project directory as a zip file from local or from S3 (with the necessary packages installed, like numpy)

AWS CLI:
* `aws iam create-role --role-name <role-name> --assume-role-policy-document 'something-here'`
* `aws iam attach-role-policy --role-name <role-name> --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole`
* `aws lambda create-function --function-name <function-name> --zip-file <zip-file-name> --handler lambda_function.lambda_handler --runtime python3.10 --role <role-arn>`





Function ARN = function endpoint?

You pay only for the time your function runs. There's no dedicated server; you don't manage any server, but it's all handled by the server provider.

You need to give the IAM user access to Lambda: AWSLambdaFullAccess, AmazonAPIGatewayInvokeFullAccess

There are a few ways to create a Lambda function, including writing the code yourself or using a container image. My function will be in Python, but you can use other languages too.

You need to define a role for your function, which manages what your function has access to. For example, does your function need access to other AWS services?



Can Lambda support an interactive web application?

Before, we used nginx and uvicorn to respond to client requests posted to our API endpoint. But we don't have that anymore, so we need the API Gateway. 

You need to define which events trigger your Lambda function and also where to send the output of your Lambda function (which can be another Lambda function). Lambda functions can only run for 15 minutes, so you may need to chain functions. You can also take a look at AWS Step Functions for this.

You need to define how much memory you need for your lambda function (max of 10GB). This is ephemeral storage, under `/tmp/`.

You can define the timeout (max of 15 mins).

You can define environment variables.

You can also package multiple files into a .zip and upload it to AWS from your local computer or from an S3 bucket.

Project folder name = function name. Within this folder, you must have a `lambda_function.py` and inside `lambda_function.py`, you need a `lambda_handler` function. 

Within `lambda_function.py`, you cannot import any libraries that aren't installed by default (e.g. you can't say `import numpy`). This isn't on a dedicated server. The only way you can do this is having a `numpy.py` in your project folder. This is runtime.

To include dependencies (libraries), you need to zip the packages. In your virtual environment folder, `venv/lib/python3.12/site-packages`, run `zip -r9 {proj_folder}/packages.zip .`. And then you need to add `lambda_function.py` to the zip file, but I missed this part.

Go to CloudWatch for logs to debug.

To containerize your function, you might want to create the virtual environment from env.yml, so that way you create the environment in the same way as the image will create the environment.

Dockerfile format:
```python
FROM public.ecr.aws/lambda/python:3.12

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN yum install gcc -y # for AWS
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}" #/var/task/

COPY lambda_function.py ${LAMBDA_TASK_ROOT}

ENV SURPRISE_DATA_FOLDER=/tmp/.surprise_data

CMD [ "lambda_function.lambda_handler" ]

```

If you have a model, load it to `/tmp/` so it persists? But it's a Lambda function. I think you need to store the model in persistent memory?

Push the image to elastic container registry (ECR). Amazon ECR is like Docker Hub. Then you can create a lambda function from the Docker image and connect it to API Gateway to serve HTTP requests.

You need to create a repository, which you can do from your browser. You can also do it via the CLI:
* `aws ecr get-login-password --region us-east-2`
* `docker login --username AWS --password {password}`
* `aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin {ecr-link}`
* `aws ecr create-repository --repository-name {repo-name} --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE`
* 


# <u>Using the AWS CLI</u>

* `aws iam create-role --role-name lambda-ex-3 --assume-role-policy-document ...`
* `aws iam attach-role-policy --role-name lambda-ex-3 --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole`
* `aws lambda create-function --function-name waqas-demo-math-function --zip-file fileb://demo-math-function-package.zip -- handler lambda_function.lambda_handler --runtime python3.10 --role arn:aws:iam::{account_id}:role:lambda-ex-3`
* `aws s3 mb s3://lambda-demo`
* `aws s3 cp resize-image.zip s3://lambda-demo`
* `aws lambda invoke --function demo-math-function --cli-binary-format raw-in-base64-out --payload '{"action": "square, "number": 3}' output.txt`


# <u>AWS API Gateway</u>

You need to define different endpoints in `lambda_function.py`. E.g., you need to define `PREDICT_PATH = /predict` in the file, and the event handling syntax changes: `event['rawPath'] == PREDICT_PATH`.

We'll use HTTP API. Integration with Lambda; pick the Lambda function.

You get an Invoke URL for which you can send your HTTP requests.

# <u>DynamoDB</u>

NoSQL database (JSON format)
AmazonDynamoDBFullAccess
I don't think you can store models on here. This is better for working with datasets. S3 is more like a data lake.