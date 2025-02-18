Experiment tracking, model packaging, model serving

Extremely important tool for MLE - hyperparameter tuning, tracking model performance

Registering your models, packaging models for deployment

Other ways to serve models: SageMaker, Ray, Lambda, Flask, FastAPI, native PyTorch and TF. What exactly does model serving mean? It means creating a server.

MLFlow can be used for complete ML lifecycle. What does this mean?

Terminal: `mlflow ui` for the dashboard. Looks for `mlruns` directory.

In the MLflow UI, you can select experiments using SQL's `WHERE` syntax, so learn some SQL.

You can package your MLflow project so other people can run it too. You need
* `requirements.txt`
* `MLproject`
* Your code, e.g. `train.py`

Then you can run `mlflow run <mlflow-dir>`, e.g. `mlflow run .` after creating a virtual environment and installing the libraries in `requirements.txt`.

You can define the `conda` environment inside `MLproject`, but if you're using a local environment, e.g. a `venv` folder in your project directory, then you can specify `mlflow run . --env-manager local`.

This runs with default parameters. To specify parameters, `mlflow run . -P alpha=0.0001 -P l1_ratio=0.9999 --env-manager local`.

What does it mean to register a model? Does this do anything if I'm registering it locally? All this registering and serving locally seems to mean no one else can access it, so what's the point?

After you register the model, you can serve it locally and use `curl` to `POST` data to the model.