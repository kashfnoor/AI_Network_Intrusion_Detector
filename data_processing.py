"""Dataset loading and preprocessing utilities."""

from pathlib import Path
import numpy as np
import pandas as pd
from config import DATASET_FILE, SAMPLE_FILE

class DatasetManager:
    """Handles loading, target-column detection, and preprocessing."""

    def load_data(self):
        """Load the real dataset if available, otherwise load the sample dataset."""
        if Path(DATASET_FILE).exists():
            return pd.read_csv(DATASET_FILE), DATASET_FILE
        return pd.read_csv(SAMPLE_FILE), SAMPLE_FILE

    def get_target_column(self, df):
        """Find the output/label column even if the dataset version uses a different name."""
        if "label" in df.columns:
            return "label"
        if "binary_label" in df.columns:
            return "binary_label"
        if "attack_type" in df.columns:
            return "attack_type"
        return df.columns[-1]       # if no label match, return last column

    def preprocess_for_training(self, df):
        """Clean the dataset and split it into features X and target y."""
        df = df.copy().replace([np.inf, -np.inf], np.nan).dropna()      # remove null and infinte values
        target_col = self.get_target_column(df)     

        if target_col == "attack_type":                 # if detailed attack types, binarize as normal or attack
            df["label"] = df["attack_type"].apply(
                lambda x: "normal" if str(x).strip().lower() == "normal" else "attack"
            )
            target_col = "label"        # target column label 

        drop_cols = [target_col]
        for col in ["attack_type", "attack_category", "difficulty"]:        # remove columns so model doesnt just learn the result
            if col in df.columns and col != target_col:
                drop_cols.append(col)

        X = df.drop(columns=drop_cols, errors="ignore")         # drop answer columns or missing columns
        y = df[target_col].astype(str)              # convert labels to string

        categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()  # detect categorical columns for onehotencoding
        numeric_cols = X.select_dtypes(exclude=["object"]).columns.tolist()    # detect numeric columns for scaling
        return df, X, y, numeric_cols, categorical_cols, target_col
