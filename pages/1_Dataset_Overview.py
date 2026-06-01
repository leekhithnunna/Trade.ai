# ============================================================
# Page 1 — Dataset Overview
# ============================================================

import streamlit as st
import pandas as pd

from utils.data_loader import load_final_dataset, load_fear_greed_dataset
from utils.constants import PAGE_ICON
from utils.styles import inject_css

st.set_page_config(
    page_title="Dataset Overview | PrimeTrade.ai",
    page_icon=PAGE_ICON,
    layout="wide",
)
inject_css()

st.title("🗂️ Dataset Overview")
st.caption("Structural summary of the trade dataset and Fear & Greed index.")

# ── Load ───────────────────────────────────────────────────────────────────
df = load_final_dataset()
fg = load_fear_greed_dataset()

if df.empty:
    st.stop()

# ── KPI metrics ────────────────────────────────────────────────────────────
st.markdown('<p class="pt-section">📌 Key Metrics</p>', unsafe_allow_html=True)

total_trades      = len(df)
total_traders     = df["Account"].nunique()  if "Account"    in df.columns else 0
total_coins       = df["Coin"].nunique()     if "Coin"       in df.columns else 0
avg_pnl           = df["Closed PnL"].mean()  if "Closed PnL" in df.columns else 0
avg_position_size = df["Size USD"].mean()    if "Size USD"   in df.columns else 0

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Total Trades",      f"{total_trades:,}")
m2.metric("Total Traders",     f"{total_traders:,}")
m3.metric("Total Coins",       f"{total_coins:,}")
m4.metric("Avg Closed PnL",    f"${avg_pnl:,.2f}")
m5.metric("Avg Position Size", f"${avg_position_size:,.2f}")

# ── Tabs ───────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(
    ["📋 Data Preview", "🔢 Column Info", "❓ Missing Values", "📊 Data Types"]
)

# ── Tab 1: Data Preview ────────────────────────────────────────────────────
with tab1:
    st.markdown('<p class="pt-section">Data Preview</p>', unsafe_allow_html=True)
    st.caption(f"Showing first 100 rows of {len(df):,} total rows.")
    st.dataframe(df.head(100), use_container_width=True, height=420)

    st.markdown("---")
    st.markdown("**Fear & Greed Index — first 20 rows**")
    st.dataframe(fg.head(20), use_container_width=True)

# ── Tab 2: Column Info ─────────────────────────────────────────────────────
with tab2:
    st.markdown('<p class="pt-section">Column Information</p>', unsafe_allow_html=True)

    col_info = pd.DataFrame({
        "Column":   list(df.columns),
        "Dtype":    [str(df[c].dtype) for c in df.columns],
        "Non-Null": [int(df[c].notna().sum()) for c in df.columns],
        "Null":     [int(df[c].isna().sum())  for c in df.columns],
        "Unique":   [int(df[c].nunique())     for c in df.columns],
        "Sample":   [str(df[c].dropna().iloc[0]) if df[c].notna().any() else "N/A"
                     for c in df.columns],
    })
    st.dataframe(col_info, use_container_width=True, height=500)
    st.caption(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

# ── Tab 3: Missing Values ──────────────────────────────────────────────────
with tab3:
    st.markdown('<p class="pt-section">Missing Value Summary</p>', unsafe_allow_html=True)

    missing = pd.DataFrame({
        "Column":        list(df.columns),
        "Missing Count": [int(df[c].isna().sum()) for c in df.columns],
        "Missing %":     [round(df[c].isna().sum() / len(df) * 100, 2) for c in df.columns],
    }).sort_values("Missing Count", ascending=False)

    has_missing = missing[missing["Missing Count"] > 0]
    no_missing  = missing[missing["Missing Count"] == 0]

    if not has_missing.empty:
        st.warning(f"⚠️ {len(has_missing)} column(s) have missing values.")
        st.dataframe(has_missing, use_container_width=True, hide_index=True)
    else:
        st.success("✅ No missing values found in the trade dataset.")

    with st.expander("Show columns with zero missing values"):
        st.dataframe(no_missing, use_container_width=True, hide_index=True)

# ── Tab 4: Data Types ──────────────────────────────────────────────────────
with tab4:
    st.markdown('<p class="pt-section">Data Types & Descriptive Statistics</p>',
                unsafe_allow_html=True)

    dtype_counts = pd.DataFrame({
        "Dtype": [str(k) for k in df.dtypes.value_counts().index],
        "Count": list(df.dtypes.value_counts().values),
    })
    st.markdown("**Dtype distribution:**")
    st.dataframe(dtype_counts, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("**Descriptive statistics — numeric columns:**")
    num_cols = df.select_dtypes(include="number").columns.tolist()
    if num_cols:
        numeric_desc = df[num_cols].describe().T.round(4).reset_index()
        numeric_desc.rename(columns={"index": "Column"}, inplace=True)
        st.dataframe(numeric_desc, use_container_width=True, height=350)
    else:
        st.info("No numeric columns found.")

    st.markdown("---")
    st.markdown("**Descriptive statistics — categorical columns:**")
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    if cat_cols:
        cat_desc = df[cat_cols].describe().T.reset_index()
        cat_desc.rename(columns={"index": "Column"}, inplace=True)
        cat_desc = cat_desc.astype(str)
        st.dataframe(cat_desc, use_container_width=True)
    else:
        st.info("No categorical columns found.")

st.markdown(
    '<div class="pt-footer">PrimeTrade.ai · Dataset Overview</div>',
    unsafe_allow_html=True,
)
