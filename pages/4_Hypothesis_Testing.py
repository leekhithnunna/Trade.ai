# ============================================================
# Page 4 — Hypothesis Testing
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

from utils.data_loader import load_final_dataset
from utils.constants import PAGE_ICON, SENTIMENT_ORDER, PLOTLY_TEMPLATE
from utils.styles import inject_css

st.set_page_config(
    page_title="Hypothesis Testing | PrimeTrade.ai",
    page_icon=PAGE_ICON,
    layout="wide",
)
inject_css()

st.title("🧪 Hypothesis Testing")
st.caption("Statistical tests computed directly from the trade dataset.")

# ── Load ───────────────────────────────────────────────────────────────────
df = load_final_dataset()
if df.empty:
    st.stop()

ALPHA = 0.05

_CHART_LAYOUT = dict(
    template=PLOTLY_TEMPLATE,
    font=dict(family="Inter, system-ui, sans-serif", size=12),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=52, b=40, l=40, r=20),
)


def decision(p_val: float) -> str:
    return "✅ Reject H₀ (significant)" if p_val < ALPHA else "❌ Fail to Reject H₀"


def result_card(text: str, p_val: float) -> None:
    cls = "pt-pass" if p_val < ALPHA else "pt-fail"
    st.markdown(f'<div class="pt-result {cls}">{text}</div>', unsafe_allow_html=True)


def stat_card(label: str, value: str, note: str = "", sig: bool | None = None) -> str:
    note_cls  = "s-sig" if sig is True else ("s-nosig" if sig is False else "")
    note_html = f'<span class="s-note {note_cls}">({note})</span>' if note else ""
    return (
        f'<div class="pt-stat">'
        f'<div class="s-label">{label}</div>'
        f'<div class="s-value">{value}{note_html}</div>'
        f'</div>'
    )


# ── 1. Pearson Correlation ─────────────────────────────────────────────────
st.markdown('<p class="pt-section">1. Pearson Correlation Analysis</p>', unsafe_allow_html=True)
st.markdown(
    "Tests whether the Fear & Greed score (`value`) has a linear relationship "
    "with **Closed PnL** and **Size USD**."
)

corr_results = []
for target_col, label in [("Closed PnL", "value vs Closed PnL"),
                           ("Size USD",   "value vs Size USD")]:
    if "value" in df.columns and target_col in df.columns:
        clean = df[["value", target_col]].dropna()
        r, p  = stats.pearsonr(clean["value"], clean[target_col])
        interp = (
            "Strong positive"    if r > 0.5  else
            "Moderate positive"  if r > 0.3  else
            "Weak positive"      if r > 0    else
            "Weak negative"      if r > -0.3 else
            "Moderate negative"  if r > -0.5 else
            "Strong negative"
        ) + " correlation"
        corr_results.append({
            "Test": label, "Pearson r": round(r, 4),
            "P-Value": round(p, 6), "Decision": decision(p),
            "Interpretation": interp,
        })

if corr_results:
    st.dataframe(pd.DataFrame(corr_results), use_container_width=True, hide_index=True)

    col1, col2 = st.columns(2, gap="medium")
    for idx, (target_col, label) in enumerate([("Closed PnL", "value vs Closed PnL"),
                                                ("Size USD",   "value vs Size USD")]):
        if "value" in df.columns and target_col in df.columns:
            sample = df[["value", target_col]].dropna().sample(
                min(4000, len(df)), random_state=42
            )
            fig = px.scatter(
                sample, x="value", y=target_col,
                trendline="ols", title=label, opacity=0.3,
                color_discrete_sequence=["#2563EB"],
            )
            fig.update_traces(
                hovertemplate=f"Score: %{{x}}<br>{target_col}: %{{y:,.2f}}<extra></extra>"
            )
            fig.update_layout(**_CHART_LAYOUT, xaxis_title="Fear & Greed Score",
                              yaxis_title=target_col)
            (col1 if idx == 0 else col2).plotly_chart(fig, use_container_width=True)

    for row in corr_results:
        result_card(
            f"<strong>{row['Test']}</strong> — r = {row['Pearson r']}, "
            f"p = {row['P-Value']:.6f} → {row['Decision']} | {row['Interpretation']}",
            row["P-Value"],
        )
else:
    st.warning("Required columns (value, Closed PnL, Size USD) not found.")

# ── 2. One-Way ANOVA ───────────────────────────────────────────────────────
st.markdown('<p class="pt-section">2. One-Way ANOVA — Closed PnL vs Sentiment</p>',
            unsafe_allow_html=True)
st.markdown("H₀: All group means are equal.")

if "Closed PnL" in df.columns and "classification" in df.columns:
    groups_pnl = [
        df.loc[df["classification"] == s, "Closed PnL"].dropna().values
        for s in SENTIMENT_ORDER if s in df["classification"].values
    ]
    groups_pnl = [g for g in groups_pnl if len(g) > 1]

    if len(groups_pnl) >= 2:
        f_stat, p_anova = stats.f_oneway(*groups_pnl)

        col_a, col_b, col_c = st.columns(3)
        col_a.metric("F-Statistic", f"{f_stat:.4f}")
        col_b.metric("P-Value",     f"{p_anova:.6f}")
        col_c.metric("Decision",    "Significant ✅" if p_anova < ALPHA else "Not Significant ❌")

        fig_box = px.box(
            df[df["classification"].notna()],
            x="classification", y="Closed PnL",
            color="classification",
            category_orders={"classification": SENTIMENT_ORDER},
            title="Closed PnL Distribution by Sentiment",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig_box.update_layout(**_CHART_LAYOUT, showlegend=False,
                              xaxis_title="Sentiment", yaxis_title="Closed PnL (USD)")
        st.plotly_chart(fig_box, use_container_width=True)
        result_card(f"ANOVA: F = {f_stat:.4f}, p = {p_anova:.6f} → {decision(p_anova)}", p_anova)
    else:
        st.warning("Not enough sentiment groups for ANOVA.")
else:
    st.warning("Required columns not found.")

# ── 3. Kruskal-Wallis ──────────────────────────────────────────────────────
st.markdown('<p class="pt-section">3. Kruskal-Wallis Test</p>', unsafe_allow_html=True)
st.markdown("Non-parametric test for **Closed PnL** and **Size USD** across sentiment groups.")

kw_results = []
for target_col, label in [("Closed PnL", "PnL vs Sentiment"),
                           ("Size USD",   "Position Size vs Sentiment")]:
    if target_col in df.columns and "classification" in df.columns:
        groups = [
            df.loc[df["classification"] == s, target_col].dropna().values
            for s in SENTIMENT_ORDER if s in df["classification"].values
        ]
        groups = [g for g in groups if len(g) > 1]
        if len(groups) >= 2:
            h_stat, p_kw = stats.kruskal(*groups)
            kw_results.append({
                "Test": label, "H-Statistic": round(h_stat, 4),
                "P-Value": round(p_kw, 6), "Decision": decision(p_kw),
            })

if kw_results:
    st.dataframe(pd.DataFrame(kw_results), use_container_width=True, hide_index=True)
    for row in kw_results:
        result_card(
            f"<strong>Kruskal-Wallis — {row['Test']}</strong>: "
            f"H = {row['H-Statistic']}, p = {row['P-Value']:.6f} → {row['Decision']}",
            row["P-Value"],
        )
else:
    st.warning("Required columns not found for Kruskal-Wallis test.")

# ── 4. Chi-Square ──────────────────────────────────────────────────────────
st.markdown('<p class="pt-section">4. Chi-Square Test — Direction vs Sentiment</p>',
            unsafe_allow_html=True)
st.markdown("H₀: Trade direction and sentiment are independent.")

if "Direction" in df.columns and "classification" in df.columns:
    contingency = pd.crosstab(df["classification"], df["Direction"])
    chi2, p_chi2, dof, _ = stats.chi2_contingency(contingency)

    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("Chi² Statistic",       f"{chi2:.4f}")
    col_b.metric("P-Value",              f"{p_chi2:.6f}")
    col_c.metric("Degrees of Freedom",   f"{dof}")
    col_d.metric("Decision", "Significant ✅" if p_chi2 < ALPHA else "Not Significant ❌")

    st.markdown("**Contingency Table (observed counts):**")
    st.dataframe(contingency, use_container_width=True)

    fig_heat = px.imshow(
        contingency, text_auto=True,
        title="Direction vs Sentiment — Contingency Heatmap",
        color_continuous_scale="Blues",
    )
    fig_heat.update_layout(**_CHART_LAYOUT)
    st.plotly_chart(fig_heat, use_container_width=True)
    result_card(
        f"Chi-Square: χ² = {chi2:.4f}, df = {dof}, p = {p_chi2:.6f} → {decision(p_chi2)}",
        p_chi2,
    )
else:
    st.warning("Required columns (Direction, classification) not found.")

# ── 5. Effect Size Analysis ────────────────────────────────────────────────
st.markdown('<p class="pt-section">5. Effect Size Analysis</p>', unsafe_allow_html=True)
st.markdown("Quantifies **practical significance** independent of sample size.")

effect_results = []

# Eta Squared
if "Closed PnL" in df.columns and "classification" in df.columns:
    gp = [df.loc[df["classification"] == s, "Closed PnL"].dropna().values
          for s in SENTIMENT_ORDER if s in df["classification"].values]
    gp = [g for g in gp if len(g) > 1]
    if len(gp) >= 2:
        f_s, _ = stats.f_oneway(*gp)
        k, n   = len(gp), sum(len(g) for g in gp)
        eta_sq = max(0.0, min(1.0, (f_s * (k-1)) / (f_s * (k-1) + (n-k))))
        interp = ("Negligible" if eta_sq < 0.01 else "Small" if eta_sq < 0.06
                  else "Medium" if eta_sq < 0.14 else "Large")
        effect_results.append({"Measure": "Eta Squared (η²)",
                                "Variable": "Closed PnL vs Sentiment",
                                "Value": round(eta_sq, 6), "Interpretation": interp})

# Epsilon Squared
for target_col, label in [("Closed PnL", "PnL vs Sentiment"),
                           ("Size USD",   "Size USD vs Sentiment")]:
    if target_col in df.columns and "classification" in df.columns:
        gp = [df.loc[df["classification"] == s, target_col].dropna().values
              for s in SENTIMENT_ORDER if s in df["classification"].values]
        gp = [g for g in gp if len(g) > 1]
        if len(gp) >= 2:
            h_s, _ = stats.kruskal(*gp)
            n, k   = sum(len(g) for g in gp), len(gp)
            eps_sq = max(0.0, min(1.0, (h_s - k + 1) / (n - k)))
            interp = ("Negligible" if eps_sq < 0.01 else "Small" if eps_sq < 0.06
                      else "Medium" if eps_sq < 0.14 else "Large")
            effect_results.append({"Measure": "Epsilon Squared (ε²)",
                                   "Variable": label,
                                   "Value": round(eps_sq, 6), "Interpretation": interp})

# Cramer's V
if "Direction" in df.columns and "classification" in df.columns:
    ct = pd.crosstab(df["classification"], df["Direction"])
    chi2_v, _, _, _ = stats.chi2_contingency(ct)
    n_v, k_v = ct.values.sum(), min(ct.shape) - 1
    v = min(1.0, np.sqrt(chi2_v / (n_v * k_v)) if (n_v * k_v) > 0 else 0.0)
    interp = ("Negligible" if v < 0.1 else "Small" if v < 0.3
              else "Medium" if v < 0.5 else "Large")
    effect_results.append({"Measure": "Cramer's V", "Variable": "Direction vs Sentiment",
                            "Value": round(v, 6), "Interpretation": interp})

if effect_results:
    eff_df = pd.DataFrame(effect_results)
    st.dataframe(eff_df, use_container_width=True, hide_index=True)

    fig_eff = px.bar(
        eff_df, x="Variable", y="Value", color="Interpretation",
        title="Effect Size Summary", text="Value",
        color_discrete_map={
            "Negligible": "#94a3b8", "Small": "#f97316",
            "Medium": "#2563EB",    "Large": "#22c55e",
        },
    )
    fig_eff.update_traces(
        texttemplate="%{text:.4f}", textposition="outside", marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Effect Size: %{y:.4f}<extra></extra>",
    )
    fig_eff.update_layout(**_CHART_LAYOUT, xaxis_title="", yaxis_title="Effect Size Value")
    st.plotly_chart(fig_eff, use_container_width=True)

    st.markdown("**Effect Size Interpretation Guide:**")
    guide_cols = st.columns(4)
    for col, (lbl, threshold, color) in zip(guide_cols, [
        ("Negligible", "< 0.01",    "#94a3b8"),
        ("Small",      "0.01–0.06", "#f97316"),
        ("Medium",     "0.06–0.14", "#2563EB"),
        ("Large",      "> 0.14",    "#22c55e"),
    ]):
        col.markdown(
            f'<div class="pt-stat" style="text-align:center;border-color:{color};">'
            f'<div class="s-value" style="color:{color};">{lbl}</div>'
            f'<div class="s-label">{threshold}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
else:
    st.warning("Could not compute effect sizes — check required columns.")

# ── Summary ────────────────────────────────────────────────────────────────
st.markdown('<p class="pt-section">📋 Statistical Summary</p>', unsafe_allow_html=True)

all_tests  = (corr_results or []) + (kw_results or [])
sig_count  = sum(1 for t in all_tests if t.get("P-Value", 1) < ALPHA)
total_count = len(all_tests)

st.markdown(
    f'<div class="pt-result pt-neutral">'
    f'<strong>Overall:</strong> {sig_count} of {total_count} tests returned statistically '
    f'significant results (α = {ALPHA}). '
    f'{"Sentiment has a measurable impact on trader behaviour." if sig_count > 0 else "No significant effects detected."}'
    f'</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="pt-footer">PrimeTrade.ai · Hypothesis Testing</div>',
    unsafe_allow_html=True,
)
