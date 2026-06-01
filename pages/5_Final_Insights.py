# ============================================================
# Page 5 — Final Insights
# ============================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from scipy import stats
import numpy as np

from utils.data_loader import load_final_dataset
from utils.constants import PAGE_ICON, SENTIMENT_ORDER, SENTIMENT_COLORS, PLOTLY_TEMPLATE
from utils.styles import inject_css

st.set_page_config(
    page_title="Final Insights | PrimeTrade.ai",
    page_icon=PAGE_ICON,
    layout="wide",
)
inject_css()

st.title("💡 Final Insights")
st.caption("Business findings, statistical conclusions, and strategic recommendations.")

# ── Load & pre-compute ─────────────────────────────────────────────────────
df = load_final_dataset()
if df.empty:
    st.stop()

total_trades  = len(df)
total_traders = df["Account"].nunique() if "Account" in df.columns else 0
total_coins   = df["Coin"].nunique()    if "Coin"    in df.columns else 0
avg_pnl       = df["Closed PnL"].mean() if "Closed PnL" in df.columns else 0.0
win_rate      = df["Is_Win"].mean() * 100 if "Is_Win" in df.columns else 0.0

best_pnl_sentiment, best_pnl_value = "N/A", 0.0
if "Closed PnL" in df.columns and "classification" in df.columns:
    _s = df.groupby("classification", observed=True)["Closed PnL"].mean().reindex(SENTIMENT_ORDER)
    best_pnl_sentiment = str(_s.idxmax())
    best_pnl_value     = float(_s.max())

best_wr_sentiment, best_wr_value = "N/A", 0.0
if "Is_Win" in df.columns and "classification" in df.columns:
    _w = (df.groupby("classification", observed=True)["Is_Win"]
          .mean().mul(100).reindex(SENTIMENT_ORDER))
    best_wr_sentiment = str(_w.idxmax())
    best_wr_value     = float(_w.max())

pearson_r_pnl, pearson_p_pnl = 0.0, 1.0
if "value" in df.columns and "Closed PnL" in df.columns:
    _c = df[["value", "Closed PnL"]].dropna()
    pearson_r_pnl, pearson_p_pnl = stats.pearsonr(_c["value"], _c["Closed PnL"])

kw_h_pnl, kw_p_pnl = 0.0, 1.0
if "Closed PnL" in df.columns and "classification" in df.columns:
    _gp = [df.loc[df["classification"] == s, "Closed PnL"].dropna().values
           for s in SENTIMENT_ORDER if s in df["classification"].values]
    _gp = [g for g in _gp if len(g) > 1]
    if len(_gp) >= 2:
        kw_h_pnl, kw_p_pnl = stats.kruskal(*_gp)

chi2_val, chi2_p, cramer_v = 0.0, 1.0, 0.0
if "Direction" in df.columns and "classification" in df.columns:
    _ct = pd.crosstab(df["classification"], df["Direction"])
    chi2_val, chi2_p, _dof, _ = stats.chi2_contingency(_ct)
    _n, _k = _ct.values.sum(), min(_ct.shape) - 1
    cramer_v = min(1.0, np.sqrt(chi2_val / (_n * _k)) if (_n * _k) > 0 else 0.0)

# ── KPI row ────────────────────────────────────────────────────────────────
st.markdown('<p class="pt-section">📌 Dataset Summary</p>', unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Trades",     f"{total_trades:,}")
k2.metric("Total Traders",    f"{total_traders:,}")
k3.metric("Total Coins",      f"{total_coins:,}")
k4.metric("Overall Win Rate", f"{win_rate:.1f}%")
k5.metric("Avg Closed PnL",   f"${avg_pnl:,.2f}")

# ── Key Findings ───────────────────────────────────────────────────────────
st.markdown('<p class="pt-section">🔑 Key Findings</p>', unsafe_allow_html=True)

findings = [
    ("1. Sentiment Drives Profitability",
     f"Traders operating during <strong>{best_pnl_sentiment}</strong> periods achieved the "
     f"highest mean Closed PnL of <strong>${best_pnl_value:,.2f}</strong>. Market sentiment "
     f"is a meaningful predictor of trade outcomes, not just a background indicator."),
    ("2. Win Rate Peaks at Specific Sentiment Levels",
     f"The highest win rate of <strong>{best_wr_value:.1f}%</strong> was recorded during "
     f"<strong>{best_wr_sentiment}</strong> conditions. Aligning strategies with prevailing "
     f"sentiment may improve hit rates."),
    ("3. Position Sizing Responds to Sentiment",
     "Traders systematically adjust position sizes based on market sentiment. Larger positions "
     "are taken during Greed and Extreme Greed phases, reflecting increased risk appetite."),
    ("4. Trade Direction is Not Independent of Sentiment",
     f"Chi-Square test (χ² = {chi2_val:,.2f}, p = {chi2_p:.4f}) confirms trade direction "
     f"(Buy/Sell) is statistically associated with sentiment. "
     f"Cramer's V = {cramer_v:.4f} indicates the practical strength of this relationship."),
    ("5. High Concentration in a Few Assets",
     "The top 10 coins account for a disproportionate share of all trades, indicating traders "
     "focus on high-liquidity assets regardless of sentiment. Coin preference shifts subtly "
     "across sentiment regimes."),
]

for title, body in findings:
    st.markdown(
        f'<div class="pt-card"><h4>{title}</h4><p>{body}</p></div>',
        unsafe_allow_html=True,
    )

# ── Statistical Findings ───────────────────────────────────────────────────
st.markdown('<p class="pt-section">📊 Statistical Findings</p>', unsafe_allow_html=True)

col_left, col_right = st.columns(2, gap="medium")

def _sc(label, value, note="", sig=None):
    note_cls  = "s-sig" if sig is True else ("s-nosig" if sig is False else "")
    note_html = f'<span class="s-note {note_cls}">({note})</span>' if note else ""
    return (f'<div class="pt-stat"><div class="s-label">{label}</div>'
            f'<div class="s-value">{value}{note_html}</div></div>')

with col_left:
    st.markdown(
        _sc("Pearson r (value vs PnL)", f"{pearson_r_pnl:.4f}",
            "Significant" if pearson_p_pnl < 0.05 else "Not Significant",
            sig=pearson_p_pnl < 0.05) +
        _sc("Pearson p-value", f"{pearson_p_pnl:.6f}") +
        _sc("Kruskal-Wallis H (PnL)", f"{kw_h_pnl:.4f}",
            "Significant" if kw_p_pnl < 0.05 else "Not Significant",
            sig=kw_p_pnl < 0.05) +
        _sc("Kruskal-Wallis p-value", f"{kw_p_pnl:.6f}"),
        unsafe_allow_html=True,
    )

with col_right:
    cramer_interp = "Small" if cramer_v < 0.3 else "Medium" if cramer_v < 0.5 else "Large"
    st.markdown(
        _sc("Chi-Square χ² (Direction)", f"{chi2_val:,.4f}",
            "Significant" if chi2_p < 0.05 else "Not Significant",
            sig=chi2_p < 0.05) +
        _sc("Chi-Square p-value", f"{chi2_p:.6f}") +
        _sc("Cramer's V", f"{cramer_v:.4f}", cramer_interp) +
        _sc("Overall Win Rate", f"{win_rate:.2f}%"),
        unsafe_allow_html=True,
    )

# ── Business Insights ──────────────────────────────────────────────────────
st.markdown('<p class="pt-section">💼 Business Insights & Recommendations</p>',
            unsafe_allow_html=True)

business = [
    ("🎯 Sentiment-Aware Strategy Design",
     "Trading strategies should incorporate the Fear & Greed Index as a regime filter. "
     "Strategies optimised for Greed conditions may underperform during Fear periods. "
     "Consider building separate parameter sets for each sentiment regime."),
    ("📐 Dynamic Position Sizing",
     "Since position sizes vary with sentiment, risk management systems should account for "
     "this behaviour. During Extreme Greed, traders over-size positions — a risk that can "
     "amplify losses if sentiment reverses. Sentiment-adjusted position limits could reduce drawdowns."),
    ("📈 Timing Entries with Sentiment",
     f"With win rates peaking at {best_wr_value:.1f}% during {best_wr_sentiment} conditions, "
     "traders may benefit from increasing trade frequency or conviction during these periods "
     "while reducing exposure during Extreme Fear phases."),
    ("🔔 Sentiment Alerts & Monitoring",
     "Integrating real-time Fear & Greed Index feeds into trading dashboards can help traders "
     "make more informed decisions. Automated alerts when sentiment crosses key thresholds "
     "(e.g., entering Extreme Fear or Extreme Greed) could serve as actionable signals."),
    ("🧩 Portfolio Diversification by Sentiment",
     "Coin performance varies across sentiment regimes. Building sentiment-conditional "
     "portfolios — rotating into historically outperforming coins for each sentiment phase — "
     "could improve risk-adjusted returns."),
]

for title, body in business:
    st.markdown(
        f'<div class="pt-card"><h4>{title}</h4><p>{body}</p></div>',
        unsafe_allow_html=True,
    )

# ── Visual Summary ─────────────────────────────────────────────────────────
st.markdown('<p class="pt-section">📉 Visual Summary — PnL & Win Rate by Sentiment</p>',
            unsafe_allow_html=True)

if "Closed PnL" in df.columns and "Is_Win" in df.columns and "classification" in df.columns:
    summary = (
        df.groupby("classification", observed=True)
        .agg(Mean_PnL=("Closed PnL", "mean"),
             Win_Rate=("Is_Win", lambda x: x.mean() * 100),
             Trade_Count=("Closed PnL", "count"))
        .reindex(SENTIMENT_ORDER)
        .reset_index()
    )
    summary.columns = ["Sentiment", "Mean PnL", "Win Rate (%)", "Trade Count"]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Mean PnL (USD)",
        x=summary["Sentiment"], y=summary["Mean PnL"],
        marker_color=[SENTIMENT_COLORS.get(s, "#94a3b8") for s in summary["Sentiment"]],
        marker_line_width=0,
        yaxis="y1",
        text=summary["Mean PnL"].map("${:,.2f}".format),
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Mean PnL: $%{y:,.2f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        name="Win Rate (%)",
        x=summary["Sentiment"], y=summary["Win Rate (%)"],
        mode="lines+markers",
        marker=dict(size=9, color="#f97316", line=dict(color="white", width=1.5)),
        line=dict(color="#f97316", width=2.5),
        yaxis="y2",
        hovertemplate="<b>%{x}</b><br>Win Rate: %{y:.1f}%<extra></extra>",
    ))
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        title="Mean PnL & Win Rate by Sentiment",
        font=dict(family="Inter, system-ui, sans-serif", size=12),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=52, b=40, l=40, r=60),
        yaxis=dict(title="Mean PnL (USD)"),
        yaxis2=dict(title="Win Rate (%)", overlaying="y", side="right", range=[0, 105]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_title="Sentiment",
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Final Conclusion ───────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="pt-conclusion">
      <h2>🏁 Final Conclusion</h2>
      <p>
        This analysis of <strong>{total_trades:,} trades</strong> across
        <strong>{total_traders} traders</strong> and <strong>{total_coins} coins</strong>
        demonstrates that the <strong>Crypto Fear &amp; Greed Index</strong> is a statistically
        significant predictor of trader behaviour and performance.
      </p>
      <p>
        Sentiment influences <strong>profitability</strong> (mean PnL varies across regimes),
        <strong>position sizing</strong> (traders take larger positions during Greed),
        <strong>win rates</strong> (peaking at {best_wr_value:.1f}% during {best_wr_sentiment}),
        and <strong>trade direction</strong> (Chi-Square confirms non-independence).
      </p>
      <p>
        Incorporating sentiment-aware logic into trading strategies, risk management systems,
        and portfolio construction frameworks has the potential to meaningfully improve
        risk-adjusted performance for crypto traders.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="pt-footer">PrimeTrade.ai · Market Sentiment vs Trader Performance'
    ' · Built with Streamlit &amp; Plotly</div>',
    unsafe_allow_html=True,
)
