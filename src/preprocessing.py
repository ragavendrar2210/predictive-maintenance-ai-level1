"""
preprocessing.py
----------------
Reusable, beginner-friendly helper functions for Level 1 of the
Predictive Maintenance & Equipment Failure Intelligence System.

Dataset: UCI AI4I 2020 Predictive Maintenance Dataset (ai4i2020.csv).
No machine learning model is trained here - these functions only load,
validate, clean and engineer features.
"""

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Column groups (taken from the real dataset schema)
# ---------------------------------------------------------------------------
ID_COLS = ["UDI", "Product ID"]
CATEGORICAL_COLS = ["Type"]
SENSOR_COLS = [
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]",
]
TARGET_COL = "Machine failure"
# Failure-mode flags describe WHY a machine failed -> post-event information.
FAILURE_MODE_COLS = ["TWF", "HDF", "PWF", "OSF", "RNF"]

EXPECTED_TYPES = {"L", "M", "H"}

# Physically plausible ranges (wide, conservative sanity limits - NOT outlier rules)
PLAUSIBLE_RANGES = {
    "Air temperature [K]": (250, 350),      # roughly -23 C to 77 C
    "Process temperature [K]": (250, 400),
    "Rotational speed [rpm]": (0, 10000),
    "Torque [Nm]": (0, 200),
    "Tool wear [min]": (0, 1000),
}


def load_raw(path):
    """Load the raw AI4I CSV file without modifying it."""
    return pd.read_csv(path)


def check_missing(df):
    """Return the number of missing values per column."""
    return df.isna().sum()


def check_implausible(df, ranges=PLAUSIBLE_RANGES):
    """Count readings outside physically plausible ranges for each sensor."""
    rows = []
    for col, (lo, hi) in ranges.items():
        mask = (df[col] < lo) | (df[col] > hi)
        rows.append({"column": col, "min_allowed": lo, "max_allowed": hi,
                     "n_outside": int(mask.sum())})
    return pd.DataFrame(rows)


def iqr_outlier_counts(df, cols=SENSOR_COLS, k=1.5):
    """Count IQR outliers per column. Used for investigation only - no rows are removed."""
    rows = []
    for col in cols:
        q1, q3 = df[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        lo, hi = q1 - k * iqr, q3 + k * iqr
        mask = (df[col] < lo) | (df[col] > hi)
        rows.append({"column": col, "lower_fence": round(lo, 2), "upper_fence": round(hi, 2),
                     "n_outliers": int(mask.sum()), "pct": round(100 * mask.mean(), 2)})
    return pd.DataFrame(rows)


def clean_data(df):
    """
    Apply only justified cleaning steps. Returns (cleaned_df, log) where log
    is a list of dicts documenting every step and the rows affected.
    """
    log = []
    out = df.copy()

    # 1. Strip whitespace / standardise case in categorical text columns
    for col in ["Product ID", "Type"]:
        before = out[col].copy()
        out[col] = out[col].astype(str).str.strip()
        if col == "Type":
            out[col] = out[col].str.upper()
        log.append({"step": f"Strip/standardise text in '{col}'",
                    "rows_affected": int((before != out[col]).sum())})

    # 2. Remove exact duplicate rows (only if any exist)
    n_dup = int(out.duplicated().sum())
    out = out.drop_duplicates().reset_index(drop=True)
    log.append({"step": "Drop exact duplicate rows", "rows_affected": n_dup})

    # 3. Missing values: dropped only if present (the AI4I file has none)
    n_missing_rows = int(out.isna().any(axis=1).sum())
    out = out.dropna().reset_index(drop=True)
    log.append({"step": "Drop rows with missing values", "rows_affected": n_missing_rows})

    # 4. Remove physically implausible readings (not statistical outliers)
    mask = pd.Series(False, index=out.index)
    for col, (lo, hi) in PLAUSIBLE_RANGES.items():
        mask |= (out[col] < lo) | (out[col] > hi)
    log.append({"step": "Drop physically implausible readings", "rows_affected": int(mask.sum())})
    out = out[~mask].reset_index(drop=True)

    # 5. Make sure 'Type' is an ordered category L < M < H (quality variants)
    out["Type"] = pd.Categorical(out["Type"], categories=["L", "M", "H"], ordered=True)
    log.append({"step": "Convert 'Type' to ordered category (L<M<H)", "rows_affected": 0})

    return out, log


def validate_schema(df):
    """Raise an AssertionError if the cleaned data does not look as expected."""
    required = ID_COLS + CATEGORICAL_COLS + SENSOR_COLS + [TARGET_COL] + FAILURE_MODE_COLS
    missing = [c for c in required if c not in df.columns]
    assert not missing, f"Missing columns: {missing}"
    assert df.isna().sum().sum() == 0, "Missing values found"
    assert set(df["Type"].astype(str).unique()) <= EXPECTED_TYPES, "Unexpected Type values"
    assert set(df[TARGET_COL].unique()) <= {0, 1}, "Target must be binary"
    for c in FAILURE_MODE_COLS:
        assert set(df[c].unique()) <= {0, 1}, f"{c} must be binary"
    assert df["UDI"].is_unique, "UDI must be unique"
    return True


def add_engineered_features(df):
    """
    Add Level-1 engineered features using ONLY process variables that are
    available at prediction time. The target and failure-mode columns are
    never used here (prevents target leakage).
    """
    out = df.copy()
    air = out["Air temperature [K]"]
    proc = out["Process temperature [K]"]
    rpm = out["Rotational speed [rpm]"]
    torque = out["Torque [Nm]"]

    # Temperature difference (K). Same as a difference in degrees Celsius.
    out["temp_diff_K"] = proc - air

    # Temperature ratio - safe because Kelvin temperatures are absolute and > 0
    out["temp_ratio"] = proc / air

    # Raw mechanical power proxy (Nm * rpm) and proper power in watts:
    # P [W] = torque [Nm] * angular speed [rad/s] = torque * rpm * 2*pi / 60
    out["torque_x_rpm"] = torque * rpm
    out["power_W"] = torque * rpm * 2 * np.pi / 60

    # Tool-wear bands (minutes)
    bins = [-0.1, 50, 100, 150, 200, np.inf]
    labels = ["0-50", "51-100", "101-150", "151-200", "200+"]
    out["tool_wear_band"] = pd.cut(out["Tool wear [min]"], bins=bins, labels=labels)

    return out


def model_feature_columns():
    """Columns that may be used as model inputs in Level 2."""
    return (CATEGORICAL_COLS + SENSOR_COLS +
            ["temp_diff_K", "temp_ratio", "torque_x_rpm", "power_W", "tool_wear_band"])


def excluded_columns():
    """Columns that must NOT be used as model inputs, with reasons."""
    return {
        "UDI": "Row identifier - no physical meaning",
        "Product ID": "Identifier; its first letter duplicates 'Type'",
        "Machine failure": "Target variable",
        "TWF": "Failure-mode label (post-event, leaks the target)",
        "HDF": "Failure-mode label (post-event, leaks the target)",
        "PWF": "Failure-mode label (post-event, leaks the target)",
        "OSF": "Failure-mode label (post-event, leaks the target)",
        "RNF": "Failure-mode label (post-event, leaks the target)",
    }
