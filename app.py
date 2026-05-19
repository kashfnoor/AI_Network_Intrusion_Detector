"""Main Streamlit UI for the modular AI Network Intrusion Detection System.

This file intentionally contains mostly interface code.
The ML logic, preprocessing, experiments, prediction helpers, charts, CSS,
and constants are separated into different files so the project is easier to
understand and modify.

Run:
    streamlit run app.py
"""

import joblib           # to sav trained models
import numpy as np      # arrays, math
import pandas as pd     # tables, dataframes
import plotly.express as px     # for graphs and shi
import streamlit as st      # buttons, sidebars, tables, charts, the app ui
from sklearn.metrics import confusion_matrix    

from config import (
    BASE_PROFILES,
    DATASET_FILE,
    FEATURE_GROUPS,
    IMPORTANT_FEATURES,
    KNN_K_VALUE,
    MLP_HIDDEN_LAYERS,
    SAMPLE_FILE,
)
from data_processing import DatasetManager      # dataset load and preprocess
from experiments import run_architecture_experiments        
from model_training import IDSModelTrainer, model_metric_dataframe  # training and metrics
from prediction_utils import make_demo_record, risk_explanation    # live predicting
from styles import apply_custom_css     # styling
from ui_components import (
    glass_note,
    kpi_card,
    prediction_card,
    render_hero,
    section_bar,
    show_feature_legend,
    simple_model_explanations,
)
from visualization import (         # graphs and charts
    dark_plotly_layout,
    make_pca_cluster_data,
    plot_class_distribution,
    plot_confidence,
    plot_mlp_loss,
    plot_model_accuracy,
    plot_pca_clusters,
)

# -----------------------------------------------------------------------------
# Streamlit page setup
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI IDS Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_custom_css()      # css styling apply (dark cyber themed)


# Streamlit reruns the script after every interaction. Caching prevents expensive
# loading/training work from repeating unnecessarily.
@st.cache_data
def cached_load_data():
    """Load dataset once and reuse it across Streamlit reruns."""
    return DatasetManager().load_data()


@st.cache_resource
def cached_train(df):
    """Train models once and reuse trained pipelines across reruns."""
    manager = DatasetManager()
    clean_df, X, y, numeric_cols, categorical_cols, target_col = manager.preprocess_for_training(df)
    results = IDSModelTrainer(numeric_cols, categorical_cols).train_models(X, y)
    return clean_df, X, y, numeric_cols, categorical_cols, target_col, results


@st.cache_resource
def cached_architecture_experiments(df):
    """Run model variation experiments and cache the result table."""
    return run_architecture_experiments(df)


# -----------------------------------------------------------------------------
# Data loading and model training
# -----------------------------------------------------------------------------
df, source_file = cached_load_data()
try:
    clean_df, X, y, numeric_cols, categorical_cols, target_col, results = cached_train(df)
    training_error = None
except Exception as e:
    training_error = str(e)

metric_df = model_metric_dataframe(results) if not training_error else pd.DataFrame()           # model metrics table
best_model = metric_df.sort_values("F1-score", ascending=False).iloc[0] if not metric_df.empty else None  # model with highest f1 score

# -----------------------------------------------------------------------------
# Sidebar navigation
# -----------------------------------------------------------------------------
st.sidebar.title("🛡️ AI Intrusion Detection System")
st.sidebar.caption("013-052")
st.sidebar.markdown(f"""
<span class="pill">MLP {MLP_HIDDEN_LAYERS}</span>
<span class="pill">KNN k={KNN_K_VALUE}</span>
<span class="pill">Naive Bayes</span>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Live Detection", "Model Analytics", "Model Experiments", "PCA & Clustering", "Dataset Explorer", "Instructions"],
)

# -----------------------------------------------------------------------------
# Page 1: Dashboard overview
# -----------------------------------------------------------------------------
if page == "Dashboard":
    render_hero()           # project intro section

    attack_count = int((y.astype(str).str.lower() != "normal").sum()) if not training_error else 0
    normal_count = int((y.astype(str).str.lower() == "normal").sum()) if not training_error else 0      #attack v normal labels count

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Total Records", f"{len(df):,}", f"Loaded from {source_file}", "📦")
    with c2:
        kpi_card("Attack Records", f"{attack_count:,}", "Suspicious / non-normal traffic", "🚨")
    with c3:
        kpi_card("Normal Records", f"{normal_count:,}", "Safe traffic examples", "✅")
    with c4:
        value = f"{best_model['F1-score']:.2f}%" if best_model is not None else "N/A"
        note = f"Best model: {best_model['Model']}" if best_model is not None else "Training not available"
        kpi_card("Best F1-score", value, note, "🏆")

    left, right = st.columns([1.15, 1])
    with left:
        section_bar("Traffic Class Distribution")
        if training_error:
            st.error(training_error)
        else:
            st.plotly_chart(plot_class_distribution(y), use_container_width=True)
    with right:
        section_bar("Project Intelligence Layer")
        glass_note("Supervised Detection", "MLP, KNN, and Naive Bayes learn from labeled normal/attack examples.")
        glass_note("Visual Analytics", "PCA and K-Means turn many network features into visible traffic groups.")

    section_bar("Model Snapshot")
    if training_error:
        st.error(training_error)
    else:
        st.dataframe(metric_df, use_container_width=True, hide_index=True)  
        st.plotly_chart(plot_model_accuracy(metric_df), use_container_width=True)

    if source_file == SAMPLE_FILE:
        st.warning(f"You are using {SAMPLE_FILE}. Put {DATASET_FILE} in project folder for the real project dataset.")

# -----------------------------------------------------------------------------
# Page 2: Live detection demo
# -----------------------------------------------------------------------------
elif page == "Live Detection":
    st.title("📡 Live Intrusion Detection")
    if training_error:
        st.error(training_error)
        st.stop()

    left, right = st.columns([0.95, 1.05])
    with left:
        section_bar("Detection Controls")
        selected_model_name = st.selectbox("Choose AI model", list(results.keys()))     # choose bw mlp, knn and nb for prediction
        profile = st.selectbox("Traffic scenario", list(BASE_PROFILES.keys()))      # normal, dos, probe etc
        randomize = st.checkbox("Randomize values every test", value=True)
        strength = st.slider("Random variation strength", 0.0, 2.0, 1.0, 0.1)
        seed_mode = st.radio("Random mode", ["New random values", "Fixed seed"], horizontal=True)
        seed = None
        if seed_mode == "Fixed seed":
            seed = st.number_input("Seed value", min_value=0, max_value=999999, value=42, step=1)
        if st.button("Auto-fill / Refresh Traffic"):
            st.session_state["demo_input"] = make_demo_record(profile, X, numeric_cols, randomize=randomize, seed=seed, strength=strength)
        if "demo_input" not in st.session_state:
            st.session_state["demo_input"] = make_demo_record(profile, X, numeric_cols, randomize=randomize, seed=seed, strength=strength)
        # creating input row for checking

    input_df = st.session_state["demo_input"].copy()            

    with right:
        section_bar("Input Feature Guide")
        show_feature_legend([c for group in FEATURE_GROUPS.values() for c in group])

    section_bar("Adjust Important Traffic Values")
    edited_values = {}
    for group, cols in FEATURE_GROUPS.items():
        existing_cols = [c for c in cols if c in input_df.columns]
        if not existing_cols:
            continue
        with st.expander(group, expanded=(group in ["Basic connection info", "Traffic volume", "Error rates"])):
            group_cols = st.columns(3)
            for idx, col in enumerate(existing_cols):
                current = input_df.loc[0, col]
                with group_cols[idx % 3]:
                    help_text = IMPORTANT_FEATURES.get(col, "Network feature")
                    if col in categorical_cols:
                        options = sorted(X[col].astype(str).unique().tolist())[:80]
                        if str(current) not in options:
                            options.insert(0, str(current))
                        edited_values[col] = st.selectbox(col, options, index=options.index(str(current)), help=help_text)
                    elif col in ["serror_rate", "srv_serror_rate", "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate", "dst_host_same_srv_rate", "dst_host_diff_srv_rate"]:
                        edited_values[col] = st.slider(col, 0.0, 1.0, float(np.clip(current, 0, 1)), 0.01, help=help_text)
                    elif col in ["logged_in", "num_failed_logins"]:
                        edited_values[col] = st.number_input(col, min_value=0, value=int(round(float(current))), step=1, help=help_text)
                    else:
                        edited_values[col] = st.number_input(col, min_value=0.0, value=float(current), step=1.0, help=help_text)

    for col, val in edited_values.items():
        input_df.loc[0, col] = val

    with st.expander("Show complete technical row sent to model"):
        st.dataframe(input_df, use_container_width=True)

    if st.button("Run AI Detection", type="primary"):
        model = results[selected_model_name]["pipeline"]
        pred = model.predict(input_df)[0]
        prediction_card(pred, selected_model_name)

        if hasattr(model.named_steps["model"], "predict_proba"):
            probs = model.predict_proba(input_df)[0]
            classes = model.named_steps["model"].classes_
            prob_df = pd.DataFrame({"Class": classes, "Probability (%)": probs * 100})
            st.plotly_chart(plot_confidence(prob_df), use_container_width=True)

        section_bar("Why the result makes sense")
        for line in risk_explanation(input_df):
            st.write(f"• {line}")

# -----------------------------------------------------------------------------
# Page 3: Model analytics
# -----------------------------------------------------------------------------
elif page == "Model Analytics":
    st.title("🤖 Model Analytics")
    if training_error:
        st.error(training_error)
        st.stop()

    section_bar("Performance Comparison")
    st.dataframe(metric_df, use_container_width=True, hide_index=True)
    st.plotly_chart(plot_model_accuracy(metric_df), use_container_width=True)

    section_bar("MLP Loss vs Epoch")
    loss_fig = plot_mlp_loss(results)
    if loss_fig:
        st.plotly_chart(loss_fig, use_container_width=True)
        mlp = results["MLP Neural Network"]["pipeline"].named_steps["model"]
        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Training Iterations", mlp.n_iter_)
        c2.metric("Hidden Layers", ",".join(map(str, MLP_HIDDEN_LAYERS)))
        c3.metric("Activation", mlp.activation)

        train_acc = results["MLP Neural Network"]["train_accuracy"] * 100
        test_acc = results["MLP Neural Network"]["test_accuracy"] * 100

        c4.metric("Generalization Gap", f"{abs(train_acc - test_acc):.2f}%")
        st.info("A decreasing loss means the neural network is learning from the dataset.")

    section_bar("Confusion Matrix")
    cm_model_name = st.selectbox("Choose model", list(results.keys()))
    labels = sorted(y.unique())
    cm = confusion_matrix(results[cm_model_name]["y_test"], results[cm_model_name]["predictions"], labels=labels)
    cm_df = pd.DataFrame(cm, index=labels, columns=labels)
    fig = px.imshow(cm_df, text_auto=True, title=f"Confusion Matrix - {cm_model_name}")
    st.plotly_chart(dark_plotly_layout(fig), use_container_width=True)
    st.caption("Rows are actual classes. Columns are predicted classes. Diagonal values are correct predictions.")

    section_bar("Models in Simple Words")
    st.dataframe(simple_model_explanations(), use_container_width=True, hide_index=True)

    try:
        mlp_pipe = results["MLP Neural Network"]["pipeline"]
        joblib.dump(mlp_pipe.named_steps["model"], "ids_mlp_model.pkl")
        joblib.dump(mlp_pipe.named_steps["preprocess"], "ids_preprocessor.pkl")
        joblib.dump(list(X.columns), "ids_feature_columns.pkl")
        st.success("Saved MLP model, preprocessor, and feature column list.")
    except Exception as e:
        st.warning(f"Models trained, but saving failed: {e}")

# -----------------------------------------------------------------------------
# Page 4: Model experiments
# -----------------------------------------------------------------------------
elif page == "Model Experiments":
    st.title("🧪 Model Architecture Experiments")
    if training_error:
        st.error(training_error)
        st.stop()

    section_bar("Controlled changes to MLP and KNN")
    st.markdown("""
    This page retrains model variations using the same train/test split.
    That makes the comparison fair because the dataset remains the same and only the model setting changes.
    """)

    with st.spinner("Training experiment models and calculating comparison table..."):
        exp_df = cached_architecture_experiments(df)

    main_cols = ["Family", "Variation", "Changed setting", "Accuracy", "Precision", "Recall", "F1-score", "Δ Accuracy", "Δ Precision", "Δ Recall", "Δ F1-score"]
    cm_cols = [c for c in ["TN", "FP", "FN", "TP"] if c in exp_df.columns]
    st.dataframe(exp_df[main_cols + cm_cols], use_container_width=True, hide_index=True)

    st.download_button(
        "Download experiment comparison as CSV",
        exp_df.to_csv(index=False).encode("utf-8"),
        file_name="model_architecture_experiment_results.csv",
        mime="text/csv",
    )

    section_bar("Visual comparison")
    metric_choice = st.selectbox("Choose metric to compare", ["Accuracy", "Precision", "Recall", "F1-score"])
    fig = px.bar(exp_df, x="Variation", y=metric_choice, color="Family", text=metric_choice, title=f"Experiment Comparison by {metric_choice}")
    fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    fig.update_yaxes(range=[0, 105])
    st.plotly_chart(dark_plotly_layout(fig), use_container_width=True)

    section_bar("How to interpret the changes")
    st.markdown("""
    **Deeper MLP:** uses more hidden layers, so it has more learning capacity. If performance improves, the extra depth helped. If it drops, the model may be harder to train or unnecessarily complex.

    **Smaller MLP:** uses fewer neurons/layers, so it trains faster and is simpler. If recall drops, the smaller model is missing more attacks.

    **KNN k = 3:** more sensitive to nearby records. It may catch local attack patterns better, but can also be noisier.

    **KNN k = 9:** smoother and more conservative. False positives may reduce, but recall can fall if real attacks are surrounded by normal records.

    **For IDS, recall matters heavily** because a false negative means an actual attack was classified as normal.
    """)

# -----------------------------------------------------------------------------
# Page 5: PCA and clustering
# -----------------------------------------------------------------------------
elif page == "PCA & Clustering":
    st.title("📊 PCA & Clustering Analysis")
    if training_error:
        st.error(training_error)
        st.stop()

    k = st.slider("Choose number of clusters (k)", 2, 8, 3)
    pca_df, clusters, pca = make_pca_cluster_data(X, y, numeric_cols, k)

    section_bar("Interactive PCA Cluster Graph")
    st.plotly_chart(plot_pca_clusters(pca_df), use_container_width=True)

    explained = pca.explained_variance_ratio_ * 100                     # how much info retained
    c1, c2, c3 = st.columns(3)
    c1.metric("PCA Component 1", f"{explained[0]:.2f}%")
    c2.metric("PCA Component 2", f"{explained[1]:.2f}%")
    c3.metric("Clusters", k)

    st.info("PCA combines many numeric features into two new directions so traffic can be visualized in 2D.")

    section_bar("Cluster Contents")
    cluster_summary = pd.crosstab(pca_df["Cluster"], pca_df["Actual label"])            # which label appears in which cluster
    st.dataframe(cluster_summary, use_container_width=True)

    section_bar("Cluster Size Chart")
    cluster_counts = pca_df["Cluster"].value_counts().sort_index().reset_index()
    cluster_counts.columns = ["Cluster", "Records"]
    fig = px.bar(cluster_counts, x="Cluster", y="Records", text="Records", title="Records per Cluster")
    st.plotly_chart(dark_plotly_layout(fig), use_container_width=True)

# -----------------------------------------------------------------------------
# Page 6: Dataset explorer
# -----------------------------------------------------------------------------
elif page == "Dataset Explorer":
    st.title("📁 Dataset Explorer")
    st.write(f"Current file: `{source_file}`")

    c1, c2, c3 = st.columns(3)
    c1.metric("Rows", df.shape[0])
    c2.metric("Columns", df.shape[1])
    c3.metric("Target Column", target_col if not training_error else "Not available")

    section_bar("Dataset Preview")
    st.dataframe(df.head(100), use_container_width=True)

    section_bar("Important Feature Legend")
    show_feature_legend([c for c in IMPORTANT_FEATURES if c in df.columns])

    section_bar("Zero Value Check")
    st.info("Many zero values are normal in network datasets. For example, most connections do not have failed logins or urgent packets.")
    numeric_df = df.select_dtypes(include=[np.number])
    if not numeric_df.empty:
        zero_summary = ((numeric_df == 0).mean() * 100).sort_values(ascending=False).head(20).reset_index()
        zero_summary.columns = ["Column", "Zero values (%)"]
        st.dataframe(zero_summary, use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------------
# Page 7: Instructions
# -----------------------------------------------------------------------------
elif page == "Instructions":
    st.title("🧾 Instructions")
    st.markdown("""
    ### Run this modular dashboard
    ```bash
    pip install -r requirements.txt
    streamlit cache clear
    streamlit run app.py
    ```

    ### Dataset setup
    Keep your final dataset in this same folder with this exact name:
    ```text
    intrusion_dataset.csv
    ```

    ### Modular file guide
    - `app.py` = Streamlit interface only
    - `config.py` = settings like KNN k value and file names
    - `data_processing.py` = dataset loading and preprocessing
    - `model_training.py` = MLP, KNN, Naive Bayes training
    - `experiments.py` = MLP/KNN comparison experiments
    - `prediction_utils.py` = live demo record creation and risk explanation
    - `visualization.py` = Plotly charts, PCA, clustering
    - `ui_components.py` = reusable dashboard cards and UI blocks
    - `styles.py` = custom dark dashboard CSS

    ### Changing KNN k value
    Open `config.py` and change:
    ```python
    KNN_K_VALUE = 3
    ```
    Then run:
    ```bash
    streamlit cache clear
    streamlit run app.py
    ```
    """)
