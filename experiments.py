"""Controlled model experiments for viva/presentation comparison."""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

from config import TEST_SIZE, RANDOM_STATE, MLP_HIDDEN_LAYERS
from data_processing import DatasetManager
from model_training import IDSModelTrainer
 

def run_architecture_experiments(df):
    """Train MLP/KNN variations using the same train/test split for fair comparison."""
    manager = DatasetManager()
    _, X_exp, y_exp, numeric_cols_exp, categorical_cols_exp, _ = manager.preprocess_for_training(df)
    trainer = IDSModelTrainer(numeric_cols_exp, categorical_cols_exp)

    stratify = y_exp if y_exp.value_counts().min() >= 2 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X_exp, y_exp, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=stratify
    )

    experiment_models = [
        {"Family": "MLP", "Variation": "Baseline MLP", "Changed setting": "5 hidden layers: 64 → 32 → 16 → 8 → 4", "Model": MLPClassifier(hidden_layer_sizes= MLP_HIDDEN_LAYERS, activation="relu", solver="adam", max_iter=500, random_state=42)},
        {"Family": "MLP", "Variation": "Removed 2 MLP layers", "Changed setting": "3 hidden layers: 32 → 16 → 8", "Model": MLPClassifier(hidden_layer_sizes=(32, 16, 8), activation="relu", solver="adam", max_iter=500, random_state=42)},
        {"Family": "MLP", "Variation": "One MLP layer", "Changed setting": "1 hidden layer: 32", "Model": MLPClassifier(hidden_layer_sizes=(32,), activation="relu", solver="adam", max_iter=500, random_state=42)},
        {"Family": "KNN", "Variation": "KNN k=5", "Changed setting": "k = 5 nearest neighbors", "Model": KNeighborsClassifier(n_neighbors=5)},
        {"Family": "KNN", "Variation": "Baseline KNN k=3", "Changed setting": "k = 3 nearest neighbors", "Model": KNeighborsClassifier(n_neighbors=3)},
        {"Family": "KNN", "Variation": "KNN k=9", "Changed setting": "k = 9 nearest neighbors", "Model": KNeighborsClassifier(n_neighbors=9)},
    ]

    labels_sorted = sorted(y_exp.unique())          # get unique labels and sort
    binary_labels = None
    if len(labels_sorted) == 2:
        normal_candidates = [lbl for lbl in labels_sorted if str(lbl).lower() == "normal"]
        if normal_candidates:
            normal_label = normal_candidates[0]
            attack_label = [lbl for lbl in labels_sorted if lbl != normal_label][0]
            binary_labels = [normal_label, attack_label]

    rows = []           # each models result stored as one row
    for item in experiment_models:
        pipe = Pipeline([
            ("preprocess", trainer.build_preprocessor()),
            ("model", item["Model"]),
        ])
        pipe.fit(X_train, y_train)
        preds = pipe.predict(X_test)

        row = {
            "Family": item["Family"],           # which model
            "Variation": item["Variation"],     # k=3, layers etc
            "Changed setting": item["Changed setting"],
            "Accuracy": round(accuracy_score(y_test, preds) * 100, 2),
            "Precision": round(precision_score(y_test, preds, average="weighted", zero_division=0) * 100, 2),
            "Recall": round(recall_score(y_test, preds, average="weighted", zero_division=0) * 100, 2),
            "F1-score": round(f1_score(y_test, preds, average="weighted", zero_division=0) * 100, 2),
        }

        if binary_labels:           # only run if two labels
            cm = confusion_matrix(y_test, preds, labels=binary_labels)
            tn, fp, fn, tp = cm.ravel()
            row.update({"TN": int(tn), "FP": int(fp), "FN": int(fn), "TP": int(tp)})

        rows.append(row)

    exp_df = pd.DataFrame(rows)             # rows into table
    for family in exp_df["Family"].unique():        # loops through each model
        family_mask = exp_df["Family"] == family
        if family == "MLP":
            baseline_row = exp_df[family_mask & (exp_df["Variation"] == "Baseline MLP")].iloc[0]
        else:
            baseline_row = exp_df[family_mask & (exp_df["Variation"] == "KNN k=5")].iloc[0]
        for metric in ["Accuracy", "Precision", "Recall", "F1-score"]:
            exp_df.loc[family_mask, f"Δ {metric}"] = (exp_df.loc[family_mask, metric] - baseline_row[metric]).round(2)

    return exp_df
