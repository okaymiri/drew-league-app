"""
styles.py — Global CSS injection for Drew League app.
Dark mode, premium sports-media feel, Drew League brand palette.
"""


DREW_COLORS = {
    "black": "#0A0A0A",
    "dark_bg": "#111111",
    "card_bg": "#1A1A1A",
    "border": "#2A2A2A",
    "white": "#FFFFFF",
    "cream": "#F5F0E8",
    "red": "#C8102E",
    "red_dark": "#A00C24",
    "gold": "#FFD700",
    "gold_muted": "#C9A84C",
    "wood": "#B8864E",
    "text_secondary": "#999999",
    "text_muted": "#666666",
    "success": "#22C55E",
    "upcoming": "#3B82F6",
}

GLOBAL_CSS = """
<style>
/* ─── RESET & BASE ─── */
* { box-sizing: border-box; }

[data-testid="stAppViewContainer"] {
    background-color: #0A0A0A;
    color: #FFFFFF;
}

[data-testid="stSidebar"] {
    background-color: #111111 !important;
    border-right: 1px solid #2A2A2A;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

/* ─── HIDE STREAMLIT CHROME ─── */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* ─── TYPOGRAPHY ─── */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Arial Black', 'Impact', sans-serif;
    color: #FFFFFF;
    letter-spacing: -0.02em;
}

p, div, span, label {
    font-family: 'Arial', sans-serif;
    color: #FFFFFF;
}

/* ─── METRICS ─── */
[data-testid="metric-container"] {
    background: #1A1A1A;
    border: 1px solid #2A2A2A;
    border-radius: 8px;
    padding: 16px;
}

[data-testid="metric-container"] label {
    color: #999999 !important;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #FFD700 !important;
    font-size: 28px;
    font-weight: 900;
}

/* ─── TABS ─── */
[data-baseweb="tab-list"] {
    background: #111111;
    border-bottom: 1px solid #2A2A2A;
}

[data-baseweb="tab"] {
    color: #999999 !important;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 13px;
    letter-spacing: 0.05em;
}

[aria-selected="true"] {
    color: #FFFFFF !important;
    border-bottom: 3px solid #C8102E !important;
}

/* ─── BUTTONS ─── */
.stButton > button {
    background: #C8102E;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    font-weight: 700;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    transition: all 0.15s ease;
    padding: 10px 20px;
}

.stButton > button:hover {
    background: #A00C24;
    transform: translateY(-1px);
}

/* ─── INPUTS ─── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea textarea {
    background: #1A1A1A !important;
    border: 1px solid #2A2A2A !important;
    color: #FFFFFF !important;
    border-radius: 6px;
}

/* ─── DATAFRAME ─── */
.stDataFrame {
    border: 1px solid #2A2A2A;
    border-radius: 8px;
    overflow: hidden;
}

/* ─── DIVIDER ─── */
hr {
    border: none;
    border-top: 1px solid #2A2A2A;
    margin: 24px 0;
}

/* ─── CUSTOM COMPONENTS ─── */
.drew-card {
    background: #1A1A1A;
    border: 1px solid #2A2A2A;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    transition: border-color 0.15s ease;
}

.drew-card:hover {
    border-color: #C8102E;
}

.drew-badge {
    background: #C8102E;
    color: #FFFFFF;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    display: inline-block;
}

.drew-badge-gold {
    background: #FFD700;
    color: #0A0A0A;
}

.drew-badge-live {
    background: #22C55E;
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}

.score-card {
    background: #1A1A1A;
    border: 1px solid #2A2A2A;
    border-radius: 12px;
    padding: 24px;
    text-align: center;
}

.score-card .team-name {
    font-size: 16px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #FFFFFF;
}

.score-card .score {
    font-size: 48px;
    font-weight: 900;
    color: #FFD700;
    line-height: 1;
    margin: 8px 0;
}

.score-card .vs,
.vs {
    font-size: 20px;
    color: #666666;
    font-weight: 700;
}

.highlight-card {
    background: #1A1A1A;
    border: 1px solid #2A2A2A;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
}

.highlight-card:hover {
    border-color: #C8102E;
    cursor: pointer;
}

.membership-card {
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 16px;
    border: 2px solid transparent;
}

.membership-card.free { border-color: #2A2A2A; background: #1A1A1A; }
.membership-card.insider { border-color: #C8102E; background: #1A1A1A; }
.membership-card.courtside { border-color: #FFD700; background: #1A0A00; }
.membership-card.legacy { border-color: #C9A84C; background: #0D0A00; }

.stat-leader-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid #2A2A2A;
}

.sponsor-chip {
    background: #1A1A1A;
    border: 1px solid #2A2A2A;
    border-radius: 8px;
    padding: 12px 20px;
    text-align: center;
    font-weight: 700;
    font-size: 14px;
    color: #FFFFFF;
    margin: 4px;
    display: inline-block;
}

.nav-header {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #666666;
    margin: 20px 0 8px 0;
    padding: 0 8px;
}

.page-hero {
    background: linear-gradient(135deg, #1A0A0A 0%, #0A0A0A 50%, #0A0005 100%);
    border: 1px solid #2A2A2A;
    border-radius: 16px;
    padding: 40px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}

.page-hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #C8102E, #FFD700, #C8102E);
}
</style>
"""


def inject_css():
    """Import and inject global styles into Streamlit."""
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def card(content_html, extra_class=""):
    """Wrap content in a styled drew-card div."""
    return f'<div class="drew-card {extra_class}">{content_html}</div>'


def badge(text, variant="default"):
    cls = "drew-badge"
    if variant == "gold":
        cls += " drew-badge-gold"
    elif variant == "live":
        cls += " drew-badge-live"
    return f'<span class="{cls}">{text}</span>'


def section_header(title, subtitle=""):
    sub = f'<p style="color:#999;font-size:14px;margin:4px 0 0 0;">{subtitle}</p>' if subtitle else ""
    return f"""
    <div style="margin-bottom:24px;">
        <h2 style="font-size:28px;font-weight:900;margin:0;text-transform:uppercase;letter-spacing:-0.01em;">{title}</h2>
        {sub}
    </div>
    """
