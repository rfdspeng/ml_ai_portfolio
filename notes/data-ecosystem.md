# <u>Data jobs</u>

Data science
* Role: extract insight from data using stats, programming, domain knowledge
* Core activities: EDA, data viz, stat modeling, experiments (A/B tests)
* Tools: Python, R, SQL, Tableau, Power BI
* Jobs
    * Data analyst: descriptive and diagnostic analytics using reports and dashboards
    * Data scientist: predictive and prescriptive analytics; simple ML models or pipelines

Machine learning
* Role: build and deploy models to learn from data and make predictions
* Core activities: data preprocessing, including feature engineering; training and tuning models; evaluating and deploying models
* Tools: Scikit-learn, TF, PyTorch, Hugging Face, MLFlow
* Jobs
    * ML engineer: develop, deploy, and optimize ML models using frameworks like PyTorch
    * Data scientist (with ML focus): ML + stats to extract insights
    * Applied scientist: research new ML methods and apply them to real problems

AI
* Role: build systems that mimic human intelligence
* Core activities: designing and deploying intelligent agents (chatbots, recommenders); developing generative models (GPT); CV, NLP, reinforcement learning
* Tools: PyTorch, TF, OpenAI APIs, robotics
* Jobs
    * AI researcher: create or improve algorithms
    * AI engineer: implement AI systems for applications
    * Robotics engineer: design intelligent robots

The overall flow looks something like
1. Foundation: data collection and management. Data engineers create the infrastructure for data pipelines and storage.
2. EDA: Data scientists and analysts explore the data to extract insights or prepare it for ML.
3. Modeling: Data scientists and ML engineer engineers build predictive and prescriptive models, while AI engineers create intelligent systems.
4. Deployment and maintenance: MLOps engineers integrate models into an execution/monitoring pipeline.

# <u>Pipelines</u>

"The ability to build workflows that process and transform data and systematically and automatically handle tasks."

Workflow orchestration tools (design, schedule, and monitor tasks in a pipeline): Apache Airflow, Prefect, Luigi.

Pipeline components:
* ETL (extract, transform, load)
    * Ingestion: collecting raw data (from databases, e.g. SQL, NoSQL; APIs; sensors or IoT devices)
    * Transformation: processing the data (cleaning, normalizing, encoding, feature engineering, etc.) using SQL; Pandas (small-to-medium datasets); Spark or Dask for distributed/parallel computing on large datasets
    * Storage: send the processed data to a database, data lake, or cache for further use. Usually at this point, the data is in the format expected by the model.
        * Databases: relational (PostgreSQL, MySQL) or NoSQL (MongoDB)
        * Data lakes: AWS S3, Azure Blob Storage, Google Cloud Storage
        * Caches: Redis, Memcached
        * Format: TFRecord, Parquet, CSV
* Execution: running tasks like training, refining, and testing a model; and deploying the model to generate predictions.
    * Frameworks
        * MLFlow: experiment tracking, model deployment, lifecycle management
        * Kubeflow: Kubernetes-native platform for ML pipelines
        * TensorFlow Extended (TFX): end-to-end pipeline for TF models
    * Cloud
        * AWS: S3 (storage), Lambda (serverless compute), SageMaker (ML lifecycle management)
        * GCP: BigQuery (data querying), Dataflow (data pipelines), Vertex AI (model lifecycle)
        * Azure: Synapse (data integration), Azure ML (model training and deployment)
    * Containerization: Docker, Kubernetes
* Monitoring and logging
    * Monitoring: track pipeline performance (latency, throughput, error rates); monitor model drift (changes in data distribution over time that impact predictions)
    * Logging: logs for debugging and understanding pipeline behavior. ELK Stack for centralized log management.
    * Tools: Grafana (visualize real-time metrics and alerts); Prometheus (collect and query time-series metrics); ML-specific monitoring (Fiddler AI, WhyLabs, AWS Model Monitor) for tracking model behavior

A pipeline should
* Have parallelism: splitting tasks to run in parallel for faster processing
* Choose between real-time (stream) or scheduled (batch) pipelines based on requirements
* Handle failures gracefully and resume from checkpoints
* Be scalable to efficiently handle growing data volumes or ML workloads

How to learn pipeline design skills:
1. Learn pipeline tools
    * Airflow or Prefect
    * MLFlow, TFX, Kubeflow
2. Practice ETL
    * Extract data from APIs or databases
    * Transform the data using Pandas, Spark, or SQL
    * Load the data into databases, data warehouses, or visualization tools
3. Work on the cloud
    * AWS Lambda, S3, SageMaker
    * Set up serverless workflows
4. Learn debugging and monitoring
    * Use Grafana to visualize pipeline performance
    * Create fail-safes to recover from errors

Example pipeline:
1. Collect raw text data from an API daily
2. Clean and tokenize the data using Python scripts
3. Load the cleaned data into an S3 bucket
4. Trigger a training job on a SageMaker instance
5. Deploy the trained model and monitor its inference latency with Prometheus

## <u>Pipeline metrics</u>

**Latency**: the time it takes to process a single unit of data through the pipeline or pipeline component, e.g.
* In ETL, how long it takes to ingest, transform, and store data
* In model deployment, how long it takes the model to produce predictions given a new input

Latency affects real-time capabilities, e.g. user-facing applications like recommendations.

**Throughput**: the volume of data processed by a pipeline over a period of time, measured in rows/records/transactions per second, e.g.
* In ETL, the number of records that can be ingested, processed, and stored per second
* In model deployment, the number of inference requests the model can process per second

Throughput affects how much data you can handle during peak loads.

**Error rate**: the proportion of data that fails at any stage of the pipeline or produces incorrect results, reported as a percentage of total data, e.g.
* In ETL, failed API calls, malformed records, or transformation errors (schema mismatches, out-of-range values, null values in critical fields)
* In model deployment, predictions that violate expected constraints (e.g. negative probabilities) or exceed tolerable accuracy thresholds.

Error rate affects data quality and system stability.

It's important to monitor these metrics to identify bottlenecks and scale or optimize components as needed.

## <u>Server-based vs. serverless workflows</u>

Feature | Server-Based Workflow | Serverless Workflow
--------|-----------------------|--------------------
Compute Resource|Set up VMs, containers, or physical servers|Abstracted; no visible servers, managed by the provider
Scaling|Manual or auto-scaling based on setup|Automatic scaling built-in
Cost Model|Pay for uptime (even if idle)|Pay only for execution time
Management|User manages servers, OS, updates|Provider manages infrastructure
Execution trigger|Custom-defined processes or schedules|Event-driven (e.g. API call, file upload)

Basically, a server-based workflow uses persistent server(s) that are you responsible for managing. A serverless workflow allocates provider-managed server resources based on triggering events. Serverless functions are called in serverless workflow to process data, train models, etc.

Example server-based workflow:
1. Launch an EC2 instance
2. Install libraries and tools (e.g. Python)
3. Create a cron job to run a script at regular intervals
4. Monitor and manage the instance to ensure it remains operational

Example serverless workflows:
* Data pipeline
    * Trigger: file uploaded to S3
    * Process: serverless functions clean and format the data
    * Store: write the processed data to a database
* ML pipeline
    * Trigger: new dataset uploaded
    * Process: serverless function trains the model on a cloud ML service
    * Deploy: deploy model to endpoint

Serverless workflow tools: AWS Step Functions, Google Cloud Workflows, Azure Logic Apps  
Serverless function frameworks: AWS Lambda, Google Cloud Functions, Azure Functions

Serverless workflow benefits:
* No server management: focus only on development
* Cost efficient (pay only for execution time and resources)
* Automatic resource scaling

Serverless workflow challenges:
* Cold starts: initial latency when functions are triggered after being idle
* Limited execution time: functions may have timeouts
* More difficult to debug and monitor because of distributed and event-driven workflow

# <u>Data analytics</u>

Data analytics is anything that involves using data to generate insights.

Key steps:
1. Data collection, often facilitated by a data pipeline
2. Data cleaning and preparation
3. Data exploration, or more formally, EDA: visualize, get statistics, and try to understand the data
4. Apply statistical or machine learning models to generate insights or predictions
5. Present (dashboards, reports, visualization)

Types of data analytics:
1. Descriptive analytics: describe past data, e.g. sales over the last quarter. Tools: simple visualizations, reports, and summary statistics.
2. Diagnostic analytics: based on data, determine why something happened. Tools: correlation analysis, root cause analysis.
3. Predictive analytics: use historical data to predict future outcomes. Tools: ML/DL models.
4. Prescriptive analytics: recommend actions based on data and potential outcomes. Tools: ML/DL models, optimization algorithms, recommendation systems.

Descriptive and diagnostic analytics is more traditional data analytics, while ML/DL is more predictive and prescriptive.

## <u>"Data exploration" vs. exploratory data analysis (EDA)</u>

Data exploration is a broad term for very basic analysis of data. The focus is to gain a quick, high-level understanding of the data. Techniques include simple stats (mean, median, stdev); simple plots (histograms, scatterplots); data types, ranges, and nulls.

EDA, proposed by John Tukey, is deeper exploration. The focus is to identify relationships, distributions, and trends; detect potential problems like outliers, multicollinearity, or skewness; and generating hypotheses or guiding feature engineering for ML models. Techniques include advanced stat methods (correlations, hypothesis testing); sophisticated plots (boxplots, pair plots, heatmaps); dimension reduction techniques like PCA for multivariate analysis; and creating derived features for better understanding. EDA is often iterative.

# <u>Data analysis techniques</u>

https://builtin.com/data-science/types-of-data-analysis

Sort from simple to complex.

**Descriptive analysis** generates a simple summary or visualization of the data
* Mean, median, mode, standard deviation, variance, range
* Histograms, scatter plots, box plots, bar charts

**Diagnostic analysis** seeks to answer the question "Why did this happen?"
* Typically comes after descriptive analysis when we want to investigate why certain patterns appear in the data (e.g. to explain anomalies)
* May involve analyzing related data sources (e.g. analyzing past data to explain current trends)
* Example: a footwear store finds that its website traffic surged in June (descriptive). To investigate, they further break down the data by footwear type and find that the additional traffic in June is caused by views of sandals.

**Exploratory data analysis (EDA)** is examining the data to find relationships between variables.
* Useful for formulating hypotheses, e.g. "X has this effect on Y". To be clear, however, this analysis only shows correlation, not causation.
* Drives data collection because it helps answer the question "What data do we need to test our hypothesis?"
* Example: if you look at the increase in human industrial activity and the increase in global temperatures, you will find a positive correlation.

https://www.geeksforgeeks.org/what-is-inferential-statistics/

**Inferential statistics/analysis** uses a small sample of data to make inferences about a larger population of data. It allows us to
* **Generalize insights** from a sample to the population
* **Test hypotheses** to validate assumptions or claims about the data
* **Quantify uncertainty** by calculating confidence intervals and p-values
* **Make predictions** using statistical models

_In essence, inferential statistics provides the tools to go beyond the data you have and make informed decisions about the data you don't._



```
* A/B testing
* Hypothesis testing: determines if there's enough evidence to reject a hypothesis. Examples: T-tests, Z-tests, chi-square tests, ANOVA
* Regression analysis: examines the relationship between a dependent variable and one or more independent variables. Examples: linear regression, logistic regression
* Time series analysis: analyzes data points collected over time to identify trends, seasonality, and patterns
* Bayesian inference: uses prior knowledge and observed data to update beliefs or probabilities
```

**Predictive analysis** trains statistical models to make predictions (supervised learning like classification and regression).
* Using a feature to predict a label does not imply a causal relationship
* Example: training a prediction model on historical polling data, trends, and current polling data to predict the winner of an election

**Causal analysis** like randomized control trials to test the effect of a drug.

**Mechanistic analysis** is used to understand the mechanisms that cause a change in one variable to propagate to changes in other variables.

**Prescriptive analysis** takes the results of predictive analysis (and other analyses) to prescribe some course of action to achieve a desired outcome. Example: on platforms like TikTok and Instagram, algorithms can apply prescriptive analysis to review past content a user has engaged with and the kinds of behaviors they exhibited with specific posts and recommend similar content. What are some prescriptive ML models?


ML is a subset of both AI and data science.



Other important techniques:
* Exploratory data analysis (EDA):
* Predictive analysis
* Causal or diag analysis
* Prescriptive analysis
* Correlation analysis

Descriptive: what happened
Diagnostic: why did it happen
Predictive: what is likely to happen (statistical modeling)
Prescriptive: what should we do?

# <u>Statistical modeling vs. machine learning</u>

Statistical modeling is things like regression, classification. I think the difference between statistical modeling and ML is that SM prioritizes model interpretability. For example, when you construct a linear regression model, you can easily see how much each feature contributes to the overall prediction. That's also why feature engineering goes hand-in-hand with statistical modeling, because you need to consider the features carefully.

ML is more brute force. You keep increasing the number of parameters and let the training figure out the features/derived features. You have no idea what the features mean or what any of the numbers inside the ML model mean (black box).

# <u>Data engineering</u>

https://www.mongodb.com/resources/basics/data-engineering

Key elements of data engineering:
* Data extraction/collection: creating systems to extract data of varying formats from multiple sources. Examples of sources:
    * Structured customer data in relational databases and data warehouses
    * Semi-structured data like email and website content stored on a server
    * Unstructured data like video, audio, and text files stored in a data lake
* Data ingestion: data source identification, data validation, indexing, cataloguing, and formatting.
* Data storage: designing storage solutions to house ingested data, e.g. picking the types of databases and the schemas. I would lump data modeling here.
* Data transformation: cleaning, enriching, and integrating raw data with other sources, and loading the processed data into data analytics systems to be used by data analysts and data scientists.
* Data modeling, scaling, performance
* Data quality and governance

What's in a data pipeline?

What is the flow of data in a pipeline?

How does ETL fit into this? Is ETL = collection + ingestion + transformation + storage?

Technical skills:
* Data warehousing: database design, query optimization, schema modeling
* Data pipeline orchestration: orchestrating and scheduling data pipelines

Data lake vs. warehouse vs. lakehouse

SQL vs. NoSQL

## Data pipelines according to Snowflake
https://www.snowflake.com/guides/data-pipeline/

A data pipeline moves data from a source to a destination while simultaneously optimizing and transforming the data. The data arrives at the destination ready to be used by data analysts and data scientists.

A pipeline includes aggregating, organizing, and moving data. Typically, this includes loading raw data into a staging table for interim storage, changing it, and inserting it into the destination reporting tables.

Your organization may have a massive amount of data that resides in multiple locations. To use it all, you need a way to pipe that data into one location.

Data pipeline elements:
1. Sources: where the data comes from. Databases, CRMs, ERPs, IoT device sensors, etc.
2. Processing steps: manipulating and changing the data. Transformation, augmentation, filtering, grouping, aggregation.
3. Destination: where the data is deposited. Data lakes, warehouses, and lakehouses.

ETL systems are a kind of data pipeline: they move data from a source, transform it, and then load it into a destination. ETL usually exists as a subprocess of a data pipeline, but not all data pipelines will have ETL.

## <u>Data pipelines according to IBM</u>
https://www.ibm.com/think/topics/data-pipeline

### <u>Ingestion, processing, storage</u>

A data pipeline ingests raw data from various data sources, transforms the data, and then ports it to a data store for analysis.

Pipelines act as the "piping" for data science projects or BI dashboards. Data can be sourced through a wide variety of places - APIs, SQL and NoSQL databases, files, etc. Usually, that data isn't ready for immediate use. Data needs to be processed (which includes transformations) to make sure it matches the format required by the destination storage. This is especially important when the storage is a relational database, which stores data in tables with specific columns and data types.

During sourcing, data lineage is tracked - where the data comes from, how it's changed, and its ultimate destination within the pipeline.

Data preparation/processing usually falls on data scientists or data engineers. Data scientists determine the required processing through a mix of EDA and defined business requirements, while data engineers spin up the infrastructure necessary to automate the processing for huge amounts of data.

Once processed and stored into the final data store, the data is ready for use in data projects like data analysis, data visualization, and machine learning.

### <u>Types of data pipelines</u>



### <u>Data pipeline architecture</u>



### <u>Data pipeline vs. ETL pipeline</u>



