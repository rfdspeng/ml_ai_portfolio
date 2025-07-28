# Alignment techniques: instruction-based finetuning, RLHF

# Apache Spark



# CI/CD: GitHub Actions

# Data discovery

# Data extraction

# Data mining

https://en.wikipedia.org/wiki/Data_mining

Semi-automatic or automatic analysis of massive quantities of data to extract previously unknown, interesting patterns like
* Groups of data records (cluster analysis)
* Unusual records (anomaly detection)
* Dependencies (association rule mining, sequential pattern mining)

This usually involves using database techniques such as spatial indices. These patterns are a kind of summary of the input data and may be used in further analysis like ML and predictive analytics.

Difference b/w data analysis and data mining:
* Data analysis is used to test models and hypotheses on the dataset, regardless of data volume
* Data mining uses ML and statistical models to uncover patterns in large data volumes

# Data warehousing

Data lakehouse

# Data transformation pipeline:

# Databricks

* Cloud platform for data engineering, data science, ML. Scalable cloud infrastructure.
* Data lakehouse architecture
* Delta Lake
* Built on Apache Spark, a distributed processing framework that efficiently handles large datasets
* MLflow
* Notebooks

# Deep learning

https://www.ibm.com/think/topics/deep-learning

Subset of machine learning that uses multilayered neural networks (deep neural networks).

# Distillation

# Distributed training: PyTorch?

# Entity recognition

# Exploratory data analysis:

# Feature engineering: Preprocessing step in supervised ML and statistical modeling which transforms raw data into a more effective set of inputs. Each input comprises several attributes, known as features. Sklearn has a module called feature_extraction.
# Feature selection
# Feature store: https://www.qwak.com/post/what-is-a-feature-store-in-ml#:~:text=Finally%2C%20Feature%20Stores%20are%20feature%20storage%20systems,whenever%20input%20for%20a%20prediction%20is%20required.

# Foundation model

Also known as large X model (LxM) - ML/deep learning model trained on vast datasets so it can be applied across a wide range of use cases.

Very expensive to acquire, curate, and process massive datasets plus the compute power required for training.

Generally self-supervised training.

1B+ parameters.

All foundation models are pretrained models, but not all pretrained models are foundation models. 

Pretrained model: Any model that has been trained and then saved for reuse, e.g. ResNet-50 on ImageNet.

Foundation model: Massive model trained on broad, diverse data at scale, is general-purpose (not designed for a single task), and capable of adaptation to many downstream tasks with fine-tuning or prompting, e.g. GPT, LLaMA.

# Generative adversarial networks

# GraphRAG

# Image augmentation: https://docs.ultralytics.com/guides/yolo-data-augmentation/#saturation-adjustment-hsv_s

# Information extraction

# Infrastructure

# Kubernetes

# Large scale machine learning tools

# MLOps

# Model deployment/serving: ONNX Runtime
# Model optimization: https://www.ultralytics.com/glossary/optimization-algorithm
# Model serving/deployment
# Monitoring: Prometheus, Grafana

# Multi-modal models

# Orchestration

# ONNX: https://docs.pytorch.org/docs/stable/onnx.html

# PySpark

# Quantization

# Ray/

# Regression

* Multiple regression: multiple features
* Univariate regression: one output (prediction)
* Multivariate regression: multiple outputs (predictions)

# REST APIs

# Self-supervised learning (SSL)

https://www.ibm.com/think/topics/self-supervised-learning

ML technique that uses unsupervised learning for tasks that conventionally require supervised learning. Rather than relying on labeled datasets for supervisory signals, self-supervised models generate implicit labels from unstructured data.

Particularly useful in CV/NLP that require large datasets where manual labeling is extremely costly.

In SSL, tasks are designed s.t. ground truths can be inferred from unlabeled data.

Two SSL task categories:
* Pretext tasks: train the model to learn meaningful representations of unstructured data (pretraining)
* Downstream tasks: representations are subsequently used as input to a downstream task (transfer learning), like a supervised learning task or reinforcement learning task

# Semantic search

# Sequence models

# Statistical model

# Training-serving skew: https://www.qwak.com/post/training-serving-skew-in-machine-learning
# Recommendation systems: candidate generation, scoring, ranking https://aman.ai/recsys/candidate-gen/ 

# VLM