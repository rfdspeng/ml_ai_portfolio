# References

* Hands-On Machine Learning

# Deployment

Prepare solution for production (polish code, write documentation and tests).

Deploy model to production environment. Save your preprocessing+model pipeline (pickle, joblib, ONNX) and load it within your production environment.

Serialization is important.
* Save the model for later use
* Deploy model to different environments (web server, embedded systems)
* Share model with others
* Version control

Example deployment as a web app:
* Model to be used on a website
* User makes a query on the website
* Query containing data is sent to web server, which forwards to web app, which calls the model's `predict()` function
* Load model on server startup rather than every time the model is used

Example deployment as a web service:
* Wrap model within a dedicated web service that your web app can query through a REST API
    * Easier to upgrade your model to new versions without interrupting the app
    * Simplifies scaling since you can start as many web services as needed and load-balance the requests from the web app across the web services
    * Allows web app to use any language, not just Python

Example deployment using a managed cloud service:
* Deploy the model on a cloud platform
* This gives you a simple RESTful web service that takes care of load balancing and scaling for you

# Monitoring

Write monitoring code to check system live performance at regular intervals and trigger alerts when it drops.
* Could be a steep drop due to a broken component in your infra
* Could be a gentle decay as the model "rots" over time as the world (and its data) changes

How to monitor?
* Sometimes model performance can be inferred from downstream metrics, e.g. monitoring recommended products sold in a recommender system. Data pipeline could be broken or the model may need to be retrained on fresh data.
* Sometimes you may need human analysis - humans to check a subset of the model's predictions. These could be employees or the users themselves.

You should also monitor the input data to the model, which may tell your earlier if something is wrong. Look for
* Missing features
* Summary statistics drifting from the training data
* New categories in categorical features

You need processes in place to prepare for and handle failures.

# Retraining

If the data keeps changing, you need to retrain your model regularly.

Ideally, you would automate these:
* Collect fresh data and label it (e.g. with humans)
* Train the model and fine-tune the hyperparameters
* Compare the new model and old model
* Deploy the new model if performance has not decreased

# Rolling back

Keep backups of every model and dataset so you can easily roll back models and datasets.