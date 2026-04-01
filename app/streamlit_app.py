from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.decision import decide_actions
from src.metrics import compute_summary, provider_breakdown


# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Payment Decision Engine",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Global CSS injection ──────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

    :root {
        --bg-base:      #070c18;
        --bg-surface:   #0d1626;
        --bg-card:      #111d35;
        --border:       #1e2f50;
        --accent:       #0a84ff;
        --accent-soft:  #0a84ff1a;
        --accent-text:  #4da6ff;
        --success:      #00c896;
        --warning:      #f5a623;
        --text-primary: #e8edf7;
        --text-muted:   #6b7fa3;
        --text-label:   #8c9dc0;
    }

    html, body, [class*="css"] {
        font-family: 'DM Mono', monospace;
        background-color: var(--bg-base) !important;
        color: var(--text-primary) !important;
    }

    .stApp {
        background: var(--bg-base);
        background-image: radial-gradient(ellipse 80% 50% at 50% -20%, #0a84ff14 0%, transparent 70%);
    }

    #MainMenu, footer, header { visibility: hidden; }
    .block-container {
        padding: 2.5rem 3rem 4rem !important;
        max-width: 1600px !important;
    }

    .page-header {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        border-bottom: 1px solid var(--border);
        padding-bottom: 1.5rem;
        margin-bottom: 2.5rem;
    }
    .page-header-left { display: flex; flex-direction: column; gap: 0.4rem; }
    .page-title {
        font-family: 'Syne', sans-serif;
        font-size: 1.75rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: var(--text-primary);
        margin: 0;
        line-height: 1;
    }
    .page-title span { color: var(--accent-text); }
    .page-caption {
        font-size: 0.78rem;
        color: var(--text-muted);
        letter-spacing: 0.04em;
        font-weight: 300;
        margin: 0;
    }
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        background: var(--accent-soft);
        border: 1px solid var(--accent);
        border-radius: 4px;
        padding: 0.35rem 0.8rem;
        font-size: 0.72rem;
        font-weight: 500;
        color: var(--accent-text);
        letter-spacing: 0.06em;
        text-transform: uppercase;
        align-self: flex-start;
    }
    .status-dot {
        width: 6px; height: 6px;
        background: var(--success);
        border-radius: 50%;
        animation: pulse 2s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }

    .section-heading {
        font-family: 'Syne', sans-serif;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--text-muted);
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    .section-heading::after {
        content: '';
        flex: 1;
        height: 1px;
        background: var(--border);
    }
    .section-heading .accent-mark { color: var(--accent); font-size: 0.9rem; }

    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1px;
        background: var(--border);
        border: 1px solid var(--border);
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 1px;
    }
    .kpi-grid-secondary {
        grid-template-columns: repeat(3, 1fr);
        margin-bottom: 2.5rem;
    }
    .kpi-card {
        background: var(--bg-card);
        padding: 1.4rem 1.6rem;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        transition: background 0.2s;
    }
    .kpi-card:hover { background: #141f38; }
    .kpi-label {
        font-size: 0.68rem;
        font-weight: 400;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--text-muted);
    }
    .kpi-value {
        font-family: 'Syne', sans-serif;
        font-size: 1.9rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1;
        letter-spacing: -0.03em;
    }
    .kpi-value.accent  { color: var(--accent-text); }
    .kpi-value.success { color: var(--success); }
    .kpi-value.warning { color: var(--warning); }
    .kpi-sub {
        font-size: 0.7rem;
        color: var(--text-muted);
        font-weight: 300;
    }

    [data-testid="stSidebar"] {
        background: var(--bg-surface) !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] .block-container { padding: 2rem 1.5rem !important; }
    .sidebar-title {
        font-family: 'Syne', sans-serif;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--accent-text);
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--border);
        margin-bottom: 1.5rem;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        overflow: hidden;
    }
    [data-testid="stDataFrame"] thead tr th {
        background: var(--bg-surface) !important;
        color: var(--text-muted) !important;
        font-size: 0.68rem !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        border-bottom: 1px solid var(--border) !important;
        font-weight: 500 !important;
    }
    [data-testid="stDataFrame"] tbody tr td {
        font-size: 0.78rem !important;
        color: var(--text-primary) !important;
        border-bottom: 1px solid var(--border) !important;
        font-family: 'DM Mono', monospace !important;
    }
    [data-testid="stDataFrame"] tbody tr:hover td { background: var(--accent-soft) !important; }

    .callout {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-left: 3px solid var(--accent);
        border-radius: 0 8px 8px 0;
        padding: 1.2rem 1.4rem;
        display: flex;
        flex-direction: column;
        gap: 0.6rem;
    }
    .callout-title {
        font-family: 'Syne', sans-serif;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--accent-text);
    }
    .callout ul { margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 0.4rem; }
    .callout ul li { font-size: 0.8rem; color: var(--text-label); display: flex; align-items: center; gap: 0.6rem; }
    .callout ul li::before { content: '→'; color: var(--accent); font-weight: 600; }

    hr { border-color: var(--border) !important; margin: 2rem 0 !important; }
    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent); }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─── Data loading ──────────────────────────────────────────────────────────────
data_path = ROOT / "data" / "sample_transactions.csv"
df = pd.read_csv(data_path)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">⚙ Simulation settings</div>', unsafe_allow_html=True)
    max_rows = st.slider(
        "Transaction sample size",
        50, min(500, len(df)), min(200, len(df)), 25,
        help="Number of transactions to include in the simulation",
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Filters**")
    high_amount_only = st.checkbox("High amount only (€80+)", value=False)
    cross_border_only = st.checkbox("Cross-border only", value=False)
    st.markdown("---")
    st.markdown(
        f"""
        <div style='font-size:0.72rem; color:var(--text-muted); line-height:1.8;'>
            Dataset<br>
            <span style='color:var(--text-primary); font-weight:500;'>{len(df):,} transactions loaded</span><br><br>
            Engine<br>
            <span style='color:var(--success); font-weight:500;'>● Active</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ─── Filtering & simulation ───────────────────────────────────────────────────
filtered = df.copy()
if high_amount_only:
    filtered = filtered[filtered["amount_eur"] >= 80]
if cross_border_only:
    filtered = filtered[filtered["is_cross_border"] == True]
filtered = filtered.head(max_rows)

results = decide_actions(filtered)
summary = compute_summary(results)

# ─── Page header ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="page-header">
        <div class="page-header-left">
            <p class="page-title">Payment <span>Decision</span> Engine</p>
            <p class="page-caption">Smart routing · Fraud scoring · Business impact simulation</p>
        </div>
        <div class="status-badge">
            <div class="status-dot"></div>
            Live simulation
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─── Primary KPI row ──────────────────────────────────────────────────────────
st.markdown(
    '<div class="section-heading"><span class="accent-mark">◆</span> Key performance indicators</div>',
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Approval rate</div>
            <div class="kpi-value success">{summary['approval_rate']}%</div>
            <div class="kpi-sub">of processed transactions</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Fallback rate</div>
            <div class="kpi-value warning">{summary['fallback_rate']}%</div>
            <div class="kpi-sub">provider failover events</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Avg latency</div>
            <div class="kpi-value accent">{summary['avg_latency_ms']} ms</div>
            <div class="kpi-sub">decision pipeline</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Gross margin</div>
            <div class="kpi-value">€{summary['gross_margin_total_eur']}</div>
            <div class="kpi-sub">estimated on sample</div>
        </div>
    </div>
    <div class="kpi-grid kpi-grid-secondary">
        <div class="kpi-card">
            <div class="kpi-label">Transactions</div>
            <div class="kpi-value">{summary['transactions']}</div>
            <div class="kpi-sub">in current simulation</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Avg fraud score</div>
            <div class="kpi-value warning">{summary['avg_fraud_score']}</div>
            <div class="kpi-sub">model confidence</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Review rate</div>
            <div class="kpi-value accent">{summary['review_rate']}%</div>
            <div class="kpi-sub">flagged for manual review</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─── Provider breakdown ────────────────────────────────────────────────────────
st.markdown(
    '<div class="section-heading"><span class="accent-mark">◆</span> Provider breakdown</div>',
    unsafe_allow_html=True,
)
st.dataframe(provider_breakdown(results), use_container_width=True, hide_index=False)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Decision output ───────────────────────────────────────────────────────────
st.markdown(
    '<div class="section-heading"><span class="accent-mark">◆</span> Decision output</div>',
    unsafe_allow_html=True,
)
st.dataframe(
    results[
        [
            "transaction_id",
            "country",
            "payment_method",
            "amount_eur",
            "fraud_score",
            "risk_band",
            "selected_provider",
            "decision",
            "final_status",
            "fallback_provider",
            "simulated_latency_ms",
            "gross_margin_eur",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Positioning callout ──────────────────────────────────────────────────────
st.markdown(
    """
    <div class="callout">
        <div class="callout-title">About this project</div>
        <ul>
            <li>Intelligent payment routing with multi-provider fallback and approval optimization</li>
            <li>Latency-sensitive decisioning adapted to high-throughput retail payment flows</li>
            <li>Transparent scoring logic with business KPIs and controllable risk thresholds</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)