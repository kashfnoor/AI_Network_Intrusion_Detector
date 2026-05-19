# AI_Network_Intrusion_Detector
An interactive AI-powered Network Intrusion Detection System (IDS) developed using Machine Learning, Streamlit, PCA, and clustering techniques for detecting suspicious network traffic and visualizing cybersecurity patterns.

---

## Features

- Interactive Streamlit Dashboard
- Live Intrusion Detection
- Machine Learning-Based Traffic Classification
- PCA Visualization
- K-Means Clustering
- Model Performance Analytics

---

## Machine Learning Models

### Multi-Layer Perceptron (MLP)

Architecture used:

```text
64 → 32 → 16 → 8 → 4
```

- ReLU activation function
- Adam optimizer
- Best overall performance

### K-Nearest Neighbors (KNN)

Tested values:

```text
K = 3
K = 5
K = 9
```

Best result achieved using:

```text
K = 3
```

### Bernoulli Naive Bayes

- Fast probabilistic classifier
- Suitable for One-Hot Encoded features
- Lightweight and computationally efficient

---

## Dataset

Dataset used: **NSL-KDD Dataset**

The dataset contains both normal and malicious network traffic records.

### Attack Categories

- DOS
- Probe
- R2L
- U2R

### Preprocessing Techniques

- Dataset Cleaning
- One-Hot Encoding
- StandardScaler Normalization
- Train-Test Splitting
- Scikit-learn Pipelines

---

## Dashboard Features

The Streamlit dashboard includes:

- Dataset Viewer
- Live Intrusion Prediction
- PCA Cluster Visualization
- Confusion Matrices
- Model Comparison
- Performance Graphs
- Experiment Analysis

---

# Project Structure

```text
├── app.py
├── config.py
├── data_processing.py
├── experiments.py
├── model_training.py
├── prediction_utils.py
├── prepare_dataset.py
├── styles.py
├── ui_components.py
├── visualization.py
├── intrusion_dataset.csv
├── requirements.txt
└── README.md
```

---

# File Descriptions

| File | Purpose |
|---|---|
| `app.py` | Main Streamlit dashboard |
| `config.py` | Project settings and constants |
| `data_processing.py` | Dataset loading and preprocessing |
| `model_training.py` | ML model training pipelines |
| `experiments.py` | Hyperparameter experiments |
| `prediction_utils.py` | Live prediction helpers |
| `visualization.py` | Charts and visualizations |
| `ui_components.py` | Reusable dashboard UI components |
| `styles.py` | Custom dashboard styling |
| `prepare_dataset.py` | NSL-KDD dataset preparation |

---
---

### Key Findings

- MLP achieved the highest overall performance
- KNN produced highly competitive results
- BernoulliNB provided faster lightweight classification

---

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

---

## Technologies Used

- Python
- Streamlit
- Scikit-learn
- Pandas
- NumPy
- Plotly
- Matplotlib

---

