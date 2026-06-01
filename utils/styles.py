# ============================================================
# styles.py — Theme-aware CSS injected on every page
# ============================================================
# Uses CSS custom properties so a single inject_css() call
# handles both Streamlit light mode and dark mode without
# any Python-side branching.  The [data-theme] attribute on
# <html> is set by Streamlit itself when the user toggles the
# theme in the top-right menu.
# ============================================================

import streamlit as st


def inject_css() -> None:
    """Inject global theme-aware CSS into the current page."""
    st.markdown(_CSS, unsafe_allow_html=True)


_CSS = """
<style>
/* ── CSS custom properties (light defaults) ─────────────────────────── */
:root {
  --pt-bg:           #f8fafc;
  --pt-surface:      #ffffff;
  --pt-surface-2:    #f1f5f9;
  --pt-border:       #e2e8f0;
  --pt-border-hover: #2563EB;
  --pt-text:         #0f172a;
  --pt-text-muted:   #64748b;
  --pt-accent:       #2563EB;
  --pt-accent-soft:  #dbeafe;
  --pt-green:        #16a34a;
  --pt-red:          #dc2626;
  --pt-amber:        #d97706;
  --pt-shadow:       0 2px 8px rgba(0,0,0,0.08);
  --pt-shadow-hover: 0 6px 20px rgba(37,99,235,0.18);
  --pt-radius:       10px;
  --pt-transition:   all 0.22s cubic-bezier(0.4,0,0.2,1);
}

/* ── Dark-mode overrides ─────────────────────────────────────────────── */
[data-theme="dark"] {
  --pt-bg:           #0f172a;
  --pt-surface:      #1e293b;
  --pt-surface-2:    #0f172a;
  --pt-border:       #334155;
  --pt-border-hover: #3b82f6;
  --pt-text:         #f1f5f9;
  --pt-text-muted:   #94a3b8;
  --pt-accent:       #3b82f6;
  --pt-accent-soft:  #1e3a5f;
  --pt-green:        #22c55e;
  --pt-red:          #f87171;
  --pt-amber:        #fbbf24;
  --pt-shadow:       0 2px 8px rgba(0,0,0,0.4);
  --pt-shadow-hover: 0 6px 20px rgba(59,130,246,0.3);
}

/* ── Global resets ───────────────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {
  background-color: var(--pt-bg) !important;
}

/* ── Sidebar ─────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: var(--pt-surface) !important;
  border-right: 1px solid var(--pt-border) !important;
}
[data-testid="stSidebar"] * { color: var(--pt-text) !important; }

/* ── Metric cards ────────────────────────────────────────────────────── */
div[data-testid="metric-container"] {
  background:    var(--pt-surface) !important;
  border:        1px solid var(--pt-border) !important;
  border-radius: var(--pt-radius) !important;
  padding:       1rem 1.2rem !important;
  box-shadow:    var(--pt-shadow);
  transition:    var(--pt-transition);
}
div[data-testid="metric-container"]:hover {
  border-color: var(--pt-border-hover) !important;
  box-shadow:   var(--pt-shadow-hover);
  transform:    translateY(-2px);
}
div[data-testid="metric-container"] label {
  color: var(--pt-text-muted) !important;
  font-size: 0.78rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.04em !important;
  text-transform: uppercase !important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
  color: var(--pt-text) !important;
  font-size: 1.6rem !important;
  font-weight: 700 !important;
}

/* ── Hero banner ─────────────────────────────────────────────────────── */
.pt-hero {
  background: linear-gradient(135deg, var(--pt-surface) 0%, var(--pt-surface-2) 100%);
  border: 1px solid var(--pt-border);
  border-top: 4px solid var(--pt-accent);
  border-radius: var(--pt-radius);
  padding: 2.8rem 2.4rem 2.2rem;
  text-align: center;
  margin-bottom: 1.8rem;
  box-shadow: var(--pt-shadow);
  transition: var(--pt-transition);
}
.pt-hero:hover {
  box-shadow: var(--pt-shadow-hover);
}
.pt-hero-title {
  font-size: 2.6rem;
  font-weight: 800;
  color: var(--pt-accent);
  margin: 0;
  letter-spacing: 1px;
}
.pt-hero-sub {
  font-size: 1.1rem;
  color: var(--pt-text-muted);
  margin-top: 0.5rem;
  font-weight: 400;
}
.pt-hero-badge {
  display: inline-block;
  background: var(--pt-accent-soft);
  color: var(--pt-accent);
  border-radius: 20px;
  padding: 0.2rem 0.9rem;
  font-size: 0.78rem;
  font-weight: 600;
  margin-top: 0.8rem;
  letter-spacing: 0.05em;
}

/* ── Section headers ─────────────────────────────────────────────────── */
.pt-section {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--pt-accent);
  border-left: 3px solid var(--pt-accent);
  padding: 0.3rem 0 0.3rem 0.75rem;
  margin: 1.8rem 0 0.9rem;
  letter-spacing: 0.01em;
}

/* ── Insight / info boxes ────────────────────────────────────────────── */
.pt-insight {
  background: var(--pt-surface);
  border: 1px solid var(--pt-border);
  border-left: 3px solid var(--pt-accent);
  border-radius: var(--pt-radius);
  padding: 0.85rem 1.1rem;
  margin-top: 0.6rem;
  font-size: 0.9rem;
  color: var(--pt-text-muted);
  line-height: 1.6;
  transition: var(--pt-transition);
}
.pt-insight:hover {
  border-left-color: var(--pt-amber);
  box-shadow: var(--pt-shadow);
}
.pt-insight strong { color: var(--pt-text); }

/* ── Navigation cards ────────────────────────────────────────────────── */
.pt-nav-card {
  background: var(--pt-surface);
  border: 1px solid var(--pt-border);
  border-radius: var(--pt-radius);
  padding: 0.9rem 1.1rem;
  margin-bottom: 0.55rem;
  cursor: pointer;
  transition: var(--pt-transition);
  display: flex;
  align-items: center;
  gap: 0.6rem;
}
.pt-nav-card:hover {
  border-color: var(--pt-border-hover);
  background: var(--pt-accent-soft);
  box-shadow: var(--pt-shadow-hover);
  transform: translateX(4px);
}
.pt-nav-card .nav-icon { font-size: 1.3rem; }
.pt-nav-card .nav-title {
  font-weight: 700;
  color: var(--pt-text);
  font-size: 0.95rem;
}
.pt-nav-card .nav-desc {
  color: var(--pt-text-muted);
  font-size: 0.82rem;
  margin-top: 0.1rem;
}

/* ── Finding / insight cards ─────────────────────────────────────────── */
.pt-card {
  background: var(--pt-surface);
  border: 1px solid var(--pt-border);
  border-radius: var(--pt-radius);
  padding: 1.1rem 1.3rem;
  margin-bottom: 0.75rem;
  transition: var(--pt-transition);
  box-shadow: var(--pt-shadow);
}
.pt-card:hover {
  border-color: var(--pt-border-hover);
  box-shadow: var(--pt-shadow-hover);
  transform: translateY(-2px);
}
.pt-card h4 {
  color: var(--pt-accent);
  margin: 0 0 0.45rem;
  font-size: 0.97rem;
  font-weight: 700;
}
.pt-card p {
  color: var(--pt-text-muted);
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.6;
}

/* ── Stat cards (hypothesis page) ───────────────────────────────────── */
.pt-stat {
  background: var(--pt-surface-2);
  border: 1px solid var(--pt-border);
  border-radius: var(--pt-radius);
  padding: 0.85rem 1.1rem;
  margin-bottom: 0.55rem;
  transition: var(--pt-transition);
}
.pt-stat:hover {
  border-color: var(--pt-border-hover);
  box-shadow: var(--pt-shadow);
}
.pt-stat .s-label {
  color: var(--pt-text-muted);
  font-size: 0.78rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.pt-stat .s-value {
  color: var(--pt-text);
  font-size: 1.05rem;
  font-weight: 700;
  margin-top: 0.15rem;
}
.pt-stat .s-note {
  font-size: 0.78rem;
  font-weight: 600;
  margin-left: 0.4rem;
}
.s-sig   { color: var(--pt-green); }
.s-nosig { color: var(--pt-red);   }

/* ── Result cards (pass/fail) ────────────────────────────────────────── */
.pt-result {
  border-radius: var(--pt-radius);
  padding: 0.9rem 1.1rem;
  margin: 0.4rem 0;
  font-size: 0.9rem;
  transition: var(--pt-transition);
}
.pt-result:hover { transform: translateX(3px); }
.pt-pass {
  background: color-mix(in srgb, var(--pt-green) 10%, var(--pt-surface));
  border: 1px solid var(--pt-green);
  color: var(--pt-green);
}
.pt-fail {
  background: color-mix(in srgb, var(--pt-red) 10%, var(--pt-surface));
  border: 1px solid var(--pt-red);
  color: var(--pt-red);
}
.pt-neutral {
  background: var(--pt-surface);
  border: 1px solid var(--pt-border);
  color: var(--pt-text-muted);
}

/* ── Conclusion banner ───────────────────────────────────────────────── */
.pt-conclusion {
  background: linear-gradient(135deg, var(--pt-surface) 0%, var(--pt-surface-2) 100%);
  border: 1px solid var(--pt-border);
  border-top: 4px solid var(--pt-accent);
  border-radius: var(--pt-radius);
  padding: 2.2rem 2rem;
  margin-top: 1.8rem;
  text-align: center;
  box-shadow: var(--pt-shadow);
  transition: var(--pt-transition);
}
.pt-conclusion:hover { box-shadow: var(--pt-shadow-hover); }
.pt-conclusion h2 {
  color: var(--pt-accent);
  margin-bottom: 0.8rem;
  font-size: 1.5rem;
}
.pt-conclusion p {
  color: var(--pt-text-muted);
  font-size: 0.95rem;
  line-height: 1.7;
  max-width: 820px;
  margin: 0.5rem auto;
}
.pt-conclusion strong { color: var(--pt-text); }

/* ── Dataset summary cards ───────────────────────────────────────────── */
.pt-ds-card {
  background: var(--pt-surface);
  border: 1px solid var(--pt-border);
  border-radius: var(--pt-radius);
  padding: 1.2rem 1.4rem;
  height: 100%;
  transition: var(--pt-transition);
  box-shadow: var(--pt-shadow);
}
.pt-ds-card:hover {
  border-color: var(--pt-border-hover);
  box-shadow: var(--pt-shadow-hover);
}
.pt-ds-card h4 {
  color: var(--pt-accent);
  font-size: 0.9rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 0 0 0.8rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--pt-border);
}
.pt-ds-card .ds-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.3rem 0;
  border-bottom: 1px solid var(--pt-border);
  font-size: 0.88rem;
}
.pt-ds-card .ds-row:last-child { border-bottom: none; }
.pt-ds-card .ds-label { color: var(--pt-text-muted); }
.pt-ds-card .ds-val   { color: var(--pt-text); font-weight: 600; }

/* ── Sentiment badge pills ───────────────────────────────────────────── */
.badge-ef  { background:#fde8e8; color:#b91c1c; border-radius:12px; padding:2px 10px; font-size:0.78rem; font-weight:600; }
.badge-f   { background:#fef3c7; color:#92400e; border-radius:12px; padding:2px 10px; font-size:0.78rem; font-weight:600; }
.badge-n   { background:#f0fdf4; color:#166534; border-radius:12px; padding:2px 10px; font-size:0.78rem; font-weight:600; }
.badge-g   { background:#dcfce7; color:#15803d; border-radius:12px; padding:2px 10px; font-size:0.78rem; font-weight:600; }
.badge-eg  { background:#dbeafe; color:#1d4ed8; border-radius:12px; padding:2px 10px; font-size:0.78rem; font-weight:600; }

/* ── Streamlit tab styling ───────────────────────────────────────────── */
button[data-baseweb="tab"] {
  font-weight: 600 !important;
  font-size: 0.88rem !important;
  transition: var(--pt-transition) !important;
}
button[data-baseweb="tab"]:hover {
  color: var(--pt-accent) !important;
}

/* ── Streamlit selectbox / inputs ────────────────────────────────────── */
div[data-baseweb="select"] > div {
  border-color: var(--pt-border) !important;
  border-radius: var(--pt-radius) !important;
  transition: var(--pt-transition) !important;
}
div[data-baseweb="select"] > div:hover {
  border-color: var(--pt-border-hover) !important;
}

/* ── Divider ─────────────────────────────────────────────────────────── */
hr { border-color: var(--pt-border) !important; margin: 1.5rem 0 !important; }

/* ── Footer caption ──────────────────────────────────────────────────── */
.pt-footer {
  text-align: center;
  color: var(--pt-text-muted);
  font-size: 0.8rem;
  padding: 1.2rem 0 0.5rem;
  border-top: 1px solid var(--pt-border);
  margin-top: 2rem;
}
</style>
"""
