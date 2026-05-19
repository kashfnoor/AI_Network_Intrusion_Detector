"""Live demo record creation and prediction explanation utilities."""

import numpy as np
import pandas as pd
from config import BASE_PROFILES


def randomize_value(value, col, rng, strength):
    """Add controlled randomness to live-demo values."""
    if isinstance(value, str):
        return value
    try:
        value = float(value)
    except Exception:
        return value

    rate_cols = ["serror_rate", "srv_serror_rate", "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate", "dst_host_same_srv_rate", "dst_host_diff_srv_rate"]
    if col in rate_cols:
        return float(np.clip(value + rng.normal(0, 0.08 * strength), 0, 1))
    if col in ["logged_in", "num_failed_logins"]:
        return int(max(0, round(value + rng.integers(-1, 2) * strength)))

    noise = rng.normal(0, max(1, abs(value) * 0.25) * strength)
    return float(max(0, value + noise))


def make_demo_record(profile, X, numeric_cols, randomize=True, seed=None, strength=1.0):
    """Build one complete prediction row from a selected traffic scenario."""
    rng = np.random.default_rng(seed)
    values = BASE_PROFILES[profile].copy()       # base case selected(normal traffic etc)
    if randomize:
        values = {col: randomize_value(val, col, rng, strength) for col, val in values.items()}

    record = {}
    for col in X.columns:
        if col in values:
            record[col] = values[col]       # use already given value
        elif col in numeric_cols:
            record[col] = float(pd.to_numeric(X[col], errors="coerce").median())   #numeric values 
        else:
            record[col] = str(X[col].mode()[0])     # non numeric values
    return pd.DataFrame([record])


def risk_explanation(row):
    """Generate simple human-readable reasons for why traffic may be suspicious."""
    row = row.iloc[0]
    reasons = []
    if row.get("count", 0) > 100:
        reasons.append("High connection count suggests flooding or repeated access.")
    if row.get("serror_rate", 0) > 0.5 or row.get("srv_serror_rate", 0) > 0.5:
        reasons.append("High SYN error rate suggests many failed connection attempts.")
    if row.get("rerror_rate", 0) > 0.5 or row.get("srv_rerror_rate", 0) > 0.5:
        reasons.append("High rejection rate suggests probing or scanning.")
    if row.get("num_failed_logins", 0) > 0:
        reasons.append("Failed login attempts increase suspicious-access risk.")
    if str(row.get("flag", "")).upper() in ["S0", "REJ", "RSTO"]:
        reasons.append("Connection flag indicates rejected or incomplete traffic.")
    if not reasons:
        reasons.append("Values look close to normal traffic: low errors, normal counts, and successful connection behavior.")
    return reasons
