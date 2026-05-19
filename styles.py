"""Custom CSS for the professional Streamlit dashboard."""

import streamlit as st


def apply_custom_css():
    """Apply custom dark cybersecurity dashboard CSS."""
    st.markdown("""
<style>
    .stApp {background: radial-gradient(circle at top left, #13213a 0%, #0b1220 38%, #050816 100%); color: #e5e7eb;}
    .main .block-container {padding-top: 1.4rem; padding-bottom: 2rem; max-width: 1500px;}
    section[data-testid="stSidebar"] {background: linear-gradient(180deg, #07111f 0%, #0f172a 100%); border-right: 1px solid #1f2937;}
    h1, h2, h3, h4, h5, h6, p, label, span, div {color: #e5e7eb;}
    .hero {padding: 26px 30px; border-radius: 24px; background: linear-gradient(135deg, rgba(37,99,235,0.92), rgba(14,165,233,0.72), rgba(15,23,42,0.95)); border: 1px solid rgba(147,197,253,0.32); box-shadow: 0 20px 60px rgba(37,99,235,0.18); margin-bottom: 18px;}
    .hero h1 {font-size: 2.35rem; margin-bottom: 0.25rem; color: white !important;}
    .hero p {color: #dbeafe !important; font-size: 1.04rem; line-height: 1.55; max-width: 950px;}
    .glass-card {background: rgba(15, 23, 42, 0.72); border: 1px solid rgba(148, 163, 184, 0.18); border-radius: 22px; padding: 20px; box-shadow: 0 18px 45px rgba(0,0,0,0.24); min-height: 118px;}
    .glass-card h3, .glass-card h4, .glass-card p {color: #e5e7eb !important;}
    .kpi-card {background: linear-gradient(180deg, rgba(17,24,39,0.95), rgba(15,23,42,0.92)); border: 1px solid rgba(59,130,246,0.30); border-radius: 20px; padding: 18px; box-shadow: 0 12px 35px rgba(0,0,0,0.26); min-height: 128px;}
    .kpi-title {color: #94a3b8 !important; font-size: 0.88rem; margin-bottom: 8px;}
    .kpi-value {color: #ffffff !important; font-size: 1.75rem; font-weight: 800; margin-bottom: 6px;}
    .kpi-note {color: #93c5fd !important; font-size: 0.83rem;}
    .section-bar {padding: 12px 16px; margin: 8px 0 14px 0; border-radius: 14px; background: rgba(30, 41, 59, 0.82); border-left: 5px solid #38bdf8; color: #e0f2fe !important; font-weight: 800;}
    .pill {display: inline-block; padding: 6px 11px; border-radius: 999px; background: rgba(59,130,246,0.18); border: 1px solid rgba(59,130,246,0.35); color: #bfdbfe !important; font-size: 0.82rem; font-weight: 700; margin-right: 6px; margin-bottom: 6px;}
    .danger-pill {background: rgba(239,68,68,0.16); border-color: rgba(239,68,68,0.38); color: #fecaca !important;}
    .safe-pill {background: rgba(34,197,94,0.15); border-color: rgba(34,197,94,0.38); color: #bbf7d0 !important;}
    .attack-card {padding: 24px; border-radius: 22px; background: linear-gradient(135deg, rgba(127,29,29,0.95), rgba(239,68,68,0.78)); border: 1px solid rgba(252,165,165,0.45); box-shadow: 0 18px 45px rgba(239,68,68,0.18);}
    .normal-card {padding: 24px; border-radius: 22px; background: linear-gradient(135deg, rgba(20,83,45,0.95), rgba(34,197,94,0.72)); border: 1px solid rgba(134,239,172,0.45); box-shadow: 0 18px 45px rgba(34,197,94,0.16);}
    .attack-card h2, .attack-card p, .normal-card h2, .normal-card p {color: white !important;}
    div[data-testid="stDataFrame"] {border-radius: 16px; overflow: hidden;}
    .stButton > button {border-radius: 14px; padding: 0.65rem 1.1rem; font-weight: 800; border: 1px solid rgba(59,130,246,0.5); background: linear-gradient(135deg, #2563eb, #06b6d4); color: white;}
</style>
""", unsafe_allow_html=True)
