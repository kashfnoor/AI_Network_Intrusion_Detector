"""Model training logic for MLP, KNN, and Naive Bayes."""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from config import (
    MLP_HIDDEN_LAYERS,
    MLP_MAX_ITER,
    MLP_RANDOM_STATE,
    KNN_K_VALUE,
    TEST_SIZE,
    RANDOM_STATE,
)

class IDSModelTrainer:
    """Builds preprocessing pipelines and trains IDS models."""

    def __init__(self, numeric_cols, categorical_cols):
        self.numeric_cols = numeric_cols
        self.categorical_cols = categorical_cols

    def build_preprocessor(self):       # preprocessing
        """Scale numeric values and one-hot encode categorical values."""
        return ColumnTransformer(
            transformers=[
                ("num", StandardScaler(), self.numeric_cols),      # scaling numeric values 
                ("cat", OneHotEncoder(handle_unknown="ignore"), self.categorical_cols),  # ignore unknowns
            ]    # scaling categories (010, 100, 001)
        )

    def train_models(self, X, y):    # x is input features, y is labels
        """Train all supervised models and return their metrics and pipelines."""
        models = {
            "MLP Neural Network": MLPClassifier(
                hidden_layer_sizes=MLP_HIDDEN_LAYERS,   # 2 layers (32,16)
                activation="relu",      # for non linear patterns max(0, x)
                solver="adam",          # auto model tuning
                max_iter=MLP_MAX_ITER,  # 500 i believe check config
                random_state=MLP_RANDOM_STATE,
            ),
            f"KNN (k={KNN_K_VALUE})": KNeighborsClassifier(n_neighbors=KNN_K_VALUE),  # 3
            "Naive Bayes": BernoulliNB(),
        }
        
        # balance attack:normal for training and testing 
        stratify = y if y.value_counts().min() >= 2 else None   # each class has 2 samples min
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=stratify
        )

        results = {}
        for name, model in models.items():

            if name == "Naive Bayes":
                preprocessor = ColumnTransformer(
                transformers=[
                    ("num", StandardScaler(), self.numeric_cols),
                    ("cat", OneHotEncoder(handle_unknown="ignore"), self.categorical_cols),
                ]
                )
            else: 
                preprocessor = self.build_preprocessor()   

            pipe = Pipeline([
            ("preprocess", preprocessor),
            ("model", model),
            ])

       

            pipe.fit(X_train, y_train)

            train_preds = pipe.predict(X_train)
            test_preds = pipe.predict(X_test)

            results[name] = {
                "pipeline": pipe,

                "train_accuracy": accuracy_score(y_train, train_preds),
                "test_accuracy": accuracy_score(y_test, test_preds),

                "accuracy": accuracy_score(y_test, test_preds),
                "precision": precision_score(y_test, test_preds, average="weighted", zero_division=0),
                "recall": recall_score(y_test, test_preds, average="weighted", zero_division=0),
                "f1": f1_score(y_test, test_preds, average="weighted", zero_division=0),

                "predictions": test_preds,
                "y_test": y_test,
            }
        return results


def model_metric_dataframe(results):
    """Convert result dictionary into a clean metrics table for the dashboard."""
    return pd.DataFrame([
        {
            "Model": name,
            "Train Accuracy": round(info["train_accuracy"] * 100, 2),
            "Test Accuracy": round(info["test_accuracy"] * 100, 2),
            "Accuracy": round(info["accuracy"] * 100, 2),
            "Precision": round(info["precision"] * 100, 2),
            "Recall": round(info["recall"] * 100, 2),
            "F1-score": round(info["f1"] * 100, 2),
        }
        for name, info in results.items()
    ])
