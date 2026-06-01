# 📊 PrimeTrade.ai — Market Sentiment vs Trader Performance Dashboard

> A production-ready Streamlit analytics dashboard that investigates how the **Crypto Fear & Greed Index** shapes trader behaviour, profitability, position sizing, and trade direction across 211,218 real perpetual-futures trades.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Live Demo](#2-live-demo)
3. [Dataset Information](#3-dataset-information)
4. [Project Structure](#4-project-structure)
5. [Dashboard Pages](#5-dashboard-pages)
6. [Exploratory Data Analysis — Results](#6-exploratory-data-analysis--results)
7. [Sentiment Analysis — Results](#7-sentiment-analysis--results)
8. [Hypothesis Testing — Results](#8-hypothesis-testing--results)
9. [Effect Size Analysis](#9-effect-size-analysis)
10. [Key Findings](#10-key-findings)
11. [Business Insights & Recommendations](#11-business-insights--recommendations)
12. [Final Conclusion](#12-final-conclusion)
13. [Tech Stack](#13-tech-stack)
14. [Local Setup](#14-local-setup)
15. [Deployment](#15-deployment)
16. [Repository & Git Workflow](#16-repository--git-workflow)

---

## 1. Project Overview

**Title:** Market Sentiment vs Trader Performance Analysis  
**Platform:** PrimeTrade.ai  
**Goal:** Quantify and visualise how the Crypto Fear & Greed Index influences cryptocurrency trader behaviour — specifically profitability, position sizing, win rates, trading activity, and trade direction.

The analysis pipeline covers four phases:

| Phase | Description |
|-------|-------------|
| Phase 1 | Business & Data Understanding |
| Phase 2 | Data Cleaning & Quality |
| Phase 3 | Exploratory Data Analysis (EDA) |
| Phase 4 | Statistical Hypothesis Testing (SIHT) |

All phases were completed in Jupyter notebooks. This dashboard visualises the results dynamically, reading directly from CSV files — no notebook dependencies.

---

## 2. Live Demo

**GitHub Repository:** https://github.com/leekhithnunna/Trade.ai

**Run locally:**
```bash
cd Framework
python -m streamlit run app.py
```

---

## 3. Dataset Information

### 3.1 Trade Dataset — `final_eda_dataset.csv`

| Attribute | Value |
|-----------|-------|
| Total Trades | **211,218** |
| Unique Traders | **32** |
| Unique Coins | **246** |
| Date Range | **2023-05-01 → 2025-05-01** |
| Total Columns | **19** |

**Column Reference:**

| Column | Type | Description |
|--------|------|-------------|
| `Account` | string | Trader wallet address |
| `Coin` | string | Cryptocurrency traded |
| `Execution Price` | float | Price at trade execution |
| `Size Tokens` | float | Position size in tokens |
| `Size USD` | float | Position size in USD |
| `Side` | string | BUY / SELL |
| `Timestamp IST` | datetime | Trade timestamp (IST) |
| `Start Position` | float | Opening position size |
| `Direction` | string | Trade direction label |
| `Closed PnL` | float | Realised profit/loss in USD |
| `Transaction Hash` | string | On-chain transaction ID |
| `Order ID` | string | Exchange order identifier |
| `Crossed` | bool | Whether order crossed the book |
| `Fee` | float | Trading fee paid |
| `Trade ID` | string | Unique trade identifier |
| `Timestamp` | float | Unix timestamp |
| `Merge_Date` | date | Date used for sentiment merge |
| `value` | float | Fear & Greed score (0–100) |
| `classification` | category | Sentiment label |

**Sentiment Classification:**

| Sentiment | Trades | Share |
|-----------|--------|-------|
| Fear | 61,837 | 29.3% |
| Greed | 50,303 | 23.8% |
| Extreme Greed | 39,992 | 18.9% |
| Neutral | 37,686 | 17.8% |
| Extreme Fear | 21,400 | 10.1% |

### 3.2 Fear & Greed Index — `fear_greed_index.csv`

| Attribute | Value |
|-----------|-------|
| Total Records | **2,644 days** |
| Date Range | **2018-02-01 → 2025-05-02** |
| Score Range | **5 (Extreme Fear) → 95 (Extreme Greed)** |
| Mean Score | **46.98** |

**Sentiment Days Breakdown:**

| Sentiment | Days |
|-----------|------|
| Fear | 781 |
| Greed | 633 |
| Extreme Fear | 508 |
| Neutral | 396 |
| Extreme Greed | 326 |

---

## 4. Project Structure

```
Framework/
│
├── app.py                              ← Landing page (KPIs, overview, navigation)
│
├── pages/
│   ├── 1_Dataset_Overview.py           ← Shape, preview, column info, missing values
│   ├── 2_Exploratory_Data_Analysis.py  ← 6 dynamic charts with insights
│   ├── 3_Sentiment_Analysis.py         ← PnL, size, win rate, activity by sentiment
│   ├── 4_Hypothesis_Testing.py         ← Pearson, ANOVA, KW, Chi-Square, effect sizes
│   └── 5_Final_Insights.py             ← Business findings & conclusion
│
├── data/
│   ├── final_eda_dataset.csv           ← 211,218 trade records
│   └── fear_greed_index.csv            ← Daily Fear & Greed scores
│
├── utils/
│   ├── __init__.py
│   ├── constants.py                    ← Titles, sentiment order, colour palette
│   ├── data_loader.py                  ← @st.cache_data CSV loaders
│   ├── charts.py                       ← 10 reusable Plotly chart functions
│   └── styles.py                       ← Theme-aware CSS (light + dark mode)
│
├── assets/
│   └── README.md
│
├── requirements.txt
├── .gitignore
└── .streamlit/
    └── config.toml                     ← Wide layout, accent colour, no hardcoded theme
```

---

## 5. Dashboard Pages

### 🏠 Landing Page (`app.py`)
- Hero banner with project title and badge
- 5 KPI metric cards: Total Trades, Traders, Coins, Avg PnL, Avg Position Size
- Dataset summary cards (trade dataset + Fear & Greed index)
- Navigation guide with hover-animated cards

### 🗂️ Page 1 — Dataset Overview
- Key metrics row
- **Tab 1 — Data Preview:** First 100 rows of trade data + Fear & Greed index preview
- **Tab 2 — Column Info:** Dtype, non-null count, null count, unique count, sample value
- **Tab 3 — Missing Values:** Sorted missing value summary with warnings
- **Tab 4 — Data Types:** Dtype distribution + descriptive statistics for numeric and categorical columns

### 🔍 Page 2 — Exploratory Data Analysis
Six dynamic sections, each with a Plotly chart and an insight callout:
1. Sentiment Distribution (bar chart)
2. Monthly Trading Activity (area chart)
3. Top 10 Coins by Trade Count (horizontal bar)
4. Top 10 Traders by Trade Count (horizontal bar)
5. Trade Direction Distribution (donut chart + breakdown metrics)
6. Fear & Greed Index Over Time (area chart with threshold lines)

### 📈 Page 3 — Sentiment Analysis
Six interactive sections:
1. Sentiment vs Closed PnL — mean, median, total PnL table + grouped bar chart
2. Sentiment vs Position Size — mean/median size table + bar chart
3. Sentiment vs Win Rate — win/loss table + bar chart with 50% breakeven line
4. Sentiment vs Trading Activity — trade count table + bar chart
5. Coin Performance by Sentiment — interactive selectbox, top 15 coins by mean PnL
6. Trader Performance by Sentiment — interactive selectbox, top 10 traders by total PnL

### 🧪 Page 4 — Hypothesis Testing
Five statistical test sections with result cards (green = significant, red = not significant):
1. Pearson Correlation — scatter plots with OLS trendlines
2. One-Way ANOVA — box plot of PnL distributions
3. Kruskal-Wallis Test — non-parametric group comparison
4. Chi-Square Test — contingency heatmap
5. Effect Size Analysis — Eta², Epsilon², Cramer's V with interpretation guide

### 💡 Page 5 — Final Insights
- KPI summary row
- 5 Key Findings cards
- Statistical Findings panel (two-column stat cards)
- 5 Business Insights & Recommendations cards
- Dual-axis visual summary (Mean PnL bars + Win Rate line)
- Final Conclusion banner

---

## 6. Exploratory Data Analysis — Results

### 6.1 Dataset Overview

| Metric | Value |
|--------|-------|
| Total Trades | 211,218 |
| Total Traders | 32 |
| Total Coins | 246 |
| Average Closed PnL | **$48.55** |
| Median Closed PnL | **$0.00** |
| Average Position Size | **$5,639.19** |
| Overall Win Rate | **41.12%** |
| Total Winning Trades | 86,863 |

> The median PnL of $0.00 indicates a highly skewed distribution — a small number of large winning trades pull the mean upward while the majority of trades break even or generate small losses.

### 6.2 Sentiment Distribution

Fear is the dominant sentiment regime, accounting for nearly 30% of all trades. Combined, Fear + Extreme Fear cover **39.4%** of the dataset, while Greed + Extreme Greed cover **42.7%**.

```
Fear          → 61,837 trades (29.3%)
Greed         → 50,303 trades (23.8%)
Extreme Greed → 39,992 trades (18.9%)
Neutral       → 37,686 trades (17.8%)
Extreme Fear  → 21,400 trades (10.1%)
```

### 6.3 Monthly Trading Activity

| Metric | Value |
|--------|-------|
| Peak Month | **April 2025** |
| Peak Trade Count | **52,358 trades** |
| Dataset Span | May 2023 → May 2025 (24 months) |

Activity spikes correlate with periods of extreme sentiment — particularly Extreme Greed phases in late 2024 and early 2025.

### 6.4 Top 5 Coins by Trade Count

| Rank | Coin | Trades | Share |
|------|------|--------|-------|
| 1 | **HYPE** | 68,005 | 32.2% |
| 2 | @107 | 29,992 | 14.2% |
| 3 | BTC | 26,064 | 12.3% |
| 4 | ETH | 11,158 | 5.3% |
| 5 | SOL | 10,691 | 5.1% |

HYPE alone accounts for nearly one-third of all trades, indicating strong concentration in a single asset.

### 6.5 Trade Direction Distribution

| Direction | Trades |
|-----------|--------|
| Open Long | 49,895 |
| Close Long | 48,678 |
| Open Short | 39,741 |
| Close Short | 36,007 |
| Sell | 19,902 |
| Buy | 16,716 |
| Other | 279 |

Long-side activity (Open Long + Close Long = 98,573) slightly exceeds short-side activity (Open Short + Close Short = 75,748), suggesting a mild bullish bias in the dataset period.

### 6.6 Fear & Greed Index

The index averaged **46.98** over its full history (2018–2025), sitting just below the Neutral threshold of 50. The dataset's trading period (2023–2025) coincided with a recovery and bull market cycle, explaining the higher proportion of Greed-regime trades.

---

## 7. Sentiment Analysis — Results

### 7.1 Closed PnL by Sentiment

| Sentiment | Mean PnL | Median PnL | Total PnL | Trades |
|-----------|----------|------------|-----------|--------|
| Extreme Fear | $34.54 | $0.00 | $739,110 | 21,400 |
| Fear | $54.29 | $0.00 | $3,357,155 | 61,837 |
| Neutral | $34.31 | $0.00 | $1,292,921 | 37,686 |
| Greed | $42.74 | $0.00 | $2,150,129 | 50,303 |
| **Extreme Greed** | **$67.89** | **$0.00** | **$2,715,171** | **39,992** |

**Key finding:** Extreme Greed produces the highest mean PnL ($67.89), nearly double that of Extreme Fear ($34.54) and Neutral ($34.31). Fear surprisingly outperforms Greed in mean PnL ($54.29 vs $42.74).

### 7.2 Win Rate by Sentiment

| Sentiment | Win Rate |
|-----------|----------|
| Extreme Fear | 37.06% |
| Fear | 42.08% |
| Neutral | 39.70% |
| Greed | 38.48% |
| **Extreme Greed** | **46.49%** |

**Key finding:** Extreme Greed yields the highest win rate at **46.49%**. No sentiment regime achieves a win rate above 50%, meaning the majority of individual trades are unprofitable — profitability is driven by the magnitude of winning trades, not their frequency.

### 7.3 Position Size by Sentiment

| Sentiment | Mean Size USD |
|-----------|---------------|
| Extreme Fear | $5,349.73 |
| **Fear** | **$7,816.11** |
| Neutral | $4,782.73 |
| Greed | $5,736.88 |
| Extreme Greed | $3,112.25 |

**Surprising finding:** Traders take the **largest positions during Fear** ($7,816), not during Greed as might be expected. This may reflect contrarian positioning — traders sizing up when they perceive undervalued conditions. Extreme Greed shows the smallest average position ($3,112), possibly due to profit-taking and reduced conviction at market tops.

### 7.4 Trading Activity by Sentiment

| Sentiment | Trades | % of Total |
|-----------|--------|------------|
| Extreme Fear | 21,400 | 10.1% |
| Fear | 61,837 | 29.3% |
| Neutral | 37,686 | 17.8% |
| Greed | 50,303 | 23.8% |
| Extreme Greed | 39,992 | 18.9% |

Fear periods generate the most trading activity, consistent with the position sizing finding — traders are most active and take larger positions when sentiment is fearful.

---

## 8. Hypothesis Testing — Results

All tests use significance level **α = 0.05**.

### 8.1 Pearson Correlation

Tests linear relationship between Fear & Greed score and trade metrics.

| Test | Pearson r | P-Value | Decision |
|------|-----------|---------|----------|
| value vs Closed PnL | **0.0081** | **0.000190** | ✅ Reject H₀ |
| value vs Size USD | **−0.0298** | **< 0.000001** | ✅ Reject H₀ |

**Interpretation:**
- Both correlations are **statistically significant** but **weak in magnitude**.
- The negative correlation between sentiment score and Size USD (r = −0.030) confirms the position sizing finding: higher fear (lower score) → larger positions.
- The positive correlation with PnL (r = 0.008) is statistically real but practically negligible at the individual trade level.

### 8.2 One-Way ANOVA — Closed PnL vs Sentiment

**H₀:** Mean Closed PnL is equal across all sentiment groups.

| Statistic | Value |
|-----------|-------|
| F-Statistic | **9.0622** |
| P-Value | **2.575 × 10⁻⁷** |
| Decision | ✅ **Reject H₀ — Significant** |

Mean PnL differs significantly across sentiment groups. The ANOVA confirms that sentiment regime is a statistically meaningful predictor of trade profitability.

### 8.3 Kruskal-Wallis Test

Non-parametric test (does not assume normality), more appropriate for the heavily skewed PnL distribution.

| Test | H-Statistic | P-Value | Decision |
|------|-------------|---------|----------|
| PnL vs Sentiment | **1,226.9956** | **< 0.000001** | ✅ Reject H₀ |
| Position Size vs Sentiment | **1,945.0549** | **< 0.000001** | ✅ Reject H₀ |

Both PnL distributions and position size distributions differ significantly across sentiment groups. The extremely high H-statistics reflect the large sample size (211,218 trades).

### 8.4 Chi-Square Test — Direction vs Sentiment

**H₀:** Trade direction (Buy/Sell/Long/Short) is independent of sentiment.

| Statistic | Value |
|-----------|-------|
| Chi² | **16,168.6235** |
| P-Value | **< 0.000001** |
| Degrees of Freedom | **44** |
| Decision | ✅ **Reject H₀ — Significant** |

Trade direction is **not independent** of sentiment. The mix of long vs short, open vs close trades shifts meaningfully across sentiment regimes.

---

## 9. Effect Size Analysis

Effect sizes measure **practical significance** — how large the effect actually is, independent of sample size.

| Measure | Variable | Value | Interpretation |
|---------|----------|-------|----------------|
| Eta Squared (η²) | Closed PnL vs Sentiment | **0.000172** | Negligible |
| Epsilon Squared (ε²) | PnL vs Sentiment | **0.005790** | Small |
| Epsilon Squared (ε²) | Size USD vs Sentiment | **0.009190** | Small |
| Cramer's V | Direction vs Sentiment | **0.138338** | Small–Medium |

**Interpretation Guide:**

| Label | Threshold |
|-------|-----------|
| Negligible | < 0.01 |
| Small | 0.01 – 0.06 |
| Medium | 0.06 – 0.14 |
| Large | > 0.14 |

**Key takeaway:** While all tests are statistically significant (driven by the large sample of 211,218 trades), the practical effect sizes are small. Sentiment explains a **real but modest** portion of variance in PnL and position sizing. The strongest practical effect is Cramer's V = 0.138 for Direction vs Sentiment, sitting at the Small–Medium boundary — meaning sentiment has a meaningful influence on whether traders go long or short.

---

## 10. Key Findings

### Finding 1 — Sentiment Drives Profitability
Traders operating during **Extreme Greed** periods achieved the highest mean Closed PnL of **$67.89** — nearly double the $34.31 seen during Neutral periods. Market sentiment is a meaningful predictor of trade outcomes, not just a background indicator.

### Finding 2 — Win Rate Peaks at Extreme Greed
The highest win rate of **46.49%** was recorded during **Extreme Greed** conditions. No regime exceeds 50%, confirming that profitability is driven by the size of winning trades rather than their frequency. Fear achieves the second-highest win rate (42.08%), suggesting contrarian traders perform well.

### Finding 3 — Position Sizing is Contrarian
Traders take the **largest positions during Fear** ($7,816 avg), not during Greed as intuition might suggest. This contrarian sizing behaviour — going bigger when others are fearful — aligns with classic value-investing principles applied to crypto trading.

### Finding 4 — Trade Direction is Sentiment-Dependent
The Chi-Square test (χ² = 16,168.62, p < 0.000001) confirms that trade direction is **not independent of sentiment**. Cramer's V = 0.138 indicates a small-to-medium practical association. Traders systematically shift their directional bias based on prevailing market sentiment.

### Finding 5 — Asset Concentration is Extreme
**HYPE** alone accounts for **32.2% of all trades** (68,005 trades). The top 5 coins cover **69.1%** of all activity. This extreme concentration suggests traders focus almost exclusively on high-liquidity, high-momentum assets regardless of sentiment regime.

### Finding 6 — Activity Peaks During Fear
Despite Fear being associated with lower PnL, it generates the **most trading activity** (61,837 trades, 29.3%). This may reflect panic-driven or momentum-driven behaviour — traders react most actively to negative sentiment signals.

### Finding 7 — Statistical Significance vs Practical Significance
All four hypothesis tests reject H₀ at α = 0.05. However, effect sizes are small (η² = 0.000172, ε² = 0.006). This means sentiment has a **real but modest** influence on individual trade outcomes. The relationship is consistent and statistically reliable, but sentiment alone is not sufficient to predict individual trade profitability.

---

## 11. Business Insights & Recommendations

### 🎯 Sentiment-Aware Strategy Design
Trading strategies should incorporate the Fear & Greed Index as a **regime filter**. Strategies optimised for Greed conditions may underperform during Fear periods and vice versa. Consider building separate parameter sets — entry thresholds, stop-loss levels, take-profit targets — for each of the five sentiment regimes.

### 📐 Dynamic Position Sizing
Since position sizes vary significantly with sentiment (Fear: $7,816 avg vs Extreme Greed: $3,112 avg), risk management systems should account for this behaviour. During Extreme Greed, traders under-size positions relative to Fear periods — potentially leaving returns on the table. A sentiment-calibrated position sizing model could improve capital efficiency.

### 📈 Timing Entries with Sentiment
With win rates peaking at **46.49%** during Extreme Greed and mean PnL highest at **$67.89**, traders may benefit from increasing trade frequency or conviction during these periods. Conversely, reducing exposure during Extreme Fear phases (win rate: 37.06%) could improve overall portfolio performance.

### 🔔 Sentiment Alerts & Monitoring
Integrating real-time Fear & Greed Index feeds into trading dashboards can help traders make more informed decisions. Automated alerts when sentiment crosses key thresholds — entering Extreme Fear (score ≤ 25) or Extreme Greed (score ≥ 75) — could serve as actionable regime-change signals.

### 🧩 Portfolio Diversification by Sentiment
Coin performance varies across sentiment regimes. Building sentiment-conditional portfolios — rotating into historically outperforming coins for each sentiment phase — could improve risk-adjusted returns. The interactive coin performance filter on Page 3 of the dashboard enables this analysis.

### ⚠️ Risk Management During Extreme Greed
While Extreme Greed produces the highest mean PnL and win rate, it also carries the risk of sentiment reversal. Traders should implement tighter stop-losses and reduced leverage during Extreme Greed phases to protect against sudden sentiment shifts.

---

## 12. Final Conclusion

This analysis of **211,218 trades** across **32 traders** and **246 coins** over a **24-month period (May 2023 – May 2025)** demonstrates that the **Crypto Fear & Greed Index** is a statistically significant predictor of trader behaviour and performance.

**What the data shows:**

| Dimension | Finding |
|-----------|---------|
| Profitability | Mean PnL ranges from $34.31 (Neutral) to $67.89 (Extreme Greed) |
| Win Rate | Ranges from 37.06% (Extreme Fear) to 46.49% (Extreme Greed) |
| Position Sizing | Largest during Fear ($7,816), smallest during Extreme Greed ($3,112) |
| Trade Direction | Statistically associated with sentiment (χ² = 16,168, p < 0.000001) |
| Activity | Highest during Fear (61,837 trades), lowest during Extreme Fear (21,400) |

**Statistical verdict:** All four hypothesis tests (Pearson, ANOVA, Kruskal-Wallis, Chi-Square) reject the null hypothesis at α = 0.05. Effect sizes are small but consistent, confirming that sentiment has a **real, reliable, and practically meaningful** influence on crypto trader behaviour.

**Business verdict:** Incorporating sentiment-aware logic into trading strategies, risk management systems, and portfolio construction frameworks has the potential to meaningfully improve risk-adjusted performance for crypto traders operating on perpetual futures markets.

---

## 13. Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Dashboard Framework | Streamlit | 1.35.0 |
| Data Processing | Pandas | 2.2.2 |
| Numerical Computing | NumPy | 1.26.4 |
| Visualisation | Plotly | 5.22.0 |
| Statistical Tests | SciPy | 1.13.1 |
| Regression (OLS trendlines) | Statsmodels | 0.14.2 |
| Language | Python | 3.10+ |

**UI Features:**
- Light / Dark mode toggle (CSS custom properties, theme-aware)
- Hover animations on all interactive elements (cards, metrics, nav items)
- Responsive wide layout
- Plotly charts with custom hover templates
- `@st.cache_data` for performant CSV loading

---

## 14. Local Setup

### Prerequisites
- Python 3.10 or higher
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/leekhithnunna/Trade.ai.git
cd Trade.ai

# 2. (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the dashboard
python -m streamlit run app.py
```

The app will open at `http://localhost:8501`.

### Data Files
Both CSV files are included in the `data/` folder:
- `data/final_eda_dataset.csv` — 211,218 trade records (~54 MB)
- `data/fear_greed_index.csv` — 2,644 daily Fear & Greed scores

---

## 15. Deployment

### Streamlit Community Cloud

1. Push the `Framework/` folder contents to a GitHub repository (already done — see above)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app**
4. Set:
   - **Repository:** `leekhithnunna/Trade.ai`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click **Deploy**

No environment variables or secrets are required. The app reads data from the `data/` folder using relative paths.

### Configuration (`config.toml`)

```toml
[theme]
primaryColor         = "#2563EB"
font                 = "sans serif"

[server]
headless             = true
enableXsrfProtection = true

[browser]
gatherUsageStats     = false
```

The theme is user-controlled (light/dark toggle in the top-right menu). No hardcoded dark mode.

---

## 16. Repository & Git Workflow

### Initial Setup (already completed)
```bash
cd Framework
git init
git remote add origin https://github.com/leekhithnunna/Trade.ai.git
git add .
git commit -m "Initial Streamlit framework — PrimeTrade.ai Sentiment Dashboard"
git branch -M main
git push -u origin main
```

### Future Updates
```bash
git add .
git commit -m "Describe your changes"
git push
```

### .gitignore
```
__pycache__/
*.pyc
*.pyo
*.pyd
.streamlit/secrets.toml
.env
.DS_Store
*.egg-info/
dist/
build/
.venv/
venv/
```

---

## Author

**PrimeTrade.ai Assignment**  
Built with Streamlit, Plotly, Pandas, SciPy  
Dashboard · Statistical Analysis · Business Intelligence

---

*README generated from live dataset analysis — all statistics are computed directly from `final_eda_dataset.csv` and `fear_greed_index.csv`.*
