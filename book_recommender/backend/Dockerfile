FROM public.ecr.aws/lambda/python:3.12

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

# RUN python -m pip install --upgrade pip \
#     && apt-get update \
#     && apt-get install -y gcc \
#     && apt-get clean \ 
#     && rm -rf /var/lib/apt/lists/*

# RUN python -m pip install --upgrade pip \
#     && apt update \
#     && apt install -y gcc \
#     && apt clean \ 
#     && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip \
    && dnf update -y \
    && dnf install -y gcc \
    && dnf clean all

RUN pip install --no-cache-dir -r requirements.txt

COPY models ./models
COPY __init__.py .
COPY lambda_function.py .
COPY .env .

CMD [ "lambda_function.lambda_handler" ]