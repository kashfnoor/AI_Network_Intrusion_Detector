"""Reusable UI components used by the Streamlit dashboard."""

import pandas as pd
import streamlit as st
from config import IMPORTANT_FEATURES


def render_hero():
    """Display the main professional dashboard header."""
    st.markdown("""
    <div class="hero">
        <h1>🛡️ AI Network Intrusion Detection Dashboard</h1>
        <p>Professional AI-powered security analytics dashboard for detecting normal and suspicious network traffic using MLP, KNN, Naive Bayes, PCA, and K-Means clustering.</p>
        <span class="pill">MLP Neural Network</span>
        <span class="pill">KNN</span>
        <span class="pill">Naive Bayes</span>
        <span class="pill">PCA</span>
        <span class="pill">K-Means</span>
    </div>
    """, unsafe_allow_html=True)


def kpi_card(title, value, note, icon="🔹"):
    """Display a custom KPI card."""
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">{icon} {title}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)


def section_bar(title):
    """Display a reusable section heading."""
    st.markdown(f'<div class="section-bar">{title}</div>', unsafe_allow_html=True)


def glass_note(title, body):
    """Display a short explanation card."""
    st.markdown(f"""
    <div class="glass-card">
        <h4>{title}</h4>
        <p>{body}</p>
    </div>
    """, unsafe_allow_html=True)


def prediction_card(prediction, model_name):
    """Show a large professional result card after prediction."""
    if str(prediction).lower() == "normal":
        css_class = "normal-card"
        title = "✅ NORMAL TRAFFIC"
        body = "The selected model thinks this traffic looks safe based on the learned network patterns."
    else:
        css_class = "attack-card"
        title = "🚨 ATTACK / INTRUSION DETECTED"
        body = "The selected model thinks this traffic is suspicious and may represent an intrusion attempt."
    st.markdown(f"""
    <div class="{css_class}">
        <h2>{title}</h2>
        <p>Model used: <b>{model_name}</b></p>
        <p>{body}</p>
    </div>
    """, unsafe_allow_html=True)


def simple_model_explanations():
    """Return a student-friendly model explanation table."""
    return pd.DataFrame([
        {"Model": "MLP Neural Network", "Simple explanation": "Learns hidden attack patterns from previous examples.", "Why it is useful": "Best for complex network behavior."},
        {"Model": "KNN", "Simple explanation": "Compares new traffic with similar old traffic records.", "Why it is useful": "Easy to explain and good for comparison."},
        {"Model": "Naive Bayes", "Simple explanation": "Uses probability to guess the most likely class.", "Why it is useful": "Fast baseline model."},
        {"Model": "K-Means", "Simple explanation": "Groups similar traffic records without using labels.", "Why it is useful": "Shows natural traffic clusters."},
        {"Model": "PCA", "Simple explanation": "Compresses many columns into two visual axes.", "Why it is useful": "Makes high-dimensional traffic data visible."},
    ])


def show_feature_legend(columns=None):
    """Show a table explaining important input features."""
    legend_items = []
    source = columns if columns is not None else IMPORTANT_FEATURES.keys()
    for col in source:
        if col in IMPORTANT_FEATURES:
            legend_items.append({"Feature": col, "Meaning": IMPORTANT_FEATURES[col]})
    st.dataframe(pd.DataFrame(legend_items), use_container_width=True, hide_index=True)
