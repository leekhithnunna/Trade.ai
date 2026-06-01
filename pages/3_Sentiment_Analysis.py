# ============================================================
# Page 3 — Sentiment Analysis
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_final_dataset
from utils.charts import (
    pnl_by_sentiment_chart,
    position_size_by_sentiment_chart,
    win_rate_by_sentiment_chart,
    activity_by_sentiment_chart,
)
from utils.constants import PAGE_ICON, SENTIMENT_ORDER, SENTIMENT_COLORS, PLOTLY_TEMPLATE
from utils.styles import inject_css

st.set_page_config(
    page_title="Sentiment Analysis | PrimeTrade.ai",
    page_icon=PAGE_ICON,
    layout="wide",
)
inject_css()

st.title("📈 Sentiment Analysis")
st.caption("How Fear & Greed sentiment shapes trader profitability, sizing, and behaviour.")

# ── Load ───────────────────────────────────────────────────────────────────
df = load_final_dataset()
if df.empty:
    st.stop()


def insight(text: str) -> None:
    st.markdown(f'<div class="pt-insight">💡 {text}</div>', unsafe_allow_html=True)


# ── 1. Sentiment vs Closed PnL ─────────────────────────────────────────────
st.markdown('<p class="pt-section">1. Sentiment vs Closed PnL</p>', unsafe_allow_html=True)

if "Closed PnL" in df.columns and "classification" in df.columns:
    pnl_agg = (
        df.groupby("classification", observed=True)["Closed PnL"]
        .agg(Mean="mean", Median="median", Total="sum", Count="count")
        .reindex(SENTIMENT_ORDER)
    )
    best_pnl_idx      = pnl_agg["Mean"].idxmax()
    best_pnl_mean_val = float(pnl_agg.loc[best_pnl_idx, "Mean"])

    pnl_grp = pnl_agg.reset_index()
    pnl_grp.columns = ["Sentiment", "Mean PnL", "Median PnL", "Total PnL", "Trade Count"]

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Best Mean PnL Sentiment", str(best_pnl_idx), f"${best_pnl_mean_val:,.2f}")
    col_b.metric("Overall Mean PnL",   f"${df['Closed PnL'].mean():,.2f}")
    col_c.metric("Overall Median PnL", f"${df['Closed PnL'].median():,.2f}")

    st.plotly_chart(pnl_by_sentiment_chart(df), use_container_width=True)

    display_pnl = pnl_grp.copy()
    display_pnl["Mean PnL"]    = display_pnl["Mean PnL"].map("${:,.2f}".format)
    display_pnl["Median PnL"]  = display_pnl["Median PnL"].map("${:,.2f}".format)
    display_pnl["Total PnL"]   = display_pnl["Total PnL"].map("${:,.0f}".format)
    display_pnl["Trade Count"] = display_pnl["Trade Count"].map("{:,}".format)
    st.dataframe(display_pnl, use_container_width=True, hide_index=True)

    insight(
        f"Traders in <strong>{best_pnl_idx}</strong> periods achieved the highest mean PnL "
        f"of <strong>${best_pnl_mean_val:,.2f}</strong>. Sentiment conditions meaningfully "
        f"influence trade outcomes."
    )
else:
    st.warning("Required columns (Closed PnL, classification) not found.")

# ── 2. Sentiment vs Position Size ─────────────────────────────────────────
st.markdown('<p class="pt-section">2. Sentiment vs Position Size</p>', unsafe_allow_html=True)

if "Size USD" in df.columns and "classification" in df.columns:
    size_agg = (
        df.groupby("classification", observed=True)["Size USD"]
        .agg(Mean="mean", Median="median")
        .reindex(SENTIMENT_ORDER)
    )
    best_size_idx      = size_agg["Mean"].idxmax()
    best_size_mean_val = float(size_agg.loc[best_size_idx, "Mean"])

    size_grp = size_agg.reset_index()
    size_grp.columns = ["Sentiment", "Mean Size USD", "Median Size USD"]

    col_a, col_b = st.columns(2)
    col_a.metric("Largest Avg Position Sentiment", str(best_size_idx),
                 f"${best_size_mean_val:,.2f}")
    col_b.metric("Overall Avg Position Size", f"${df['Size USD'].mean():,.2f}")

    st.plotly_chart(position_size_by_sentiment_chart(df), use_container_width=True)

    display_size = size_grp.copy()
    display_size["Mean Size USD"]   = display_size["Mean Size USD"].map("${:,.2f}".format)
    display_size["Median Size USD"] = display_size["Median Size USD"].map("${:,.2f}".format)
    st.dataframe(display_size, use_container_width=True, hide_index=True)

    insight(
        f"Traders take the largest positions during <strong>{best_size_idx}</strong> periods "
        f"(avg ${best_size_mean_val:,.2f}), indicating higher risk appetite when sentiment "
        f"is elevated."
    )
else:
    st.warning("Required columns (Size USD, classification) not found.")

# ── 3. Sentiment vs Win Rate ───────────────────────────────────────────────
st.markdown('<p class="pt-section">3. Sentiment vs Win Rate</p>', unsafe_allow_html=True)

if "Is_Win" in df.columns and "classification" in df.columns:
    win_agg = (
        df.groupby("classification", observed=True)["Is_Win"]
        .agg(Win_Rate="mean", Total_Trades="count", Wins="sum")
        .reindex(SENTIMENT_ORDER)
    )
    win_agg["Win_Rate_Pct"] = (win_agg["Win_Rate"] * 100).round(2)
    win_agg["Losses"]       = win_agg["Total_Trades"] - win_agg["Wins"]

    best_wr_idx     = win_agg["Win_Rate_Pct"].idxmax()
    best_wr_pct_val = float(win_agg.loc[best_wr_idx, "Win_Rate_Pct"])

    win_grp = win_agg.reset_index()[
        ["classification", "Win_Rate_Pct", "Wins", "Losses", "Total_Trades"]
    ]
    win_grp.columns = ["Sentiment", "Win Rate (%)", "Wins", "Losses", "Total Trades"]

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Best Win Rate Sentiment", str(best_wr_idx), f"{best_wr_pct_val:.1f}%")
    col_b.metric("Overall Win Rate",        f"{df['Is_Win'].mean() * 100:.1f}%")
    col_c.metric("Total Winning Trades",    f"{int(df['Is_Win'].sum()):,}")

    st.plotly_chart(win_rate_by_sentiment_chart(df), use_container_width=True)

    display_wr = win_grp.copy()
    display_wr["Win Rate (%)"] = display_wr["Win Rate (%)"].map("{:.2f}%".format)
    display_wr["Wins"]         = display_wr["Wins"].map("{:,.0f}".format)
    display_wr["Losses"]       = display_wr["Losses"].map("{:,.0f}".format)
    display_wr["Total Trades"] = display_wr["Total Trades"].map("{:,.0f}".format)
    st.dataframe(display_wr, use_container_width=True, hide_index=True)

    insight(
        f"The highest win rate occurs during <strong>{best_wr_idx}</strong> periods at "
        f"<strong>{best_wr_pct_val:.1f}%</strong>. Win rates above 50% indicate profitable "
        f"conditions for traders."
    )
else:
    st.warning("Required columns (Is_Win, classification) not found.")

# ── 4. Sentiment vs Trading Activity ──────────────────────────────────────
st.markdown('<p class="pt-section">4. Sentiment vs Trading Activity</p>', unsafe_allow_html=True)

if "classification" in df.columns:
    st.plotly_chart(activity_by_sentiment_chart(df), use_container_width=True)

    act_grp = (
        df.groupby("classification", observed=True)
        .size()
        .reindex(SENTIMENT_ORDER, fill_value=0)
        .reset_index()
    )
    act_grp.columns = ["Sentiment", "Trade Count"]
    act_grp["% of Total"] = (act_grp["Trade Count"] / len(df) * 100).round(2)

    most_active_sentiment = act_grp.loc[act_grp["Trade Count"].idxmax(), "Sentiment"]

    display_act = act_grp.copy()
    display_act["Trade Count"] = display_act["Trade Count"].map("{:,}".format)
    display_act["% of Total"]  = display_act["% of Total"].map("{:.2f}%".format)
    st.dataframe(display_act, use_container_width=True, hide_index=True)

    insight(
        f"Trading activity is highest during <strong>{most_active_sentiment}</strong> periods. "
        f"Elevated activity during extreme sentiment phases may reflect momentum-driven "
        f"or panic-driven trading behaviour."
    )

# ── 5. Coin Performance by Sentiment ──────────────────────────────────────
st.markdown('<p class="pt-section">5. Coin Performance by Sentiment</p>', unsafe_allow_html=True)

if "Coin" in df.columns and "classification" in df.columns and "Closed PnL" in df.columns:
    selected_sentiment_coin = st.selectbox(
        "Select Sentiment:", options=SENTIMENT_ORDER, key="coin_sentiment_filter",
    )

    filtered_coin = df[df["classification"] == selected_sentiment_coin]
    top_coins_pnl = (
        filtered_coin.groupby("Coin")["Closed PnL"]
        .agg(Mean_PnL="mean", Total_PnL="sum", Trade_Count="count")
        .sort_values("Mean_PnL", ascending=False)
        .head(15)
        .reset_index()
    )

    if not top_coins_pnl.empty:
        fig_coin = px.bar(
            top_coins_pnl, x="Coin", y="Mean_PnL",
            color="Mean_PnL", color_continuous_scale="RdYlGn",
            template=PLOTLY_TEMPLATE,
            title=f"Top 15 Coins by Mean PnL — {selected_sentiment_coin}",
            text="Mean_PnL",
        )
        fig_coin.update_traces(
            texttemplate="$%{text:,.2f}", textposition="outside",
            marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>Mean PnL: $%{y:,.2f}<extra></extra>",
        )
        fig_coin.update_layout(
            xaxis_title="Coin", yaxis_title="Mean PnL (USD)",
            coloraxis_showscale=False,
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_coin, use_container_width=True)

        dc = top_coins_pnl.copy()
        dc["Mean_PnL"]    = dc["Mean_PnL"].map("${:,.2f}".format)
        dc["Total_PnL"]   = dc["Total_PnL"].map("${:,.0f}".format)
        dc["Trade_Count"] = dc["Trade_Count"].map("{:,}".format)
        dc.columns = ["Coin", "Mean PnL", "Total PnL", "Trade Count"]
        st.dataframe(dc, use_container_width=True, hide_index=True)
    else:
        st.info(f"No data available for {selected_sentiment_coin}.")

# ── 6. Trader Performance by Sentiment ────────────────────────────────────
st.markdown('<p class="pt-section">6. Trader Performance by Sentiment</p>', unsafe_allow_html=True)

if "Account" in df.columns and "classification" in df.columns and "Closed PnL" in df.columns:
    selected_sentiment_trader = st.selectbox(
        "Select Sentiment:", options=SENTIMENT_ORDER, key="trader_sentiment_filter",
    )

    filtered_trader = df[df["classification"] == selected_sentiment_trader]
    top_traders_pnl = (
        filtered_trader.groupby("Account")["Closed PnL"]
        .agg(Mean_PnL="mean", Total_PnL="sum", Trade_Count="count")
        .sort_values("Total_PnL", ascending=False)
        .head(10)
        .reset_index()
    )

    if not top_traders_pnl.empty:
        top_traders_pnl["Short_Account"] = top_traders_pnl["Account"].str[:12] + "…"

        fig_trader = px.bar(
            top_traders_pnl, x="Short_Account", y="Total_PnL",
            color="Total_PnL", color_continuous_scale="RdYlGn",
            template=PLOTLY_TEMPLATE,
            title=f"Top 10 Traders by Total PnL — {selected_sentiment_trader}",
            text="Total_PnL",
        )
        fig_trader.update_traces(
            texttemplate="$%{text:,.0f}", textposition="outside",
            marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>Total PnL: $%{y:,.0f}<extra></extra>",
        )
        fig_trader.update_layout(
            xaxis_title="Trader", yaxis_title="Total PnL (USD)",
            coloraxis_showscale=False,
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_trader, use_container_width=True)

        dt = top_traders_pnl[["Short_Account", "Mean_PnL", "Total_PnL", "Trade_Count"]].copy()
        dt["Mean_PnL"]    = dt["Mean_PnL"].map("${:,.2f}".format)
        dt["Total_PnL"]   = dt["Total_PnL"].map("${:,.0f}".format)
        dt["Trade_Count"] = dt["Trade_Count"].map("{:,}".format)
        dt.columns = ["Trader", "Mean PnL", "Total PnL", "Trade Count"]
        st.dataframe(dt, use_container_width=True, hide_index=True)
    else:
        st.info(f"No data available for {selected_sentiment_trader}.")

st.markdown(
    '<div class="pt-footer">PrimeTrade.ai · Sentiment Analysis</div>',
    unsafe_allow_html=True,
)
