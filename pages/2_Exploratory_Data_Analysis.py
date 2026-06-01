# ============================================================
# Page 2 — Exploratory Data Analysis
# ============================================================

import streamlit as st

from utils.data_loader import load_final_dataset, load_fear_greed_dataset
from utils.charts import (
    sentiment_distribution_chart,
    monthly_trading_activity_chart,
    top_coins_chart,
    top_traders_chart,
    direction_distribution_chart,
    fear_greed_over_time_chart,
)
from utils.constants import PAGE_ICON
from utils.styles import inject_css

st.set_page_config(
    page_title="EDA | PrimeTrade.ai",
    page_icon=PAGE_ICON,
    layout="wide",
)
inject_css()

st.title("🔍 Exploratory Data Analysis")
st.caption("Dynamic charts generated directly from the trade dataset.")

# ── Load ───────────────────────────────────────────────────────────────────
df = load_final_dataset()
fg = load_fear_greed_dataset()

if df.empty:
    st.stop()


def insight(text: str) -> None:
    st.markdown(f'<div class="pt-insight">💡 {text}</div>', unsafe_allow_html=True)


# ── 1. Sentiment Distribution ──────────────────────────────────────────────
st.markdown('<p class="pt-section">1. Sentiment Distribution</p>', unsafe_allow_html=True)
st.plotly_chart(sentiment_distribution_chart(df), use_container_width=True)

if "classification" in df.columns:
    top_sent = df["classification"].value_counts().idxmax()
    top_cnt  = df["classification"].value_counts().max()
    pct      = top_cnt / len(df) * 100
    insight(
        f"<strong>{top_sent}</strong> is the dominant sentiment, accounting for "
        f"<strong>{top_cnt:,} trades ({pct:.1f}%)</strong> of all activity — indicating "
        f"most trades occurred during periods of "
        f"{'heightened optimism' if 'Greed' in str(top_sent) else 'market uncertainty'}."
    )

# ── 2. Monthly Trading Activity ────────────────────────────────────────────
st.markdown('<p class="pt-section">2. Monthly Trading Activity</p>', unsafe_allow_html=True)
st.plotly_chart(monthly_trading_activity_chart(df), use_container_width=True)

if "Year_Month" in df.columns:
    monthly_counts = df.groupby("Year_Month").size()
    peak_month = monthly_counts.idxmax()
    peak_count = monthly_counts.max()
    insight(
        f"Trading activity peaked in <strong>{peak_month}</strong> with "
        f"<strong>{peak_count:,} trades</strong>. Spikes often correlate with major "
        f"market events or extreme sentiment readings."
    )

# ── 3. Top 10 Coins ────────────────────────────────────────────────────────
st.markdown('<p class="pt-section">3. Top 10 Coins by Trade Count</p>', unsafe_allow_html=True)
st.plotly_chart(top_coins_chart(df, n=10), use_container_width=True)

if "Coin" in df.columns:
    top_coin     = df["Coin"].value_counts().idxmax()
    top_coin_cnt = df["Coin"].value_counts().max()
    pct_coin     = top_coin_cnt / len(df) * 100
    insight(
        f"<strong>{top_coin}</strong> dominates with "
        f"<strong>{top_coin_cnt:,} trades ({pct_coin:.1f}%)</strong>. "
        f"Concentration in a few coins suggests traders focus on high-liquidity assets."
    )

# ── 4. Top 10 Traders ─────────────────────────────────────────────────────
st.markdown('<p class="pt-section">4. Top 10 Traders by Trade Count</p>', unsafe_allow_html=True)
st.plotly_chart(top_traders_chart(df, n=10), use_container_width=True)

if "Account" in df.columns:
    top_trader     = df["Account"].value_counts().idxmax()
    top_trader_cnt = df["Account"].value_counts().max()
    pct_trader     = top_trader_cnt / len(df) * 100
    insight(
        f"The most active trader (<strong>{top_trader[:12]}…</strong>) executed "
        f"<strong>{top_trader_cnt:,} trades ({pct_trader:.1f}%)</strong> — "
        f"suggesting algorithmic or high-frequency trading behaviour."
    )

# ── 5. Trade Direction Distribution ───────────────────────────────────────
st.markdown('<p class="pt-section">5. Trade Direction Distribution</p>', unsafe_allow_html=True)

col_pie, col_info = st.columns([2, 1], gap="medium")

with col_pie:
    if "Direction" in df.columns:
        st.plotly_chart(direction_distribution_chart(df), use_container_width=True)
    else:
        st.warning("Direction column not found.")

with col_info:
    if "Direction" in df.columns:
        st.markdown("**Direction breakdown**")
        for d, c in df["Direction"].value_counts().items():
            pct = c / len(df) * 100
            st.metric(label=str(d), value=f"{c:,}", delta=f"{pct:.1f}%")

if "Direction" in df.columns:
    dominant_dir = df["Direction"].value_counts().idxmax()
    insight(
        f"<strong>{dominant_dir}</strong> trades are more prevalent. "
        f"A balanced Buy/Sell ratio suggests active two-sided market participation, "
        f"while imbalance may indicate directional bias driven by sentiment."
    )

# ── 6. Fear & Greed Index Over Time ───────────────────────────────────────
st.markdown('<p class="pt-section">6. Fear & Greed Index Over Time</p>', unsafe_allow_html=True)

if not fg.empty and "date" in fg.columns and "value" in fg.columns:
    st.plotly_chart(fear_greed_over_time_chart(fg), use_container_width=True)
    avg_score = fg["value"].mean()
    insight(
        f"The Fear & Greed Index averaged <strong>{avg_score:.1f}</strong> over the dataset "
        f"period. Scores above 75 indicate Extreme Greed (potential market tops), "
        f"while scores below 25 indicate Extreme Fear (potential buying opportunities)."
    )
else:
    st.info("Fear & Greed index data not available for this chart.")

st.markdown(
    '<div class="pt-footer">PrimeTrade.ai · Exploratory Data Analysis</div>',
    unsafe_allow_html=True,
)
