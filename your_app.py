# ============================================================
# app.py — Landing page · PrimeTrade.ai Sentiment Dashboard
# ============================================================

import streamlit as st

from utils.constants import PAGE_TITLE, PAGE_ICON, PROJECT_DESCRIPTION
from utils.data_loader import load_final_dataset, load_fear_greed_dataset
from utils.styles import inject_css

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

# ── Load data ──────────────────────────────────────────────────────────────
df = load_final_dataset()
fg = load_fear_greed_dataset()

if df.empty:
    st.stop()

# ── Hero ───────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="pt-hero">
      <div class="pt-hero-title">📊 PrimeTrade.ai</div>
      <div class="pt-hero-sub">Market Sentiment vs Trader Performance Dashboard</div>
      <span class="pt-hero-badge">Crypto Fear &amp; Greed Analysis</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── KPI cards ──────────────────────────────────────────────────────────────
st.markdown('<p class="pt-section">📌 Dataset at a Glance</p>', unsafe_allow_html=True)

total_trades      = len(df)
total_traders     = df["Account"].nunique()  if "Account"    in df.columns else 0
total_coins       = df["Coin"].nunique()     if "Coin"       in df.columns else 0
avg_pnl           = df["Closed PnL"].mean()  if "Closed PnL" in df.columns else 0
avg_position_size = df["Size USD"].mean()    if "Size USD"   in df.columns else 0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Trades",      f"{total_trades:,}")
k2.metric("Total Traders",     f"{total_traders:,}")
k3.metric("Total Coins",       f"{total_coins:,}")
k4.metric("Avg Closed PnL",    f"${avg_pnl:,.2f}")
k5.metric("Avg Position Size", f"${avg_position_size:,.2f}")

# ── Project description ────────────────────────────────────────────────────
st.markdown('<p class="pt-section">🎯 Project Overview</p>', unsafe_allow_html=True)
st.markdown(PROJECT_DESCRIPTION)

# ── Dataset summary cards ──────────────────────────────────────────────────
st.markdown('<p class="pt-section">🗂️ Dataset Summary</p>', unsafe_allow_html=True)

col_left, col_right = st.columns(2, gap="medium")

with col_left:
    rows_trade = [("Rows", f"{len(df):,}"), ("Columns", str(df.shape[1]))]
    if "Merge_Date" in df.columns:
        rows_trade.append(("Date range",
                           f"{df['Merge_Date'].min().date()} → {df['Merge_Date'].max().date()}"))
    if "classification" in df.columns:
        for s, c in df["classification"].value_counts().items():
            rows_trade.append((str(s), f"{c:,} ({c/len(df)*100:.1f}%)"))

    rows_html = "".join(
        f'<div class="ds-row"><span class="ds-label">{lbl}</span>'
        f'<span class="ds-val">{val}</span></div>'
        for lbl, val in rows_trade
    )
    st.markdown(
        f'<div class="pt-ds-card"><h4>📁 Trade Dataset</h4>{rows_html}</div>',
        unsafe_allow_html=True,
    )

with col_right:
    rows_fg = []
    if "date" in fg.columns:
        rows_fg.append(("Date range",
                        f"{fg['date'].min().date()} → {fg['date'].max().date()}"))
    if "value" in fg.columns:
        rows_fg.append(("Score range", f"{fg['value'].min():.0f} – {fg['value'].max():.0f}"))
        rows_fg.append(("Mean score",  f"{fg['value'].mean():.1f}"))
    if "classification" in fg.columns:
        for s, c in fg["classification"].value_counts().items():
            rows_fg.append((str(s), f"{c} days"))

    rows_html2 = "".join(
        f'<div class="ds-row"><span class="ds-label">{lbl}</span>'
        f'<span class="ds-val">{val}</span></div>'
        for lbl, val in rows_fg
    )
    st.markdown(
        f'<div class="pt-ds-card"><h4>📈 Fear &amp; Greed Index</h4>{rows_html2}</div>',
        unsafe_allow_html=True,
    )

# ── Navigation guide ───────────────────────────────────────────────────────
st.markdown('<p class="pt-section">🧭 Navigation Guide</p>', unsafe_allow_html=True)

nav_items = [
    ("1️⃣", "Dataset Overview",
     "Shape, preview, column info, missing values, data types"),
    ("2️⃣", "Exploratory Data Analysis",
     "Sentiment distribution, monthly activity, top coins & traders"),
    ("3️⃣", "Sentiment Analysis",
     "PnL, position size, win rate, and activity broken down by sentiment"),
    ("4️⃣", "Hypothesis Testing",
     "Pearson, ANOVA, Kruskal-Wallis, Chi-Square, effect sizes"),
    ("5️⃣", "Final Insights",
     "Key findings, statistical summary, business recommendations"),
]

for icon, title, desc in nav_items:
    st.markdown(
        f"""
        <div class="pt-nav-card">
          <span class="nav-icon">{icon}</span>
          <div>
            <div class="nav-title">{title}</div>
            <div class="nav-desc">{desc}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="pt-footer">PrimeTrade.ai · Market Sentiment vs Trader Performance'
    ' · Built with Streamlit &amp; Plotly</div>',
    unsafe_allow_html=True,
)
