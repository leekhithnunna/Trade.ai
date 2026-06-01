# ============================================================
# data_loader.py — Cached CSV loaders for PrimeTrade Dashboard
# ============================================================

import os
import streamlit as st
import pandas as pd

# Resolve the data directory relative to this file so the app works
# both locally and on Streamlit Community Cloud.
_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def _data_path(filename: str) -> str:
    return os.path.normpath(os.path.join(_DATA_DIR, filename))


@st.cache_data(show_spinner="Loading trade dataset…")
def load_final_dataset() -> pd.DataFrame:
    """
    Load and lightly pre-process final_eda_dataset.csv.
    Returns an empty DataFrame with a warning if the file is missing.
    """
    path = _data_path("final_eda_dataset.csv")
    if not os.path.exists(path):
        st.error(
            f"❌ Could not find **final_eda_dataset.csv** at `{path}`. "
            "Please make sure the file is placed in the `data/` folder."
        )
        return pd.DataFrame()

    df = pd.read_csv(path, low_memory=False)

    # ── Normalise column names (strip whitespace) ──────────────────────────
    df.columns = df.columns.str.strip()

    # ── Parse dates ────────────────────────────────────────────────────────
    if "Merge_Date" in df.columns:
        df["Merge_Date"] = pd.to_datetime(df["Merge_Date"], errors="coerce")

    if "Timestamp IST" in df.columns:
        df["Timestamp IST"] = pd.to_datetime(df["Timestamp IST"], errors="coerce")

    # ── Numeric coercions ──────────────────────────────────────────────────
    for col in ["Closed PnL", "Size USD", "Size Tokens", "value", "Fee",
                "Execution Price", "Start Position"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # ── Derived columns ────────────────────────────────────────────────────
    if "Closed PnL" in df.columns:
        df["Is_Win"] = df["Closed PnL"] > 0

    if "Merge_Date" in df.columns:
        df["Year_Month"] = df["Merge_Date"].dt.to_period("M").astype(str)

    # ── Sentiment ordering ─────────────────────────────────────────────────
    sentiment_order = ["Extreme Fear", "Fear", "Neutral", "Greed", "Extreme Greed"]
    if "classification" in df.columns:
        df["classification"] = pd.Categorical(
            df["classification"], categories=sentiment_order, ordered=True
        )

    return df


@st.cache_data(show_spinner="Loading Fear & Greed index…")
def load_fear_greed_dataset() -> pd.DataFrame:
    """
    Load and pre-process fear_greed_index.csv.
    Returns an empty DataFrame with a warning if the file is missing.
    """
    path = _data_path("fear_greed_index.csv")
    if not os.path.exists(path):
        st.error(
            f"❌ Could not find **fear_greed_index.csv** at `{path}`. "
            "Please make sure the file is placed in the `data/` folder."
        )
        return pd.DataFrame()

    df = pd.read_csv(path, low_memory=False)
    df.columns = df.columns.str.strip()

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    if "value" in df.columns:
        df["value"] = pd.to_numeric(df["value"], errors="coerce")

    sentiment_order = ["Extreme Fear", "Fear", "Neutral", "Greed", "Extreme Greed"]
    if "classification" in df.columns:
        df["classification"] = pd.Categorical(
            df["classification"], categories=sentiment_order, ordered=True
        )

    return df
