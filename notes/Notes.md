# Lec 11/19/2024

## API

Try Cursor for improved coding speed.

FastAPI is preferred to Flask because it allows asynchronous programming. 

pydantic: input data validation; improves documentation. ip-addr:port/docs

streamlit for front-end. Understand SW architecture. Front-end, back-end, etc.

streamlit can be used to deploy. 

Understand the different types of terminals. Git Bash enables Linux commands but runs on Windows. 

IDE? SDK?

code . to open VSCode in current folder. You can change the terminal type inside VSCode - how to install other types?

## ML model serialization

Serialization: convert model into binary format (bytestrings) and saved to binary file. Any Python object can be serialized and loaded.

Saving a scikit-learn model to a pickle file is model serialization. 

joblib is another library, and it's preferred to pickle.

You need to import scikit-learn for this to work.

PyTorch has a different process. You can save just the weights (model.state_dict()), or you can save the entire model (model), including the architecture. `torch.save()`. Weights-only is preferred - lightweight saving. But you do need to save the class somewhere. Also, you can only modify the architecture if you have the class, so might as well save weights-only.

(In general, ) TensorFlow is simpler but restricted. PyTorch is more complicated but allows more freedom. PyTorch is generally preferred in industry.

ONNX (Open Neural Network eXchange) streamlines this process - it works for all models, and you don't need to import the library that the model is based on. You convert the library model to ONNX format, and ONNX-formatted model is used for inference.

PyTorch supports ONNX natively. torch.onnx.export(). You need to install libraries for scikit-learn-to-ONNX and TensorFlow-to-ONNX conversion. Hugging Face models are in PyTorch by default.

Where is ONNX important? ONNX is efficient way to run inference. Supports graph optimization, quantization.

To run inference on GPU, you need to install the GPU-specific ONNX runtime.

## Workflow

1. Push dockerized code to GitHub.
2. On EC2 instance, pull the code.
3. Deploy the code using Flask API, fast API, or streamlit (use the stored ONNX model form S3 bucket)

# Lec 11/21/2024

nginx (reverse proxy server, helps in load balancing). 

Let's say 10 people are using your AI application, which is served via Flask (wsgi). The way it works is requests are served sequentially. Serve first, then second, then third, etc. This is very slow. Serial processing.

FastAPI (asgi) is asynchronous - multiple requests are served concurrently. This is preferred.

Let's say you have 1 million people requesting. Your EC2 instance would crash. 

Instead, you would have 100 EC2 instances, each with your AI application installed on FastAPI. The 101st EC2 instance would have nginx installed to do load balancing among the 100 EC2 instances.

uvicorn is also installed on the 100 instances. It takes HTTP request and converts it to Python-readable format. Gives it to Fast/Flask, which returns something in json format. json back to uvicorn, which then converts to HTML. Then back to nginx for serving purpose on client side web browser.

HTTP requests are posted in HTML?

## MLFlow

`pip install mlflow`

# Lec 11/26/2024

SageMaker

Notebook instances are like Google Colab. Pay for how much time you use and the resources.

Studio - everything in one place, including notebook instances

Canvas - ML without code. How does this work? Who is Canvas for? Why would we ever use it? Quick prototyping; companies that don't have MLE. Won't use this as developers, but we should know that this tool exists. Waqas has not compared these models to models he's trained himself.

Need to set up SageMaker Domain to work with notebook instances - it's like an IAM user with specific access (AmazonSageMakerFullAccess)

# Lec 11/28/2024 - bias and explanability

Bias (against gender, race, etc.) in text data

Explainability - shapley and lime. Need to be able to explain how a model gets its predictions (e.g. coefficients in linear regression or decision points in decision trees - these are explainable). Neural networks are black boxes - can't really understand how the input features affect the output. 

Explainability - how the inputs impact the output. 

What if your features were ratios of the default feature, and the cost function was say, mineral quality. Implement a cost function s.t. cost rapidly rises once mineral quality degrades below a threshold. Then could you use gradient descent to figure out the optimal features? Uhh not sure. How did clipper work?


Ray - use multiple cores for parallel processing. Big data processing. PySpark same thing. How big is big?
* GPU and CPU?
* Where could we best put Ray to use? Hyperparameter tuning (yes)? Layers of Ray? E.g. distributed training, distributed tuning, distributed eval.
    * Data preprocessing
    * Parallel training - you're not parallelizing across batches if you update per batch - you're parallelizing a single batch
    * Batch is already parallelized
    * Use it with MLFlow. What about Optuna?

Flask (not async), FastAPI (async), MLFlow, SageMaker (async), Ray (not async), Lambda - can all deploy