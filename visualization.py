"""Plotly chart functions for the professional dashboard."""

import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


def dark_plotly_layout(fig, title=None):
    """ 
    Apply a consistent professional dark theme to Plotly charts.

    Important fix:
    Earlier, this function always ran `title=title`.
    When no title was passed, `title` became None, and Plotly could show
    the word "undefined" above charts.

    Now the function only changes the chart title when a real title is given.
    If the chart already has a title from px.bar(), px.line(), px.pie(), etc.,
    that original title is preserved.
    """
    layout_settings = dict(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.55)",         # transparent bg for charts
        font=dict(color="#e5e7eb"),
        margin=dict(l=35, r=25, t=55, b=35),        # chart spacing
        height=390,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),       # legend position
    )

    # Only set a new title if a valid title is provided.
    # This prevents "undefined" from appearing on charts.
    if title is not None and str(title).strip() != "":
        layout_settings["title_text"] = str(title)

    fig.update_layout(**layout_settings)
    return fig


def plot_model_accuracy(metric_df):
    """Interactive model comparison chart."""
    fig = px.bar(metric_df, x="Model", y="Accuracy", text="Accuracy", title="Model Accuracy Comparison", color="Model")
    fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")      # format labels
    fig.update_yaxes(range=[0, 105], title="Accuracy (%)")
    return dark_plotly_layout(fig)


def plot_mlp_loss(results):
    """Plot MLP loss against training epoch/iteration."""
    mlp = results["MLP Neural Network"]["pipeline"].named_steps["model"]  # get trained model
    loss_curve = getattr(mlp, "loss_curve_", [])        # get loss history
    if len(loss_curve) == 0:
        return None
    loss_df = pd.DataFrame({"Epoch": list(range(1, len(loss_curve) + 1)), "Loss": loss_curve})      # table for plotting
    fig = px.line(loss_df, x="Epoch", y="Loss", markers=True, title="MLP Loss vs Epoch")
    fig.update_traces(line=dict(width=3), marker=dict(size=5))
    fig.update_yaxes(title="Training Loss")
    fig.update_xaxes(title="Epoch / Iteration")
    return dark_plotly_layout(fig)


def plot_class_distribution(y):
    """Plot normal vs attack class distribution."""
    counts = y.value_counts().reset_index()
    counts.columns = ["Class", "Records"]
    fig = px.pie(counts, values="Records", names="Class", hole=0.45, title="Traffic Class Distribution")    # pie chart
    fig.update_traces(textinfo="label+percent")         # class name and percentage on chart
    return dark_plotly_layout(fig)


def make_pca_cluster_data(X, y, numeric_cols, k):
    """Create PCA coordinates and K-Means cluster labels."""
    numeric_data = X[numeric_cols].replace([np.inf, -np.inf], np.nan).dropna()      # only numeric columns keep
    scaled = StandardScaler().fit_transform(numeric_data)           # scale
    pca = PCA(n_components=2, random_state=42)
    pca_values = pca.fit_transform(scaled)           # run pca and get 2D values
    clusters = KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(scaled)         # run k means multiple times and select ebest
    pca_df = pd.DataFrame({
        "PCA Component 1": pca_values[:, 0],
        "PCA Component 2": pca_values[:, 1],
        "Cluster": [f"Cluster {c}" for c in clusters],
        "Actual label": y.loc[numeric_data.index].astype(str).values,
    })
    return pca_df, clusters, pca


def plot_pca_clusters(pca_df):
    """Create professional PCA cluster scatter plot."""
    fig = px.scatter(
        pca_df,
        x="PCA Component 1",
        y="PCA Component 2",
        color="Cluster",
        symbol="Actual label",
        hover_data=["Actual label"],
        title="PCA + K-Means Traffic Clusters",
        opacity=0.72,
    )
    fig.update_traces(marker=dict(size=7, line=dict(width=0.3, color="white")))
    return dark_plotly_layout(fig)


def plot_confidence(prob_df):
    """Plot prediction confidence as a horizontal bar chart."""
    fig = px.bar(prob_df, x="Probability (%)", y="Class", orientation="h", text="Probability (%)", title="Prediction Confidence")
    fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    fig.update_xaxes(range=[0, 105])
    return dark_plotly_layout(fig)
