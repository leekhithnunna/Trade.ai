# ============================================================
# constants.py — App-wide constants for PrimeTrade Dashboard
# ============================================================

PAGE_TITLE = "PrimeTrade.ai — Market Sentiment Dashboard"
PAGE_ICON  = "📊"
APP_NAME   = "PrimeTrade.ai"
PROJECT_DESCRIPTION = (
    "This dashboard explores how the **Crypto Fear & Greed Index** influences "
    "trader behaviour, profitability, position sizing, and trade direction across "
    "**211 000+ trades**, **32 traders**, and **246 coins**. "
    "Navigate through the pages to explore the data, run statistical tests, "
    "and read the final business insights."
)

# Ordered sentiment categories (low → high)
SENTIMENT_ORDER = ["Extreme Fear", "Fear", "Neutral", "Greed", "Extreme Greed"]

# Colour palette aligned to sentiment (red → green)
SENTIMENT_COLORS = {
    "Extreme Fear": "#ef4444",
    "Fear":         "#f97316",
    "Neutral":      "#eab308",
    "Greed":        "#22c55e",
    "Extreme Greed":"#2563EB",
}

# Plotly template — single source of truth used by charts.py
# "plotly_white" renders cleanly in both light and dark Streamlit themes
# because Streamlit wraps charts in an iframe that inherits the page bg.
PLOTLY_TEMPLATE = "plotly_white"
