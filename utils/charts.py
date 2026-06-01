# ============================================================
# charts.py — Reusable Plotly chart functions
# ============================================================

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.constants import SENTIMENT_ORDER, SENTIMENT_COLORS, PLOTLY_TEMPLATE

# ── Shared layout defaults ─────────────────────────────────────────────────
_LAYOUT = dict(
    template=PLOTLY_TEMPLATE,
    font=dict(family="Inter, system-ui, sans-serif", size=12),
    margin=dict(t=52, b=40, l=40, r=20),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    hoverlabel=dict(bgcolor="white", font_size=13, font_family="Inter, sans-serif"),
)


def _base(**kwargs) -> dict:
    d = dict(_LAYOUT)
    d.update(kwargs)
    return d


def _sentiment_colors(categories) -> list:
    return [SENTIMENT_COLORS.get(c, "#94a3b8") for c in categories]


# ── Sentiment Distribution ─────────────────────────────────────────────────

def sentiment_distribution_chart(df: pd.DataFrame) -> go.Figure:
    counts = (
        df["classification"]
        .value_counts()
        .reindex(SENTIMENT_ORDER, fill_value=0)
        .reset_index()
    )
    counts.columns = ["Sentiment", "Trades"]

    fig = px.bar(
        counts, x="Sentiment", y="Trades",
        color="Sentiment",
        color_discrete_map=SENTIMENT_COLORS,
        text="Trades",
        title="Trade Count by Sentiment Regime",
    )
    fig.update_traces(
        texttemplate="%{text:,}",
        textposition="outside",
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Trades: %{y:,}<extra></extra>",
    )
    fig.update_layout(**_base(showlegend=False,
                              xaxis_title="Sentiment", yaxis_title="Number of Trades"))
    return fig


# ── Monthly Trading Activity ───────────────────────────────────────────────

def monthly_trading_activity_chart(df: pd.DataFrame) -> go.Figure:
    if "Year_Month" not in df.columns:
        return go.Figure()
    monthly = df.groupby("Year_Month").size().reset_index(name="Trades")
    monthly = monthly.sort_values("Year_Month")

    fig = px.area(
        monthly, x="Year_Month", y="Trades",
        title="Monthly Trading Activity",
        color_discrete_sequence=["#2563EB"],
    )
    fig.update_traces(
        line_width=2,
        fillcolor="rgba(37,99,235,0.12)",
        hovertemplate="<b>%{x}</b><br>Trades: %{y:,}<extra></extra>",
    )
    fig.update_layout(**_base(xaxis_title="Month", yaxis_title="Number of Trades"))
    fig.update_xaxes(tickangle=45)
    return fig


# ── Top Coins ──────────────────────────────────────────────────────────────

def top_coins_chart(df: pd.DataFrame, n: int = 10) -> go.Figure:
    top = df["Coin"].value_counts().head(n).reset_index()
    top.columns = ["Coin", "Trades"]
    top = top.sort_values("Trades")

    fig = px.bar(
        top, x="Trades", y="Coin", orientation="h",
        text="Trades",
        title=f"Top {n} Coins by Trade Count",
        color="Trades",
        color_continuous_scale=["#dbeafe", "#2563EB"],
    )
    fig.update_traces(
        texttemplate="%{text:,}", textposition="outside",
        marker_line_width=0,
        hovertemplate="<b>%{y}</b><br>Trades: %{x:,}<extra></extra>",
    )
    fig.update_layout(**_base(yaxis_title="", xaxis_title="Number of Trades",
                              coloraxis_showscale=False))
    return fig


# ── Top Traders ────────────────────────────────────────────────────────────

def top_traders_chart(df: pd.DataFrame, n: int = 10) -> go.Figure:
    top = df["Account"].value_counts().head(n).reset_index()
    top.columns = ["Account", "Trades"]
    top["Account"] = top["Account"].str[:10] + "…"
    top = top.sort_values("Trades")

    fig = px.bar(
        top, x="Trades", y="Account", orientation="h",
        text="Trades",
        title=f"Top {n} Traders by Trade Count",
        color="Trades",
        color_continuous_scale=["#fef3c7", "#f97316"],
    )
    fig.update_traces(
        texttemplate="%{text:,}", textposition="outside",
        marker_line_width=0,
        hovertemplate="<b>%{y}</b><br>Trades: %{x:,}<extra></extra>",
    )
    fig.update_layout(**_base(yaxis_title="", xaxis_title="Number of Trades",
                              coloraxis_showscale=False))
    return fig


# ── Direction Distribution ─────────────────────────────────────────────────

def direction_distribution_chart(df: pd.DataFrame) -> go.Figure:
    counts = df["Direction"].value_counts().reset_index()
    counts.columns = ["Direction", "Count"]

    fig = px.pie(
        counts, names="Direction", values="Count",
        title="Trade Direction Distribution",
        color_discrete_sequence=["#2563EB", "#f97316", "#22c55e", "#ef4444"],
        hole=0.42,
    )
    fig.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>",
        marker=dict(line=dict(color="white", width=2)),
    )
    fig.update_layout(**_base())
    return fig


# ── PnL by Sentiment ───────────────────────────────────────────────────────

def pnl_by_sentiment_chart(df: pd.DataFrame) -> go.Figure:
    grp = (
        df.groupby("classification", observed=True)["Closed PnL"]
        .agg(Mean="mean", Median="median")
        .reindex(SENTIMENT_ORDER)
        .reset_index()
    )
    grp.columns = ["Sentiment", "Mean PnL", "Median PnL"]

    fig = go.Figure()
    for metric, color in [("Mean PnL", "#2563EB"), ("Median PnL", "#f97316")]:
        fig.add_trace(go.Bar(
            name=metric, x=grp["Sentiment"], y=grp[metric],
            marker_color=color, marker_line_width=0,
            hovertemplate=f"<b>%{{x}}</b><br>{metric}: $%{{y:,.2f}}<extra></extra>",
        ))
    fig.update_layout(**_base(
        barmode="group",
        title="Mean & Median Closed PnL by Sentiment",
        xaxis_title="Sentiment", yaxis_title="Closed PnL (USD)",
    ))
    return fig


# ── Position Size by Sentiment ─────────────────────────────────────────────

def position_size_by_sentiment_chart(df: pd.DataFrame) -> go.Figure:
    grp = (
        df.groupby("classification", observed=True)["Size USD"]
        .mean()
        .reindex(SENTIMENT_ORDER)
        .reset_index()
    )
    grp.columns = ["Sentiment", "Mean Size USD"]

    fig = px.bar(
        grp, x="Sentiment", y="Mean Size USD",
        color="Sentiment", color_discrete_map=SENTIMENT_COLORS,
        text="Mean Size USD",
        title="Mean Position Size (USD) by Sentiment",
    )
    fig.update_traces(
        texttemplate="$%{text:,.0f}", textposition="outside",
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Avg Size: $%{y:,.2f}<extra></extra>",
    )
    fig.update_layout(**_base(showlegend=False,
                              xaxis_title="Sentiment", yaxis_title="Mean Size USD"))
    return fig


# ── Win Rate by Sentiment ──────────────────────────────────────────────────

def win_rate_by_sentiment_chart(df: pd.DataFrame) -> go.Figure:
    grp = (
        df.groupby("classification", observed=True)["Is_Win"]
        .mean().mul(100)
        .reindex(SENTIMENT_ORDER)
        .reset_index()
    )
    grp.columns = ["Sentiment", "Win Rate (%)"]

    fig = px.bar(
        grp, x="Sentiment", y="Win Rate (%)",
        color="Sentiment", color_discrete_map=SENTIMENT_COLORS,
        text="Win Rate (%)",
        title="Win Rate (%) by Sentiment",
    )
    fig.update_traces(
        texttemplate="%{text:.1f}%", textposition="outside",
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Win Rate: %{y:.1f}%<extra></extra>",
    )
    fig.add_hline(y=50, line_dash="dash", line_color="#94a3b8",
                  annotation_text="50% breakeven", annotation_position="right")
    fig.update_layout(**_base(showlegend=False,
                              xaxis_title="Sentiment", yaxis_title="Win Rate (%)",
                              yaxis_range=[0, 105]))
    return fig


# ── Activity by Sentiment ──────────────────────────────────────────────────

def activity_by_sentiment_chart(df: pd.DataFrame) -> go.Figure:
    counts = (
        df["classification"].value_counts()
        .reindex(SENTIMENT_ORDER, fill_value=0)
        .reset_index()
    )
    counts.columns = ["Sentiment", "Trades"]

    fig = px.bar(
        counts, x="Sentiment", y="Trades",
        color="Sentiment", color_discrete_map=SENTIMENT_COLORS,
        text="Trades",
        title="Trading Activity by Sentiment",
    )
    fig.update_traces(
        texttemplate="%{text:,}", textposition="outside",
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Trades: %{y:,}<extra></extra>",
    )
    fig.update_layout(**_base(showlegend=False,
                              xaxis_title="Sentiment", yaxis_title="Number of Trades"))
    return fig


# ── Fear & Greed Index Over Time ───────────────────────────────────────────

def fear_greed_over_time_chart(fg: pd.DataFrame) -> go.Figure:
    fg_sorted = fg.sort_values("date")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=fg_sorted["date"], y=fg_sorted["value"],
        mode="lines",
        line=dict(color="#2563EB", width=1.5),
        fill="tozeroy",
        fillcolor="rgba(37,99,235,0.08)",
        name="F&G Score",
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>Score: %{y}<extra></extra>",
    ))
    for level, label, color in [
        (25, "Extreme Fear ≤25", "#ef4444"),
        (50, "Neutral 50",       "#eab308"),
        (75, "Extreme Greed ≥75","#22c55e"),
    ]:
        fig.add_hline(y=level, line_dash="dot", line_color=color, line_width=1,
                      annotation_text=label, annotation_position="right",
                      annotation_font_size=10)
    fig.update_layout(**_base(
        title="Fear & Greed Index Over Time",
        xaxis_title="Date", yaxis_title="Score (0–100)",
        yaxis_range=[0, 105],
    ))
    return fig


# ── Correlation Scatter ────────────────────────────────────────────────────

def correlation_scatter(df: pd.DataFrame, x_col: str, y_col: str,
                        title: str) -> go.Figure:
    sample = df[[x_col, y_col]].dropna().sample(min(5000, len(df)), random_state=42)
    fig = px.scatter(
        sample, x=x_col, y=y_col,
        trendline="ols",
        title=title,
        opacity=0.35,
        color_discrete_sequence=["#2563EB"],
    )
    fig.update_traces(
        hovertemplate=f"<b>{x_col}</b>: %{{x}}<br><b>{y_col}</b>: %{{y:,.2f}}<extra></extra>",
    )
    fig.update_layout(**_base(xaxis_title=x_col, yaxis_title=y_col))
    return fig
