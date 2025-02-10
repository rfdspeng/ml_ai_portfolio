import mlflow
import numpy as np
from sentence_transformers import SentenceTransformer
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import re
from torch import nn, optim
from torchmetrics.classification import Accuracy, Precision, Recall, F1Score, Specificity, AUROC, ROC
from sklearn.model_selection import train_test_split
import random
import itertools
from typing import Any

# def train_and_log_model(model, model_name, params):
#     with mlflow.start_run(run_name=model_name):
#         model.set_params(**params)
        
#         model.fit(X_train, y_train)
#         y_pred = model.predict(X_test)

#         mse = mean_squared_error(y_test, y_pred)
#         r2 = r2_score(y_test, y_pred)
#         mae = mean_absolute_error(y_test, y_pred)

#         mlflow.log_params(params)
#         mlflow.log_metric("mse", mse)
#         mlflow.log_metric("r2", r2)
#         mlflow.log_metric("mae", mae)

#         mlflow.sklearn.log_model(model, model_name)

#         print(f"Model {model_name} trained and logged with MSE: {mse}, R2: {r2}, and MAE: {mae}")

# ridge_params = [{"alpha": alpha} for alpha in [0.01, 0.1, 1, 10]]
# tree_params = [{"max_depth": depth} for depth in [2, 5, 10, None]]

# for params in ridge_params:
#     train_and_log_model(Ridge(), "Ridge", params)

# for params in tree_params:
#     train_and_log_model(DecisionTreeRegressor(), "Decision Tree", params)

class ClassificationHead(nn.Module):
    """ Classification Head """

    def __init__(self, embedding_size: int, num_classes: int):
        super(ClassificationHead, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(embedding_size, num_classes),
        )
    
    def forward(self, features: torch.Tensor):
        x = features["sentence_embedding"]
        x = self.layers(x)
        return x

class SentenceTransformerWithHead(nn.Module):
    """ SentenceTransformer + Head """

    def __init__(self, transformer: SentenceTransformer, head: ClassificationHead):
        super(SentenceTransformerWithHead, self).__init__()
        self.transformer = transformer
        self.head = head
    
    def forward(self, input: dict[torch.Tensor, torch.Tensor]):
        # input['input_ids']
        # input['attention_mask']
        features = self.transformer(input)
        logits = self.head(features)
        return logits

class QueryDataset(Dataset):
    """ Custom Dataset """

    def __init__(self, csv_file: str | None=None, df: pd.core.frame.DataFrame | None=None):
        if csv_file is not None:
            self.df = pd.read_csv(csv_file)
        elif df is not None:
            self.df = df
        self.df = self.df.astype({"Label": "int64"})
    
    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        item = {
            "Query": row["Query"],
            "Label": row["Label"],

        }
        return item

def create_loaders(csv_file: str="intent_classifier_samples.csv", batch_size: int=64):
    """ Create DataLoaders """

    df = pd.read_csv(csv_file)
    train_idx, val_idx = train_test_split(range(len(df)), test_size=0.3, stratify=df["Label"], random_state=0)
    df_train = df.iloc[train_idx]
    val_idx, test_idx = train_test_split(val_idx, test_size=0.5, stratify=df.iloc[val_idx]["Label"], random_state=0)
    df_val = df.iloc[val_idx]
    df_test = df.iloc[test_idx]

    ds_train = QueryDataset(df=df_train)
    ds_val = QueryDataset(df=df_val)
    ds_test = QueryDataset(df=df_test)

    train_loader = DataLoader(ds_train, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(ds_val, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(ds_test, batch_size=batch_size, shuffle=False)

    print(f"Created DataLoaders from {csv_file}.")
    return (train_loader, val_loader, test_loader)

def create_model(device: str="cpu", freeze: str="no"):
    """
    Create models


    freeze = "no", "base transformer"
    
    """

    model = SentenceTransformer("all-MiniLM-L6-v2", device=device)
    embedding_size = model.get_sentence_embedding_dimension()
    head = ClassificationHead(embedding_size, num_classes)
    model_with_head = SentenceTransformerWithHead(model, head)
    head.to(device)
    model_with_head.to(device)
    print("Created SentenceTransformer with classification head.")

    if freeze == "no":
        print("All layers unfrozen.")
    else:
        if freeze == "base transformer":
            for name, param in model_with_head.named_parameters():
                if not re.search(r"^head", name):
                    param.requires_grad = False
        
        print("Unfrozen layers: ")
        for name, param in model_with_head.named_parameters():
            if param.requires_grad:
                print(name)
        print("-------------------")

    return (model, head, model_with_head)

def create_metrics(num_classes: int, device: str="cpu"):
    """ Create classification metrics """

    if num_classes == 2:
        f1 = F1Score(task="binary", average="macro")
        accuracy = Accuracy(task="binary", average="macro")
    elif num_classes > 2:
        f1 = F1Score(task="multiclass", num_classes=num_classes, average="macro")
        accuracy = Accuracy(task="multiclass", num_classes=num_classes, average="macro")

    metrics = [accuracy, f1]
    metrics = [metric.to(device) for metric in metrics]
    return metrics

def train(model: torch.nn.Module, hyperparameters: dict[str, Any], loaders: dict[str, torch.utils.data.dataloader.DataLoader], metrics: list | None=None, earlystopping: dict[str, Any] | None=None):
    """
    Training function 
    
    earlystopping:
    * "metric": str (metric to use for early stopping)
    * "n_epochs": int (stop if metric hasn't improved after n_epochs)
    * "lower_is_better": bool (if True, then lower metric is better; otherwise higher metric is better)

    """

    n_epochs = hyperparameters["n_epochs"]
    lr = hyperparameters["lr"]

    device = next(model.parameters()).device
    metrics = [metric.to(device) for metric in metrics]
    print(f"Training on device {device.type}.")

    train_loader = loaders["train_loader"]
    val_loader = loaders["val_loader"] if "val_loader" in loaders else None

    loss_function = nn.CrossEntropyLoss(reduction="sum")
    optimizer = optim.AdamW(model.parameters(), lr=lr)
    # lr_scheduler = optim.lr_scheduler.ExponentialLR(optimizer, 0.999)

    # For debugging
    training_epochs = {
        "Train Loss": np.ones(n_epochs)*-999,
    }
    training_epochs.update({"Train " + metric._get_name(): np.ones(n_epochs)*-999 for metric in metrics})
    if val_loader is not None:
        training_epochs["Val Loss"] = np.ones(n_epochs)*-999
        training_epochs.update({"Val " + metric._get_name(): np.ones(n_epochs)*-999 for metric in metrics})

    # Training loop
    best_epoch = 0
    best_metric = 0
    for edx in range(n_epochs):
        cum_loss = 0
        metrics = [metric.reset() for metric in metrics]
        for bdx, batch in enumerate(train_loader):
            optimizer.zero_grad()

            inputs = model.tokenize(batch["Query"])
            inputs = {key: value.to(device) for key, value in inputs.items()}
            labels = batch["Label"].to(device)

            logits = model_with_head(inputs)

            loss = loss_function(logits, labels)
            cum_loss += loss.item()
            loss.backward()
            optimizer.step()
            # lr_scheduler.step()

            for metric in metrics:
                metric.update(torch.argmax(logits, dim=1), labels)
        
        training_epochs["Train Loss"][edx] = cum_loss/len(train_loader.dataset.df)
        for metric in metrics:
            training_epochs["Train " + metric._get_name()][edx] = metric.compute().detach().cpu().numpy().item()

        # Validation loop
        if val_loader is not None:
            with torch.no_grad():
                cum_loss = 0
                metrics = [metric.reset() for metric in metrics]
                for bdx, batch in enumerate(val_loader):
                    inputs = model.tokenize(batch["Query"])
                    inputs = {key: value.to(device) for key, value in inputs.items()}
                    labels = batch["Label"].to(device)

                    logits = model_with_head(inputs)

                    loss = loss_function(logits, labels)
                    cum_loss += loss.item()

                    for metric in metrics:
                        metric.update(torch.argmax(logits, dim=1), labels)
            
            training_epochs["Val Loss"][edx] = cum_loss/len(train_loader.dataset.df)
            for metric in metrics:
                training_epochs["Val " + metric._get_name()][edx] = metric.compute().detach().cpu().numpy().item()

        print(", ".join([f"{key} = {value[edx]:.2f}" for key, value in training_epochs.items()]))

        # Check for early stopping
        if earlystopping is not None:
            current_value = training_epochs[earlystopping["metric"]][edx]
            if edx == 0:
                best_metric = current_value
            else:
                if (earlystopping["lower_is_better"] and current_value < best_metric) or (current_value > best_metric):
                    best_metric = current_value
                    best_epoch = edx
                    torch.save(model.state_dict(), "./model_weights.pth")
                
                if edx - best_epoch >= earlystopping["n_epochs"]:
                    print(f"Early stopping initiated. Loading best model weights from epoch={best_epoch}, {earlystopping["metric"]}={best_metric:.2f}.")
                    model.load_state_dict(torch.load("./model_weights.pth"))


    print("Training finished.")


if __name__ == "__main__":
    num_classes = 9
    batch_size = 64

    # Hyperparameters
    hp_grid = {
        "base_model": ["all-MiniLM-L6-v2"],
        "freeze": ["base transformer"],
        "n_epochs": [20],
        "lr": [0.01, 0.005, 0.001],
    }



    # Script start

    hp_names = hp_grid.keys()
    param_combos = list(itertools.product(*hp_grid.values()))

    # Reproducibility
    torch.manual_seed(0)
    np.random.seed(0)
    random.seed(0)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device {device}.")

    # DataLoaders
    train_loader, val_loader, test_loader = create_loaders(batch_size=batch_size)
    loaders = {
        "train_loader": train_loader,
        "val_loader": val_loader,
        "test_loader": test_loader,
    }

    # Metrics
    metrics = create_metrics(num_classes, device=device)

    mlflow.set_experiment("Intent Classifier Hyperparameter Tuning")
    for params in param_combos: # hyperparameter loop
        hp = {key: params[idx] for idx, key in enumerate(hp_names)}
        run_name = ", ".join([f"{key}={value}" for key, value in hp.items()])

        with mlflow.start_run(run_name=run_name):
            print(f"Training run: {run_name}")

            # Log hyperparameters
            mlflow.log_params(hp)

            # Create new model instances
            model, head, model_with_head = create_model(device=device)

            # 

            print("---------------------------------")