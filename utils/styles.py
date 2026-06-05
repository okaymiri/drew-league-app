"""
styles.py — Drew League platform CSS.
Mobile-first sports app aesthetic.
"""

GLOBAL_CSS = """
<style>

/* ─── HIDE STREAMLIT CHROME ─── */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }

/* ─── HIDE SIDEBAR ENTIRELY ─── */
[data-testid="stSidebar"]        { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

/* ─── BASE ─── */
html, body, [data-testid="stAppViewContainer"] {
    background: #080400 !important;
    color: #FFFFFF;
    font-family: Arial, Helvetica, sans-serif;
}

/* ─── CONSTRAIN TO MOBILE WIDTH ─── */
.main .block-container {
    max-width: 520px !important;
    padding: 0 16px 80px 16px !important;
    margin: 0 auto !important;
}

/* ─── APP HEADER ─── */
.app-header {
    position: sticky;
    top: 0;
    z-index: 100;
    background: #080400;
    border-bottom: 1px solid #2A1800;
    padding: 14px 0 12px 0;
    margin-bottom: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* ─── HORIZONTAL NAV (radio as tab bar) ─── */
div[data-testid="stRadio"] {
    background: #080400;
    border-bottom: 1px solid #2A1800;
    margin: 0 -16px !important;
    padding: 0 8px;
    position: sticky;
    top: 53px;
    z-index: 99;
}

div[data-testid="stRadio"] > div {
    display: flex !important;
    flex-direction: row !important;
    overflow-x: auto !important;
    overflow-y: hidden !important;
    gap: 0 !important;
    scrollbar-width: none !important;
    -ms-overflow-style: none !important;
    flex-wrap: nowrap !important;
}

div[data-testid="stRadio"] > div::-webkit-scrollbar {
    display: none;
}

div[data-testid="stRadio"] > div > label {
    flex-shrink: 0 !important;
    padding: 11px 14px !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    color: #444 !important;
    cursor: pointer;
    border-bottom: 2px solid transparent !important;
    white-space: nowrap !important;
    background: transparent !important;
    margin: 0 !important;
    transition: color 0.1s;
}

div[data-testid="stRadio"] > div > label:has(input:checked) {
    color: #FFFFFF !important;
    border-bottom: 2px solid #FFFFFF !important;
}

div[data-testid="stRadio"] > div > label > div:first-child {
    display: none !important;
}

div[data-testid="stRadio"] > div > label > div:last-child p {
    font-size: 10px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}

/* ─── PAGE CONTENT SPACING ─── */
.page-content {
    padding-top: 20px;
}

/* ─── TYPOGRAPHY ─── */
h1, h2, h3, h4 {
    font-family: Arial, Helvetica, sans-serif;
    color: #FFFFFF;
    letter-spacing: -0.02em;
}

/* ─── METRICS ─── */
[data-testid="metric-container"] {
    background: transparent;
    border: none;
    border-top: 1px solid #1E1200;
    border-radius: 0;
    padding: 14px 0;
}

[data-testid="metric-container"] label {
    color: #555 !important;
    font-size: 9px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.15em !important;
    font-weight: 700 !important;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-size: 24px !important;
    font-weight: 900 !important;
}

/* ─── TABS ─── */
[data-baseweb="tab-list"] {
    background: #000;
    border-bottom: 1px solid #1E1200;
    gap: 0;
    overflow-x: auto;
}

[data-baseweb="tab"] {
    color: #444 !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    font-size: 10px !important;
    letter-spacing: 0.1em !important;
    border-radius: 0 !important;
    padding: 10px 16px !important;
    white-space: nowrap;
}

[aria-selected="true"] {
    color: #FFFFFF !important;
    border-bottom: 2px solid #FFFFFF !important;
    background: transparent !important;
}

/* ─── BUTTONS ─── */
.stButton > button {
    background: #FFFFFF;
    color: #080400;
    border: none;
    border-radius: 0;
    font-weight: 700;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 12px 20px;
    width: 100%;
    transition: background 0.1s;
}

.stButton > button:hover {
    background: #FF5500 !important;
    color: #FFFFFF !important;
}

/* ─── INPUTS ─── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea textarea {
    background: #0D0800 !important;
    border: 1px solid #1E1200 !important;
    color: #FFFFFF !important;
    border-radius: 0 !important;
    font-size: 14px !important;
}

/* ─── SELECTBOX ─── */
.stSelectbox label, .stTextInput label, .stTextArea label {
    font-size: 10px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    color: #555 !important;
}

/* ─── DATAFRAME ─── */
.stDataFrame { border: 1px solid #1E1200; border-radius: 0; }

/* ─── DIVIDER ─── */
hr { border: none; border-top: 1px solid #1E1200; margin: 20px 0; }

/* ─── CARD ─── */
.drew-card {
    background: #0D0800;
    border: 1px solid #1E1200;
    border-radius: 0;
    padding: 16px;
    margin-bottom: 10px;
}

.drew-card:hover { border-color: #2A1800; }

/* ─── BADGE ─── */
.drew-badge {
    background: transparent;
    color: #555;
    border: 1px solid #2A1800;
    padding: 2px 7px;
    border-radius: 0;
    font-size: 9px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    display: inline-block;
}

.drew-badge-live {
    background: #FF5500;
    color: #FFFFFF;
    border: none;
}

/* ─── SCORE DISPLAY ─── */
.score-card {
    background: #0D0800;
    border: 1px solid #1E1200;
    border-radius: 0;
    padding: 20px 16px;
    text-align: center;
}

.score-card .team-name {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #666;
}

.score-card .score {
    font-size: 44px;
    font-weight: 900;
    color: #FFFFFF;
    line-height: 1;
    margin: 6px 0;
}

.score-card .vs,
.vs {
    font-size: 11px;
    color: #2A1800;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

/* ─── HIGHLIGHT CARD ─── */
.highlight-card {
    background: #0D0800;
    border: 1px solid #1E1200;
    padding: 14px;
    margin-bottom: 8px;
}

/* ─── SPONSOR CHIP ─── */
.sponsor-chip {
    background: transparent;
    border: 1px solid #1E1200;
    padding: 8px 14px;
    font-weight: 700;
    font-size: 11px;
    color: #555;
    margin: 3px;
    display: inline-block;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ─── PAGE HERO ─── */
.page-hero {
    background: transparent;
    border-bottom: 1px solid #1E1200;
    padding: 36px 0 28px 0;
    margin-bottom: 28px;
}

.page-hero::before { display: none; }

/* ─── MEMBERSHIP ─── */
.membership-card {
    padding: 20px;
    margin-bottom: 10px;
    border: 1px solid #1E1200;
    background: #0D0800;
    border-radius: 0;
}

.membership-card.insider { border-color: #FF5500; }
</style>
"""


def inject_css():
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def card(content_html, extra_class=""):
    return f'<div class="drew-card {extra_class}">{content_html}</div>'


def badge(text, variant="default"):
    cls = "drew-badge"
    if variant == "live":
        cls += " drew-badge-live"
    return f'<span class="{cls}">{text}</span>'


def section_header(title, subtitle=""):
    label = f'<div style="font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:0.15em;color:#555;margin-bottom:6px;">{subtitle}</div>' if subtitle else ""
    return f'<div style="margin:24px 0 16px 0;">{label}<h2 style="font-size:22px;font-weight:900;margin:0;text-transform:uppercase;letter-spacing:-0.01em;color:#FFFFFF;">{title}</h2></div>'
